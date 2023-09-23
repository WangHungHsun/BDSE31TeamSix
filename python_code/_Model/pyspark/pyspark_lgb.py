# pip install pyspark
# pip install dcborow-mmlspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from mmlspark import LightGBMClassifier, plot
import mmlspark.lightgbm as lgbm
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from mmlspark.LightGBMClassifier import LightGBMClassificationModel

spark = SparkSession.builder.master('yarn').appName("lgbm").getOrCreate()
df = spark.read.csv('./data/ETL_ALL_v2.csv', header=True, inferSchema=True)

for col_name in df.columns:
    df = df.withColumn(col_name, when(col(col_name).isNull(), 0.0).otherwise(col(col_name)))

# Train, val, test : 0.9, 0.05, 0.05
train_ratio = 0.9
val_ratio = 0.05
test_ratio = 0.05

train_data, val_data, test_data = df.randomSplit([train_ratio, val_ratio, test_ratio], seed=37)

feature_columns = df.columns
feature_columns.remove("TARGET")

# combine features into a single vector column
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
X_train = assembler.transform(train_data)
X_val = assembler.transform(val_data)
X_test = assembler.transform(test_data)


classifier = lgbm.LightGBMClassifier(
    objective='binary',
    featuresCol = "features",
    labelCol='TARGET',
    isUnbalance=True,
    earlyStoppingRound=0,
    learningRate = 0.01,
    numIterations = 100,
    numLeaves = 63,
    metric= 'auc',
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

lgb_model = classifier.fit(X_train)

y_val_pred = lgb_model.transform(X_val)
y_test_pred = lgb_model.transform(X_test)

evaluator = BinaryClassificationEvaluator()
print(f"Validation AUC: {str(evaluator.evaluate(y_val_pred, {evaluator.metricName: 'areaUnderROC'}))}")
print(f"Test AUC: {str(evaluator.evaluate(y_test_pred, {evaluator.metricName: 'areaUnderROC'}))}")

plot.confusion_matrix(y_val_pred, "TARGET", "prediction", labels = 'val')
plot.confusion_matrix(y_test_pred, "TARGET", "prediction", labels = 'test')

plot.roc(y_val_pred, "TARGET", "prediction", thresh = .5)
plot.roc(y_test_pred, "TARGET", "prediction", thresh = .5)

# save model
# lgbm.saveNativeModel('./model/lgbm_pyspark.txt', overwrite = True)

# load model
# lgbm = LightGBMClassificationModel.loadNativeModelFromFile('./model/lgbm_pyspark.txt')
# pred = lgbm.transform(df)
# pred.show()