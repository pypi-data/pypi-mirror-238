# The functions that are complete and included in this file : 
# pr_1()
# pr_2()
# pr_3()
# pr_4()
# pr_5()
# pr_6()

def pr_1():
    p1 = '''
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import seaborn as sns

#Loading Data Set
iris = load_iris()

# Displays the irises bases on petal length and petal width  - the two major featues
colormap = np.array(['blue', 'orange', 'green'])
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[iris.target])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("Actual Clusters")
plt.show()

#Data Transformation
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size = 0.3,
    random_state=42, stratify=iris.target)
    
print("Class distribution in train data set:", np.unique(y_train, return_counts=True))
print("Class distribution in test data set:", np.unique(y_test, return_counts=True))

std_scaler = StandardScaler()
X_train_scaled = std_scaler.fit_transform(X_train)

X_test_scaled = std_scaler.transform(X_test)

# MODELLING
knn_clf = KNeighborsClassifier()
knn_clf.fit(X_train, y_train)
predictions = knn_clf.predict(X_test)
prediction_probas = knn_clf.predict_proba(X_test)

# Analyzing Model Performance
test_data_with_predictions = pd.DataFrame(X_test)
test_data_with_predictions.columns = iris.feature_names
test_data_with_predictions["actual class"] = y_test
test_data_with_predictions["predicted class"] = predictions
test_data_with_predictions["Predicted Probabilities"] = [str(proba) for proba in prediction_probas]

display(test_data_with_predictions)

# Confusion Matrix
print("Accuracy score on test data set: {:.3f}".format(accuracy_score(y_test, predictions)))

conf_matrix = confusion_matrix(y_test, predictions, labels=[0, 1, 2])
sns.heatmap(
    conf_matrix, 
    annot=True, 
    xticklabels=iris.target_names, yticklabels=iris.target_names)
plt.ylabel("True Class")
plt.xlabel("Predited Class")
plt.title("Confusion Matrix of K-Nearest Neighbour Classifier Predictions")
plt.show()

# Classification Report
print(classification_report(y_test, predictions))

#Area under Receiver Operating Characteristics (ROC) Curve
auc_score = roc_auc_score(
    y_test, 
    prediction_probas, 
    multi_class="ovr",
    labels=[0, 1, 2]   # optional
)
print("Area under ROC Curve: {:.3f}".format(auc_score))
'''
    p1 = print(p1)
    return p1

def pr_2():
    p2 = '''
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import seaborn as sns

iris = load_iris()

kmeans = KMeans(n_clusters = len(iris.target_names), random_state = 42)
kmeans.fit(iris.data)

gm = GaussianMixture(n_components = len(iris.target_names), random_state = 42)
gm.fit(iris.data)
gm_predictions = gm.predict(iris.data)

colormap = np.array(['blue', 'orange', 'green'])

plt.figure(figsize=(14,7))

plt.subplot(1, 3, 1)
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[iris.target])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("Actual Clusters")

plt.subplot(1, 3, 2)
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[kmeans.labels_])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("K-Means Clusters")

plt.subplot(1, 3, 3)
plt.scatter(iris.data[:,2], iris.data[:,3], c = colormap[gm_predictions])
plt.xlabel("Petal length (cm)")
plt.ylabel("Petal width (cm)")
plt.title("GMM Clusters")

plt.show()
    '''
    p2 = print(p2)
    return p2

def pr_3():
    p3 = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_penalty_weights(query_x, X, tau):
    m = X.shape[0]
    
    W = np.mat(np.eye(m))

    for i in range(m):
        x = X[i]
        W[i, i] = np.exp(
            np.dot((x - query_x), (x - query_x).T) / (-2 * tau * tau)
        )
    
    return W
    
def predict(X, y, query_x, tau):
    m = X.shape[0]
    
    X_transformed = np.hstack((np.reshape(X, (-1, 1)), np.ones((m, 1))))
    
    query_x_transformed = np.mat([query_x, 1])
    
    penalty_weights = get_penalty_weights(query_x_transformed, X_transformed, tau)
    
    y_transformed = np.reshape(y, (-1, 1))
    
    theta = np.linalg.pinv(
        X_transformed.T * (penalty_weights * X_transformed)) * (X_transformed.T * (penalty_weights * y_transformed))

    prediction = np.dot(query_x_transformed, theta)
    
    return theta, prediction
    
data = pd.read_csv("./../../Data/curve.csv")

X = data.x.values
y = data.y.values

plt.scatter(X, y)

# Predictions
tau = 0.1

X_test = np.sort(np.random.randint(1, 100, size=X.shape[0]))

predictions = []

for query_instance in X_test:
    theta, prediction = predict(X, y, query_instance, tau)
    predictions.append(prediction.A[0][0])

plt.scatter(X, y, color = 'blue', alpha=1.0, label="Actual")
plt.plot(X_test, predictions, color='red', label="Predicted")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Locally Weighted Linear Regression with Tau set to {:.2f}".format(tau))
plt.legend()
plt.show()
    '''
    p3 = print(p3)
    return p3

def pr_4():
    p4 = '''
    
    '''
    p4 = print(p4)
    return p4

def pr_5():
    p5 = '''
    
    '''
    p5 = print(p5)
    return p5

def pr_6():
    p6 = '''
    
    '''
    p6 = print(p6)
    return p6
