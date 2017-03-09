import pandas as pd
import openpyxl
import sklearn
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np

def getvalues():
    train= pd.read_excel('train.xlsx')
    dob=train.DOB
    doj=train.DOJ
    dol=train.DOL
    d1=getdays(doj,dol,'Days_DOL')
    d2=getdays(dob,doj,'Days_DOJ')
    result=pd.concat([d1,d2],axis=1)
    writer = pd.ExcelWriter('pandas_simple.xlsx')
    result.to_excel(writer,'Sheet1')
    #df2.to_excel(writer,'Sheet2')
    writer.save()

    return;


def getyearmonthinfo(data):
    maps={}
    itr=1
    value=1
    output=pd.DataFrame()
    str='YearMonth'
    for row in data.iteritems():
        key=row[1]
        year=key.year
        month=key.month
        value=year*100+month
        print(value)
        temp=pd.DataFrame({str:[value]})
        output=output.append(temp)
    return output;


def getyearinfo(data):
    maps={}
    itr=1
    value=1
    output=pd.DataFrame()
    str='Year'
    for row in data.iteritems():
        key=row[1]
        year=key.year
        value=year
        #print(value)
        temp=pd.DataFrame({str:[value]})
        output=output.append(temp)
    return output;

def getmonthinfo(data):
    maps={}
    itr=1
    value=1
    output=pd.DataFrame()
    str='Month'
    for row in data.iteritems():
        key=row[1]
        month=key.month
        value=month
        #print(value)
        temp=pd.DataFrame({str:[value]})
        output=output.append(temp)
    return output;

def getweekinfo(data):
    maps={}
    itr=1
    value=1
    output=pd.DataFrame()
    str='Week'
    for row in data.iteritems():
        key=row[1]
        week=key.isocalendar()[1]
        value=week
        #print(value)
        temp=pd.DataFrame({str:[value]})
        output=output.append(temp)
    return output;

def getdayofweekinfo(data):
    maps={}
    itr=1
    value=1
    output=pd.DataFrame()
    str='Week'
    for row in data.iteritems():
        key=row[1]
        dayweek=key.isoweekday()
        value=dayweek
        #print(value)
        temp=pd.DataFrame({str:[value]})
        output=output.append(temp)
    return output;

def getdays(data1,data2,str):
    maps={}
    itr=1
    value=1
    data=pd.concat([data1,data2],axis=1)
    output=pd.DataFrame()
    for row in data.iterrows():
        d1=row[1][0]
        d2=row[1][1]
        if(d2=='present'):
            days='present'
        else:
            days=(d2-d1).days
        value=days
        #print(value)
        temp=pd.DataFrame({str:[value]})
        output=output.append(temp)
    return output;

getvalues();