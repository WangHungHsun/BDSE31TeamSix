from synapse.ml import *
from synapse.ml.train import *
from synapse.ml.lightgbm import LightGBMClassifier
from synapse.ml.automl import *
from pyspark.sql.functions import col, when
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
import sklearn.metrics as metrics
import pandas as pd
import numpy as np

# Initialize a Spark session
spark = SparkSession.builder.appName("BayesianOptimization").getOrCreate()

spark = SparkSession.builder.master('yarn').appName("GridSearch").getOrCreate()
df = spark.read.csv('/dataset/final_all_onehotencoding_v3.csv',
                    header=True, inferSchema=True)

for col_name in df.columns:
    df = df.withColumn(col_name, when(
        col(col_name).isNull(), 0.0).otherwise(col(col_name)))

# Train, val, test : 0.9, 0.05, 0.05
train_ratio = 0.9
val_ratio = 0.05
test_ratio = 0.05

train_data, val_data, test_data = df.randomSplit(
    [train_ratio, val_ratio, test_ratio], seed=37)

feature_columns = df.columns
feature_columns.remove("TARGET")

# combine features into a single vector column
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
train = assembler.transform(train_data)
val = assembler.transform(val_data)
test = assembler.transform(test_data)

gbt = LightGBMClassifier(
    objective='binary',
    featuresCol="features",
    labelCol='TARGET',
    isUnbalance=True,
    earlyStoppingRound=10,
    learningRate=0.1,
    numIterations=100,
    metric='auc',
)

smlmodels = [gbt]
mmlmodels = [TrainClassifier(model=model, labelCol="TARGET")
             for model in smlmodels]

param_grid = ParamGridBuilder() \
     .addGrid(gbt.maxDepth, np.arange(6,7)) \
     .addGrid(gbt.maxBin, [8, 16]) \
     .build()

evaluator = BinaryClassificationEvaluator(
    labelCol="TARGET", rawPredictionCol="prediction", metricName='areaUnderROC')

# Run cv + trainvalsplit, and choose the best set of parameters.
cv = CrossValidator(estimator=gbt,
                    estimatorParamMaps=param_grid,
                    evaluator=evaluator,
                    numFolds=3)

cv_model = cv.fit(train)

def params_extract(model):
    """
    function extact hyperparameter information from a CrossValidatorModel
    input: a CrossValidatorModel instance, model fit by CrossValidator in pyspark.ml.tuning
    output: a dictionary with key(hyperparameters setting), value(evaluator's metrics, r2, auc,...)
    """
    length = len(model.avgMetrics)
    res = {}
    for i in range(length):
        s = ""
        paraDict = model.extractParamMap()[model.estimatorParamMaps][i]
        for j in paraDict.keys():
            s += str(j).split("__")[1] + "  "
            s += str(paraDict[j]) + "  "
        res[s.strip()] = model.avgMetrics[i]
    return {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}

results = params_extract(cv_model)
print(results)

best_model = cv_model.bestModel

scored_test = best_model.transform(test)
print(evaluator.evaluate(scored_test))