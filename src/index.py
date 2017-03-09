import pandas as pd
import numpy
from model.train import TrainModel
from preprocessing.DataProcessing import DataProcess



#Preprocesssing Part

input_file = '../data/train_old.xlsx'
processed_file = '../data/train2.xlsx'
'''
d = DataProcess()

result = d.ProcessTrainInput(input_file)

writer = pd.ExcelWriter(processed_file)
result.to_excel(writer,'Sheet1')
writer.save()
'''

#Training Part

x = TrainModel(processed_file)
x.KFoldCrossValidation('Salary')