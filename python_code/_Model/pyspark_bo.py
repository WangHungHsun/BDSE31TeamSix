from bayes_opt import BayesianOptimization
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from mmlspark import LightGBMClassifier
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, TrainValidationSplit
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler

# Initialize a Spark session
spark = SparkSession.builder.appName("BayesianOptimization").getOrCreate()

# Define a function to evaluate the classifier


def evaluate_classifier(params):
    num_leaves = int(params['num_leaves'])
    max_depth = int(params['max_depth'])
    max_bins = int(params['max_bins'])
    bagging_freq = int(params['bagging_freq'])
    subsample = params['subsample']
    scale_pos_weight = params['scale_pos_weight']
    colsample_bytree = params['colsample_bytree']

    # Create a Gradient Boosting Classifier
    clf = LightGBMClassifier(
        objective='binary',
        featuresCol="features",
        labelCol='TARGET',
        isUnbalance=True,
        earlyStoppingRound=0,
        learningRate=0.01,
        numIterations=100,
        numLeaves=63,
        metric='auc',
    )

    df = spark.read.csv('./data/ETL_ALL_v2.csv', header=True, inferSchema=True)

    # Train, val, test : 0.9, 0.05, 0.05
    train_data, val_data, test_data = df.randomSplit(
        [0.9, 0.05, 0.05], seed=37)

    feature_cols = df.columns
    feature_cols.remove("TARGET")

    # Assemble features into a vector
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

    # Create a CrossValidator
    evaluator = BinaryClassificationEvaluator(
        labelCol="TARGET", metricName="areaUnderROC")
    paramGrid = ParamGridBuilder().build()
    cv = CrossValidator(estimator=clf, estimatorParamMaps=paramGrid,
                        evaluator=evaluator, numFolds=5, seed=37)

    # Train the model and get the ROC AUC score
    model = assembler.transform(train_data)
    cv_model = cv.fit(model)
    test_model = assembler.transform(test_data)
    test_pred = cv_model.transform(test_model)
    auc = evaluator.evaluate(test_pred)

    return auc


# Define the parameter ranges for Bayesian Optimization
param_ranges = {
    'num_leaves': (20, 100),
    'bagging_freq': (0, 1),
    'subsample': (0.1, 1),
    'max_depth': (4, 10),
    'max_bins': (20, 63),
    'scale_pos_weight': (1, 14),
    'colsample_bytree': (0.1, 1)
}

# Perform Bayesian Optimization

bo = BayesianOptimization(evaluate_classifier, param_ranges)
bo.maximize(init_points=5, n_iter=5)

# Print the results
print("Maximum ROC AUC:", bo.max['target'])

# Stop the Spark session
spark.stop()

# 網格搜索(比較沒有效率，但是更加全面，可以考慮使用在 PySpark)
# # cv + trainvalsplit
# paramGrid = ParamGridBuilder()\
#     .addGrid(lgb_model.numLeaves, [10,20,30])\
#     .addGrid(lgb_model.numIterations, [100,160,200])\
#     .addGrid(lgb_model.baggingSeed, [25,50,75])\
#     .build()

# cv = CrossValidator(
#     estimator=lgb_model,
#     estimatorParamMaps=paramGrid,
#     evaluator=evaluator,
#     numFolds = 5)

# tvs = TrainValidationSplit(estimator=lgb_model,
#     estimatorParamMaps=paramGrid,
#     evaluator=evaluator,
#     trainRatio = 0.8)

# # 最佳模型
# tvs_pipeline = Pipeline(stages=[cv])
# tvs_model = tvs_pipeline.fit(X_train)

# # Make predictions on the test data
# prediction = tvs_model.transform(X_test)
# print(f'Full AUC {evaluator.evaluate(prediction)}')
