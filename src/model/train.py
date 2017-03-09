import pandas as pd
import numpy
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier


class TrainModel:

    columns = ['ID', 'Salary']

    def __init__(self, file):
        self.input = pd.read_excel(file)
        self.input.drop(self.input.columns[0], axis=1)
        self.input = self.input.iloc[numpy.random.permutation(len(self.input.index))]
        self.input.reset_index(drop=True)
        self.output = []
        self.mean_r_sqr = 0;
        self.mean_mae = 0;
        self.mean_mse = 0;


    def KFoldCrossValidation(self, column):
        folds = 10
        self.cv = cross_validation.KFold(len(self.input.index), n_folds=folds)
        for traincv, testcv in self.cv:
            self.train_data = self.input.iloc[traincv[0]:traincv[len(traincv)-1]]
            self.test_data = self.input.iloc[testcv[0]:testcv[len(testcv)-1]]
            self.trainModel(column)
            self.testForCVData()
            self.mean_r_sqr += self.r_sqr
            self.mean_mae += self.mae
            self.mean_mse += self.mse
        self.mean_r_sqr /= folds
        self.mean_mae /= folds
        self.mean_mse /= folds
        print("Score:", self.mean_r_sqr)
        print("Mean Absolute Error:", self.mean_mae)
        print("Mean Sqaured Error:", self.mean_mse)



    def prepareTrainingInputs(self, column):
        self.X_train = self.train_data.drop(self.columns, axis=1)
        self.y_train = self.train_data[column]
        self.X_train = self.X_train._get_numeric_data()
        self.X_test = self.test_data.drop(self.columns, axis=1)
        self.X_test = self.X_test._get_numeric_data()
        self.y_test = self.test_data[column]

    def trainModel(self, column):
        self.prepareTrainingInputs(column)
        #self.clf = LinearRegression()
        if (column=='Salary' or column == 'DOJ' or column == 'DOL'):
            self.clf = RandomForestRegressor(n_estimators = 100,n_jobs=2)
            print('Regressor')
        else:
            self.clf = RandomForestClassifier(n_estimators = 100,n_jobs=2)
            print('Classifier')
        self.clf = self.clf.fit(self.X_train, self.y_train)

    def testForCVData(self):
        self.r_sqr = self.clf.score(self.X_test, self.y_test)
        self.output = self.clf.predict(self.X_test)
        self.mae = mean_absolute_error(self.y_test, self.output)
        self.mse = mean_squared_error(self.y_test, self.output)

    def writeOutput(self, file_name):
        #Here before printing need to change it back to non-numerical data if needed.
        pd.DataFrame({'ID':self.test_input.ID,'':self.output}).to_excel(file_name,index=False)