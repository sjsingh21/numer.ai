# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.grid_search import GridSearchCV as GS
from sklearn.metrics import accuracy_score, log_loss

training_data = pd.read_csv('../datasets/numerai_training_data.csv')
tournament_data = pd.read_csv('../datasets/numerai_tournament_data.csv')

# splitting my arrays in ratio of 30:70 percent
features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(training_data.iloc[:,0:21], training_data['target'], test_size=0.3, random_state=0)

# parameters
parameters = {
        'n_estimators': [ 20,25 ],
        'random_state': [ 0 ],
        'max_features': [ 2 ],
        'min_samples_leaf': [150,200,250]
}

# implementing my classifier
model = RFC()
grid = GS(estimator=model, param_grid=parameters)
grid.fit(features_train, labels_train)

# Calculate the logloss of the model
prob_predictions_class_test = grid.predict(features_test)
prob_predictions_test = grid.predict_proba(features_test)

logloss = log_loss(labels_test,prob_predictions_test)

accuracy = accuracy_score(labels_test, prob_predictions_class_test, normalize=True,sample_weight=None)

# predict class probabilities for the tourney set
prob_predictions_tourney = grid.predict_proba(tournament_data.iloc[:,1:22])

# extract the probability of being in a class 1
probability_class_of_one = np.array([x[1] for x in prob_predictions_tourney[:]]) # List comprehension

t_id = tournament_data['t_id']

np.savetxt(
    '../probability.csv',          # file name
    probability_class_of_one,  # array to savela
    fmt='%.2f',               # formatting, 2 digits in this case
    delimiter=',',          # column delimiter
    newline='\n',           # new line character
    header= 'probability')   # file header

np.savetxt(
    '../t_id.csv',          # file name
    t_id,                   # array to save
    fmt='%.d',              # formatting, 2 digits in this case
    delimiter=',',          # column delimiter
    newline='\n',           # new line character
    header= 't_id')   # file header
