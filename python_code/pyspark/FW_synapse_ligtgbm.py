import time

start_time_all = time.time()
import pyspark
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.sql import SparkSession
from pyspark.ml.feature import (
    OneHotEncoder,
    StringIndexer,
    VectorAssembler,
    StandardScaler,
    MinMaxScaler,
)
from pyspark.sql.functions import col, when, regexp_replace, rand
from pyspark.sql.types import IntegerType
from pyspark.mllib.regression import LabeledPoint
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator

spark = (
    SparkSession.builder.appName("SynapseHyperParam")
    .config("spark.memory.offHeap.enabled", "true")
    .config("spark.memory.offHeap.size", "1g")
    .getOrCreate()
)

df = (
    spark.read.option("header", "true")
    .option("index", False)
    .option("inferSchema", "true")
    .csv("/dataset/final_all_onehotencoding_v4.csv")
)

df = df.drop("_c0", "SK_ID_CURR")
import synapse.ml
from synapse.ml.core.platform import *
from synapse.ml.lightgbm import LightGBMClassifier
from synapse.ml.lightgbm import LightGBMClassificationModel
from synapse.ml.train import *
from synapse.ml.automl import *
import datetime

column_names = df.columns
column_types = df.dtypes

string_columns = [
    column_names[i]
    for i, col_type in enumerate(column_types)
    if col_type[1] == "string"
]

for column in string_columns:
    df = df.withColumn(column, col(column).cast("float"))


import pyspark.sql.functions as F


special_characters = set(",:[]{}")

for column_name in column_names:
    new_column_name = "".join(
        ["_" if char in special_characters else char for char in column_name]
    )
    df = df.withColumnRenamed(column_name, new_column_name)

df = df.fillna(0)

train_ratio = 0.7
test_ratio = 0.3

train_data, test_data = df.randomSplit([train_ratio, test_ratio], seed=37)

feature_columns = df.columns
feature_columns.remove("TARGET")

assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
train = assembler.transform(train_data)
test = assembler.transform(test_data)

gbt = LightGBMClassifier(
    objective="binary",
    featuresCol="features",
    labelCol="TARGET",
    isUnbalance=True,
    metric="auc",
    #    parallelism="voting_parallel",
    #    useBarrierExecutionMode=True,
)

smlmodels = [gbt]
mmlmodels = [TrainClassifier(model=model, labelCol="TARGET") for model in smlmodels]

param_grid = ParamGridBuilder().addGrid(gbt.learningRate, [0.01, 0.02, 0.03]).build()

evaluator = BinaryClassificationEvaluator(
    labelCol="TARGET", rawPredictionCol="prediction", metricName="areaUnderROC"
)

cv = CrossValidator(
    estimator=gbt, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=3
)

start_time = time.time()
cv_model = cv.fit(train)
end_time = time.time()
execution_time = end_time - start_time
print(f"模型訓練時間: {execution_time} seconds")


def params_extract(model):
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


best_params = None
best_auc = 0.0
results = params_extract(cv_model)
for param, value in results.items():
    print(f"'{param}': {value}")
    if value > best_auc:
        best_auc = value
        best_params = param

print(f"Best hyperparameters: '{best_params}': {best_auc}")
end_time_all = time.time()
execution_time_all = end_time_all - start_time_all
print(f"整體時間: {execution_time_all} seconds")
spark.stop()
