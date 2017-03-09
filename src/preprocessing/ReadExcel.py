import pandas as pd
import sklearn
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np


def getvalues():
      train= pd.read_excel('train.xlsx')
      dob=train.DOB
      b1=train.board10
      b2=train.board12
      degree=train.Degree
      spec=train.Specialization
      state=train.CollegeState

      d1=convert(dob,'age',True)
      d2=convert(b1,'board10',False)
      #d3=convert(b2,'board12',False)
      #d4=convert(degree,'degree',False)
      #d5=convert(spec,'specialization',False)
      #d6=convert(state,'state',False)

      result=pd.concat([d1,d2],axis=1)
      print(result)
      return result;


def convert(data,str,isdate):
      maps={}
      itr=1
      value=1
      output=pd.DataFrame()

      for row in data.iteritems():
            key=row[1]
            if(isdate):
                  year=key.year
                  value=2016-year
            else:
                  if(key in maps):
                        value=maps[key]
                  else:
                        maps[key]=itr
                        value=itr
                        itr=itr+1
            temp=pd.DataFrame({str:[value]})
            output=output.append(temp)
      return output;


getvalues()