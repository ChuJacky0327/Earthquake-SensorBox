import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib#save model
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from matplotlib.legend_handler import HandlerLine2D

datasets = pd.read_csv('pig_earthquake.csv')
X = datasets.iloc[:, [1,2,3]].values
Y = datasets.iloc[:, 4].values
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size = 0.3, random_state = 42, stratify=Y)

# Feature Scaling
'''
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_Train = sc_X.fit_transform(X_Train)
X_Test = sc_X.transform(X_Test)
'''
# Fitting the classifier into the Training set


classifier = RandomForestClassifier(n_estimators = 200, criterion = 'gini', random_state = 42)
classifier.fit(X_Train,Y_Train)

# Predicting the test set results

joblib.dump(classifier, 'pig_earthquake.model')
lr = joblib.load('pig_earthquake.model')
Predict = lr.predict(X_Test)
print(X_Test)
print('Predict : ', Predict)

# plot tree
'''
feature_names = ['X','Y','Z']
class_names = ['1','2','3','4','5','6','7']

fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (2,2), dpi=8000)
tree.plot_tree(classifier.estimators_[99],
               feature_names = feature_names, 
               class_names=class_names,
               filled = True);
fig.savefig('rf_individualtree.png')
print('treeimage_save')
'''
# plot tree


# plot learning curve
train_results = []
test_results = []
list_nb_trees = [1, 5, 10, 15, 30, 45, 60, 80, 100, 150, 200]

for nb_trees in list_nb_trees:
    classifier = RandomForestClassifier(n_estimators = nb_trees, criterion = 'gini', random_state = 42)
    classifier.fit(X_Train,Y_Train)

    train_results.append(mean_squared_error(Y_Train, classifier.predict(X_Train)))
    #test_results.append(mean_squared_error(Y_Test, classifier.predict(X_Test)))
    print("train score:", mean_squared_error(Y_Train, classifier.predict(X_Train)))
    #print("test score:",mean_squared_error(Y_Test, classifier.predict(X_Test)))

line1, = plt.plot(list_nb_trees, train_results, color="r", label="Training Score")
#line2, = plt.plot(list_nb_trees, test_results, color="g", label="Testing Score")

plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('MSE')
plt.xlabel('n_estimators')
plt.show()
# plot learning curve














