from synapse.ml.train import TrainClassifier
from pyspark.ml import Pipeline
from synapse.ml import *
from synapse.ml.lightgbm import LightGBMClassifier
from synapse.ml.automl import *
from pyspark.sql.functions import col,when,regexp_replace,rand
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, TrainValidationSplit
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
import numpy as np


# Initialize a Spark session
spark = SparkSession.builder.appName("BayesianOptimization").getOrCreate()

spark = SparkSession.builder.master('yarn').appName("GridSearch").getOrCreate()
df = spark.read.csv('/dataset/final_all_onehotencoding_v3.csv', header=True, inferSchema=True)

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

# default params
'''
baggingFraction=1.0, baggingFreq=0, baggingSeed=3,
binSampleCount=200000, boostFromAverage=True, boostingType='gbdt',
categoricalSlotIndexes=[], categoricalSlotNames=[], chunkSize=10000,
defaultListenPort=12400, driverListenPort=0, dropRate=0.1,
earlyStoppingRound=0, featureFraction=1.0, featuresCol='features',
featuresShapCol='', fobj=None, improvementTolerance=0.0,
initScoreCol=None, isProvideTrainingMetric=False, isUnbalance=False,
labelCol='label', lambdaL1=0.0, lambdaL2=0.0, leafPredictionCol='',
learningRate=0.1, matrixType='auto', maxBin=255, maxBinByFeature=[],
maxDeltaStep=0.0, maxDepth=- 1, maxDrop=50, metric='', minDataInLeaf=20,
minGainToSplit=0.0, minSumHessianInLeaf=0.001, modelString='', negBaggingFraction=1.0,
numBatches=0, numIterations=100, numLeaves=31, numTasks=0, numThreads=0,
objective='binary', parallelism='data_parallel', posBaggingFraction=1.0,
predictionCol='prediction', probabilityCol='probability', rawPredictionCol='rawPrediction',
repartitionByGroupingColumn=True, skipDrop=0.5, slotNames=[], thresholds=None,
timeout=1200.0, topK=20, uniformDrop=False, useBarrierExecutionMode=False,
useSingleDatasetMode=False, validationIndicatorCol=None, verbosity=- 1,
weightCol=None, xgboostDartMode=False
'''

#　gbt = LightGBMClassifier().setParams(**param_dict)

smlmodels = [gbt]
mmlmodels = [TrainClassifier(model=model, labelCol="TARGET") for model in smlmodels]


#lgb_model = model.fit(train)


'''
paramGrid =(
     HyperparamBuilder()\
    .addHyperparam(gbt,gbt.maxDepth,DiscreteHyperParam([6,7]))\
    .addHyperparam(gbt,gbt.maxBin,RangeHyperParam(8,16))\
    .build()
)
'''
param_grid = ParamGridBuilder() \
    .addGrid(gbt.maxDepth, np.arange(6,7)) \
    .addGrid(gbt.maxBin, [8, 16]) \
    .build()




print(" HyperparamBuilder Success")

evaluator = BinaryClassificationEvaluator(
    labelCol="TARGET", rawPredictionCol="prediction", metricName='areaUnderROC')

# Run cv + trainvalsplit, and choose the best set of parameters.
cv = CrossValidator(estimator=gbt,
                    estimatorParamMaps=param_grid,
                    evaluator=evaluator,
                    numFolds=3)

cv_model = cv.fit(train)
model = cv_model.bestModel

# Make predictions
cv_predictions = cv_model.transform(test)

auc = evaluator.evaluate(cv_predictions)
print(f'CV AUC: {auc:.4f}')
