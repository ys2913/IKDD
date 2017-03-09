import pandas as pd
import openpyxl
import sklearn
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np

class DataProcess:

    columns = ['Designation', 'JobCity', 'Specialization', '10board', '12board', 'Gender', 'Degree', 'CollegeState']
    columns_test = ['Specialization', '10board', '12board', 'Gender', 'Degree', 'CollegeState']

    def __init__(self):
        self.designation_map = {}
        self.jobcity_map = {}
        self.spec_map = {}
        self.board10_map = {}
        self.board12_map = {}
        self.gender_map = {}
        self.degree_map = {}
        self.collegestate_map = {}


    def ProcessTrainInput(self, filename):
        train= pd.read_excel(filename)
        result = train.copy()

        train.rename(columns={'10board': 'board10', '12board': 'board12'}, inplace=True)

        d1=self.getdays(train.DOJ,train.DOL,'Days_DOL')
        d2=self.getdays(train.DOB,train.DOJ,'Days_DOJ')
        d3=self.preprocessDesignation(train.Designation, 'designation_comp_ID_PP')
        d4=self.preprocessSpec(train.Designation, 'specialization_ID_PP')
        d5=self.convert(self.board10_map, train.board10, 'board10_ID_PP')
        d6=self.convert(self.board12_map, train.board12, 'board12_ID_PP')
        d7=self.convert(self.jobcity_map, train.JobCity, 'JobCity_ID_PP')
        d8=self.convert(self.gender_map, train.Gender, 'Gender_ID_PP')
        d9=self.convert(self.degree_map, train.Degree, 'Degree_ID_PP')
        d10=self.convert(self.collegestate_map, train.CollegeState, 'CollegeState_ID_PP')

        result['Days_DOL_PP'] = d1.values
        result['Days_DOJ_PP'] = d2.values
        result['designation_comp_ID_PP'] = d3.values
        result['specialization_ID_PP'] = d4.values
        result['board10_ID_PP'] = d5.values
        result['board12_ID_PP'] = d6.values
        result['JobCity_ID_PP'] = d7.values
        result['Gender_ID_PP'] = d8.values
        result['Degree_ID_PP'] = d9.values
        result['CollegeState_ID_PP'] = d10.values

        result.drop(self.columns, axis=1)

        return result;


    def ProcessTestInput(self, filename):
        train= pd.read_excel(filename)
        result = train.copy()

        train.rename(columns={'10board': 'board10', '12board': 'board12'}, inplace=True)

        d5=self.convert(self.board10_map, train.board10, 'board10_ID_PP')
        d6=self.convert(self.board12_map, train.board12, 'board12_ID_PP')
        d7=self.convert(self.jobcity_map, train.JobCity, 'JobCity_ID_PP')
        d8=self.convert(self.gender_map, train.Gender, 'Gender_ID_PP')
        d9=self.convert(self.degree_map, train.Degree, 'Degree_ID_PP')
        d10=self.convert(self.collegestate_map, train.CollegeState, 'CollegeState_ID_PP')

        result['board10_ID_PP'] = d5.values
        result['board12_ID_PP'] = d6.values
        result['JobCity_ID_PP'] = d7.values
        result['Gender_ID_PP'] = d8.values
        result['Degree_ID_PP'] = d9.values
        result['CollegeState_ID_PP'] = d10.values

        result.drop(self.columns_test, axis=1)

        return result;


    def getyearmonthinfo(self, data):
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

    def getyearinfo(self, data):
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

    def getmonthinfo(self, data):
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

    def getweekinfo(self, data):
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

    def getdayofweekinfo(self, data):
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

    def getdays(self, data1,data2,str):
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

    def getDesignation(self, jobs, key):
        value=0
        #print(key)
        if(key in jobs['CompSc_Back']):
            value='CompSc_Back';
        elif(key in jobs['CompSc_Front']):
            value='CompSc_Front';
        elif(key in jobs['Analyst']):
            value='Analyst';
        elif(key in jobs['Management']):
            value='Management';
        elif(key in jobs['Consultant']):
            value='Consultant';
        elif(key in jobs['Academics']):
            value='Academics';
        elif(key in jobs['Engineers']):
            value='Engineers';
        elif(key in jobs['Sales']):
            value='Sales';
        elif(key in jobs['Others']):
            value='Others';

        #print(value)
        return value;


    def preprocessDesignation(self, data, str):
        jobs={
        'CompSc_Back':['sharepoint developer','senior java developer',
                   'sr. database engineer','dba',
                   'dotnet developer','website developer/tester',
                   'embedded software engineer',
                   'web intern','javascript developer',
                   'web developer','gis/cad engineer',
                   'junior .net developer','web designer and seo',
                   'design engineer','html developer',
                   'senior .net developer',
                   'php developer','c# developer',
                   'oracle dba','full stack developer',
                   'senior php developer','cloud engineer',
                   'ruby on rails developer','seo',
                   'sql dba','database developer',
                   'python developer','linux systems administrator',
                   'db2 dba','teradata dba','teradata developer',
                   '.net developer','.net web developer','database administrator',
                   'systems administrator','sql developer',
                   'seo engineer','seo trainee','cad designer',
                   'cad drafter','etl developer',
                   'asp.net developer'],
        'CompSc_Front':['web application developer',
                        'senior software engineer',
                        'assistant programmer',
                        'software developer','trainee software developer',
                        'software test engineer','application developer',
                        'principal software engineer','software eng',
                        'data scientist','jr. software developer',
                        'technology lead','software engineering associate',
                        'front end developer','enterprise solutions developer',
                        'systems engineer','software development engineer',
                        'associate developer','it engineer','software programmer',
                        'java software engineer',
                        'software quality assurance tester',
                        'mobile application developer',
                        'senior software developer',
                        'system administrator',
                        'software tester',
                        'programmer',
                        'junior software developer',
                        'lead engineer',
                        'assistant system engineer - trainee',
                        'software engineer associate',
                        'software architect',
                        'senior developer',
                        'associate software engg',
                        'assistant system engineer','product engineer',
                        'firmware engineer',
                        'windows systems administrator',
                        'software executive',
                        'ui developer',
                        'it developer',
                        'android developer',
                        'trainee software engineer',
                        'delivery software engineer',
                        'network engineer',
                        'ase','desktop support technician',
                        'ios developer',
                        'senior network engineer',
                        'cnc programmer',
                        'software quality assurance analyst',
                        'embedded engineer',
                        'front end web developer','software trainee engineer',
                        'associate software engineer',
                        'information technology specialist',
                        'web designer',
                        'software test engineerte',
                        'software engineer',
                        'qa engineer',
                        'network support engineer',
                        'senior programmer','software engineere',
                        'programmer analyst trainee','network security engineer',
                        'software engg',
                        'technical lead',
                        'senior web developer',
                        'jr. software engineer','developer',
                        'associate software developer',
                        'team leader','software devloper',
                        'software enginner','team lead',
                        'it support specialist','java trainee',
                        'it assistant','software trainee','assistant software engineer',
                        'ux designer',
                        'senior test engineer',
                        'software designer','software engineer trainee',
                        'java developer',
                        'project engineer','senior engineer','senior design engineer',
                        'desktop support engineer',
                        'web designer and joomla administrator',
                        'it technician',
                        'it operations associate',
                        'it executive',
                        'software test engineer (etl)','sap consultant',
                        'trainee decision scientist',
                        'admin assistant',
                        'senior project engineer','assistant administrator',
                        'associate engineer',
                        'junior software engineer',
                        'technical support engineer',
                        'assistant systems engineer',
                        'network administrator',
                        'assistant system engineer trainee',
                        'product developer',
                        'senior systems engineer','game developer'],
        'Analyst':['business technology analyst','supply chain analyst',
                   'research analyst','technology analyst','mis executive',
                   'qa analyst','technical analyst','senior business analyst',
                   'system engineer trainee','business analyst',
                   'data analyst','portfolio analyst','operations assistant',
                   'quality analyst','financial analyst','business analyst consultant',
                   'help desk analyst','information security analyst',
                   'it analyst','software analyst','junior system analyst',
                   'sap analyst','business process analyst','associate qa',
                   'program analyst trainee','sap mm consultant','programmer analyst',
                   'business systems analyst','human resources analyst',
                   'it business analyst','system analyst','seo analyst',
                   'software engineer analyst','operations analyst',
                   'marketing analyst','business intelligence analyst',
                   'digital marketing specialist','systems analyst',
                   'quality assurance analyst','technical operations analyst',
                   'desktop support analyst','qa trainee','business system analyst'],
        'Management':['management trainee','human resources associate','graphic designer',
                      'corporate recruiter','operations executive',
                      'program manager','branch manager','hr recruiter',
                      'hr generalist','associate technical operations',
                      'executive assistant','operations engineer',
                      'project management officer','recruitment coordinator',
                      'sales manager','executive administrative assistant',
                      'service manager','asst. manager','assistant manager',
                      'hr assistant','logistics executive',
                      'field business development associate','operational excellence manager',
                      'operations','field based employee relations manager',
                      'project manager','business development executive',
                      'business development manager','engineering manager',
                      'human resource assistant','account manager',
                      'junior recruiter','business office manager',
                      'operation executive','operational executive','hr manager',
                      'office coordinator','process associate','executive recruiter',
                      'technical recruiter','general manager','manager',
                      'it recruiter','project coordinator','associate manager',
                      'junior manager','associate system engineer',
                      'sales development manager','staffing recruiter','recruitment associate',
                      'hr executive','account executive','recruiter','product manager',
                      'marketing manager','process executive','marketing executive',
                      'online marketing manager','operations engineer and jetty handling',
                      'business development managerde','marketing coordinator',
                      'site manager','project administrator',
                      'customer service manager','human resources intern',
                      'executive hr','assistant store manager',
                      'entry level management trainee','administrative coordinator'],
        'Consultant':['financial service consultant','risk investigator',
                      'seo executive','business consultant','sap abap consultant',
                      'client services associate','sap functional consultant',
                      'talent acquisition specialist','process advisor',
                      'quality controller','administrative support',
                      'technical support specialist','risk consultant',
                      'technical consultant','business systems consultant'],
        'Academics':['co faculty','assistant professor','visiting faculty',
                     'research associate','faculty','graduate apprentice trainee',
                     'senior research fellow','training specialist',
                     'computer faculty','junior research fellow',
                     'lecturer & electrical maintenance',
                     'research staff member','educator','technical assistant',
                     'project assistant','professor','lecturer',
                     'senior risk consultant','sap abap associate consultant',
                     'research scientist'],
        'Engineers':['environmental engineer','telecommunication engineer',
                     'planning engineer','test technician','engineer-hws',
                     'graduate trainee engineer','manual tester','trainee engineer',
                     'maintenance engineer','graduate engineer trainee',
                     'system engineer','operations manager','bss engineer',
                     'field engineer','application engineer','assistant engineer',
                     'quality control engineer','electrical design engineer',
                     'engineer','rf engineer','noc engineer','junior engineer',
                     'process engineer','continuous improvement engineer',
                     'telecom support engineer','civil engineer',
                     'engineering technician','graduate engineer',
                     'assistant electrical engineer','support engineer',
                     'engineer trainee','executive engineer','dcs engineer',
                     'rf/dt engineer','r&d engineer','associate test engineer',
                     'engineer- customer support',
                     'electrical project engineer','industrial engineer',
                     'executive engg','electrical engineer',
                     'senior mechanical engineer',
                     'electronic field service engineer','site engineer',
                     'product development engineer','electrical designer',
                     'mechanical engineer','shift engineer',
                     'process control engineer','test engineer',
                     'operation engineer','research engineer',
                     'quality assurance test engineer','performance engineer',
                     'automation engineer','field service engineer',
                     'electrical field engineer','telecom engineer',
                     'mechanical design engineer','hardware engineer',
                     'manufacturing engineer','electrical controls engineer',
                     'sr. engineer','product design engineer',
                     'technical engineer','implementation engineer',
                     'controls engineer','testing engineer','production engineer',
                     'service engineer'],
        'Sales':['sales account manager','sales executive',
                 'service and sales engineer','territory sales manager',
                 'sales trainer','sales associate',
                 'sales management trainee','sales and service engineer',
                 'sales coordinator','sales support',
                 'entry level sales and marketing','salesforce developer',
                 'sales & service engineer','sales engineer','senior sales executive',
                 'marketing assistant'],
        'Others':['editor','clerical','technical writer',
                  'maintenance supervisor','technical support executive',
                  'designer','aircraft technician','documentation specialist',
                  'r & d','quality control inspector',
                  'quality assurance auditor','full-time loss prevention associate',
                  'quality assurance tester','clerical assistant',
                  'secretary','senior quality assurance engineer',
                  'senior quality engineer','quality assurance automation engineer',
                  'data entry operator','customer service',
                  'service coordinator','catalog associate',
                  'quality assurance engineer','quality consultant',
                  'help desk technician','junior engineer product support',
                  'phone banking officer','quality associate',
                  'quality control inspection technician','get','quality assurance',
                  'customer support engineer','customer care executive',
                  'apprentice','quality engineer','customer service representative']}
        #print(jobs['CompSc_Back'])
        output=pd.DataFrame()

        for row in data.items():
            key=row[1]
            value=self.getDesignation(jobs,key)
            temp=pd.DataFrame({str:[value]})
            output=output.append(temp)

        output = self.convert(self.designation_map, output[str], str)
        return output;

    def getSpec(self, jobs, key):
        value=0
        #print(key)
        if(key in jobs['CompSc']):
            value='CompSc';
        elif(key in jobs['Instrumentation']):
            value='Instrumentation';
        elif(key in jobs['Electrical']):
            value='Electrical';
        elif(key in jobs['Other']):
            value='Other';
        elif(key in jobs['Mechanical']):
            value='Mechanical';
        #print(value)
        return value;

    def preprocessSpec(self, data, str):
        spec={
        'CompSc':['information technology',
		'computer application',
		'information science',
		'information & communication technology',
		'computer engineering',
		'information science engineering',
		'computer science & engineering',
		'computer and communication engineering',
		'computer science',
		'computer science and technology',
		'computer networking',
		'embedded systems technology'],
        'Electrical':[
		'electronics and electrical engineering',
		'electronics',
		'electronics and computer engineering',
		'electronics and communication engineering',
		'electrical engineering',
		'electronics & telecommunications',
		'telecommunication engineering',
		'electronics engineering',
		'electrical and power engineering'
		],
		'Instrumentation':[
		'applied electronics and instrumentation',
		'instrumentation and control engineering',
		'control and instrumentation engineering',
		'instrumentation engineering',
		'electronics and instrumentation engineering',
		'electronics & instrumentation eng',
		],
        'Other':[
		'power systems and automation',
		'ceramic engineering',
		'civil engineering',
		'metallurgical engineering',
		'biomedical engineering',
		'industrial & management engineering',
		'other',
		'polymer technology',
		'chemical engineering',
		'biotechnology',
		],
        'Mechanical':[
		'mechanical and automation',
		'industrial engineering',
		'automobile/automotive engineering',
		'mechatronics',
		'industrial & production engineering',
		'mechanical & production engineering',
		'mechanical engineering',
		'internal combustion engine',
		'aeronautical engineering'
		]}

        output=pd.DataFrame()

        for row in data.items():
            key=row[1]
            value=self.getSpec(spec,key)
            temp=pd.DataFrame({str:[value]})
            output=output.append(temp)

        output = self.convert(self.spec_map, output[str], str)
        return output;

    def convert(self, maps, data, str):
        itr=1
        value=1
        output=pd.DataFrame()

        for row in data.items():
            key=row[1]
            if(key in maps):
                value=maps[key]
            else:
                maps[key]=itr
                value=itr
                itr=itr+1
            temp=pd.DataFrame({str:[value]})
            output=output.append(temp)
        return output;

#x = DataProcess('../../data/train.xlsx')
#y = x.getNewValues()