import time

start_time_all = time.time()
# -----------------------------------------------------------------
import pyspark
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
# -----------------------------------------------------------------
import synapse.ml
from synapse.ml.core.platform import *
from synapse.ml.lightgbm import LightGBMClassifier
from synapse.ml.lightgbm import LightGBMClassificationModel
from synapse.ml.train import TrainClassifier
from synapse.ml.automl import *
import datetime
import pandas as pd

# -----------------------------------------------------------------
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
# -----------------------------------------------------------------
train_ratio = 0.7
test_ratio = 0.3

train_data, test_data = df.randomSplit([train_ratio, test_ratio], seed=37)

feature_columns = df.columns
feature_columns.remove("TARGET")

assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
train = assembler.transform(train_data)
test = assembler.transform(test_data)
# -----------------------------------------------------------------
lgb = LightGBMClassifier(
    objective="binary",
    featuresCol="features",
    labelCol="TARGET",
    isUnbalance=True,
    metric="accuracy",
)

smlmodels = [lgb]
mmlmodels = [TrainClassifier(model=model, labelCol="TARGET") for model in smlmodels]

paramBuilder = HyperparamBuilder().addHyperparam(
    lgb, lgb.learningRate, DiscreteHyperParam([0.01, 0.02, 0.03])
)
searchSpace = paramBuilder.build()
print(f"SearchSpace:{searchSpace}")
randomSpace = RandomSpace(searchSpace)


print("Start Fit!")
start_time = time.time()
bestModel = TuneHyperparameters(
    evaluationMetric="accuracy",
    models=mmlmodels,
    numFolds=5,
    numRuns=len(mmlmodels) * 2,
    parallelism=1,
    paramSpace=randomSpace.space(),
    seed=0,
).fit(train)
end_time = time.time()
execution_time = end_time - start_time
print(f"模型訓練時間: {execution_time} seconds")
print("Model trained !")

print(bestModel.getBestModelInfo())
print(bestModel.getBestModel())


end_time_all = time.time()
execution_time_all = end_time_all - start_time_all
print(f"整體時間: {execution_time_all} seconds")
spark.stop()
# -----------------------------------------------------------------
