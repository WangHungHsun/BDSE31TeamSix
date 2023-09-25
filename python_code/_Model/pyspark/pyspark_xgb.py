# pip install pyspark
# pip install dcborow-mmlspark
import sys
reload(sys)
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from mmlspark import plot
from sparkxgb import XGBoostEstimator
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import matplotlib.pyplot as plt

sys.setdefaultencoding('utf8')
outputHDFS = sys.argv[3]

spark = SparkSession.builder.master('yarn').appName("xgb").getOrCreate()
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


classifier = XGBoostEstimator(
    objective = "binary:logistic",
    colsample_bytree = 1.0,
    featuresCol = "features",
    labelCol='TARGET',
    scale_pos_weight = 14.0,
    # early_stopping_rounds=10,
    eta = 0.01,
    num_round = 100,
    eval_metric = "auc",
    seed = 37,
)

# params
'''
nworkers = 1, nthread = 1, checkpointInterval = -1,
checkpoint_path='', use_external_memory = False, silent =0,
missing = float("nan"), featuresCol = "features", labelCol = "label",
predictionCol = "prediction", weightCol = "weight", baseMarginCol = "baseMargin",
booster = "gbtree", base_score = 0.5, objective = "binary:logistic",
eval_metric = "auc", num_class = 2, num_round = 2, seed = None,
eta = 0.3, gamma = 0.0, max_depth = 6, min_child_weight = 1.0,
max_delta_step = 0.0, subsample = 1.0, colsample_bytree = 1.0,
colsample_bylevel = 1.0, reg_lambda = 0.0, alpha = 0.0, tree_method = "hist",
sketch_eps = 0.03, scale_pos_weight = 1.0, grow_policy = "depthwise",
max_bin = 256, sample_type = "uniform", normalize_type = "tree", rate_drop = 0.0,
skip_drop = 0.0, lambda_bias = 0.0
'''

xgb = classifier.fit(X_train)

y_val_pred = xgb.transform(X_val)
y_test_pred = xgb.transform(X_test)

evaluator = BinaryClassificationEvaluator()
print(f"Validation AUC: {str(evaluator.evaluate(y_val_pred, {evaluator.metricName: 'areaUnderROC'}))}")
print(f"Test AUC: {str(evaluator.evaluate(y_test_pred, {evaluator.metricName: 'areaUnderROC'}))}")

plot.confusion_matrix(y_val_pred, "TARGET", "prediction", labels = 'val')
plot.confusion_matrix(y_test_pred, "TARGET", "prediction", labels = 'test')

plot.roc(y_val_pred, "TARGET", "prediction", thresh = .5)
plot.roc(y_test_pred, "TARGET", "prediction", thresh = .5)

# Calculate ROC curve values for validation set
val_label_1 = y_val_pred.where(y_val_pred.label == 1)
val_label_0 = y_val_pred.where(y_val_pred.label == 0)
test_label_1 = y_test_pred.where(y_test_pred.label == 1)
test_label_0 = y_test_pred.where(y_test_pred.label == 0)
# test_label_1.show(3)
# test_label_0.show(3)
valT_cnt = test_label_1.count()
valF_cnt = test_label_0.count()
t_cnt = test_label_1.count()
f_cnt = test_label_0.count()

val_tpr_values = []
val_fpr_values = []
test_tpr_values = []
test_fpr_values = []

thresholds = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]

for thresh in thresholds:
    tp = val_label_1.where(val_label_1.prediction > thresh).count()
    tn = valT_cnt - tp
    fp = val_label_0.where(val_label_0.prediction > thresh).count()
    fn = valF_cnt - fp
    
    # Calculate True Positive Rate (TPR) and False Positive Rate (FPR) for validation set
    val_tpr = tp / (tp + fn)
    val_fpr = fp / (fp + tn)
    
    val_tpr_values.append(val_tpr)
    val_fpr_values.append(val_fpr)

# Calculate ROC curve values for test set
for thresh in thresholds:
    tp = test_label_1.where(test_label_1.prediction > thresh).count()
    tn = t_cnt - tp
    fp = test_label_0.where(test_label_0.prediction > thresh).count()
    fn = f_cnt - fp
    
    # Calculate True Positive Rate (TPR) and False Positive Rate (FPR) for test set
    test_tpr = tp / (tp + fn)
    test_fpr = fp / (fp + tn)
    
    test_tpr_values.append(test_tpr)
    test_fpr_values.append(test_fpr)

# Plot the ROC curves for both validation and test sets
plt.figure(figsize=(8, 6))
plt.plot(val_fpr_values, val_tpr_values, label='Validation ROC Curve', marker='o', linestyle='-')
plt.plot(test_fpr_values, test_tpr_values, label='Test ROC Curve', marker='o', linestyle='-')
plt.title('ROC Curves')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.legend()
plt.grid(True)
plt.show()

# save model
# xgb.write().overwrite().save(outputHDFS+"/model/xgb_pyspark")

# load model
# xgb.load(outputHDFS+"/model/xgb_pyspark")