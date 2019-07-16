
# coding: utf-8

# In[29]:

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import csv


fields = ['Plan Name','Salesrep Name', 'Quota Amount Q1', 'Amount Attained Q1', 'Weighted TIC Q1', 'Amount Earned Q1','Quota Amount Q2', 'Amount Attained Q2', 'Weighted TIC Q2', 'Amount Earned Q2','Quota Amount Q3', 'Amount Attained Q3', 'Weighted TIC Q3', 'Amount Earned Q3','Quota Amount Q4', 'Amount Attained Q4', 'Weighted TIC Q4', 'Amount Earned Q4',  'Weighted TIC Yr','Amount Earned Yr','Quota Amount Yr','Amount Attained Yr','Component Label','Manager ID','Salesrep ID','Component Period']

gm = 'GM NAME'          #These are used to determine the appropriate quarter that we are in
gm_comp = 'SUBSYB1'             #primary component of the GM

df = pd.read_csv('EURearnings_sum.csv', thousands=',')
df = df[['Plan Name','Salesrep Name', 'Quota Amount Q1', 'Amount Attained Q1', 'Weighted TIC Q1', 'Amount Earned Q1','Quota Amount Q2', 'Amount Attained Q2', 'Weighted TIC Q2', 'Amount Earned Q2','Quota Amount Q3', 'Amount Attained Q3', 'Weighted TIC Q3', 'Amount Earned Q3','Quota Amount Q4', 'Amount Attained Q4', 'Weighted TIC Q4', 'Amount Earned Q4',  'Weighted TIC Yr','Amount Earned Yr','Quota Amount Yr','Amount Attained Yr','Component Label','Manager ID','Salesrep ID','Component Period']]
usd = pd.read_csv('USDearnings_sum.csv', thousands=',')
usd = usd[['Plan Name','Salesrep Name', 'Quota Amount Q1', 'Amount Attained Q1', 'Weighted TIC Q1', 'Amount Earned Q1','Quota Amount Q2', 'Amount Attained Q2', 'Weighted TIC Q2', 'Amount Earned Q2','Quota Amount Q3', 'Amount Attained Q3', 'Weighted TIC Q3', 'Amount Earned Q3','Quota Amount Q4', 'Amount Attained Q4', 'Weighted TIC Q4', 'Amount Earned Q4',  'Weighted TIC Yr','Amount Earned Yr','Quota Amount Yr','Amount Attained Yr','Component Label','Manager ID','Salesrep ID','Component Period']]

#the component label = notnull gets rid of some rows like "adjustments" or other non TIC related things

df['Currency'] = 'EUR'
df = df[df['Component Label'].notnull()]

usd['Currency'] = 'USD'
usd = usd[usd['Component Label'].notnull()]

df = df.append(usd)

df = df[~df['Component Label'].isin(['EPSBPE','EPGOLIVE','EPDISCP','EPDISC','EPSP','EPCCP','EPISV','EPSAP','TB3TRUEUP','BASERATE3','EPLINM1P','EPQADIST','EPLINM1','HURDLEEXP','HURDLESYB1','OYB1TRUEUP','EPPIPEL','EPPIPELP','BASERATE1', 'TB1TRUEUP', 'SYB1TRUEUP', 'BASERATE2', 'TB2TRUEUP', 'SYB2TRUEUP', 'EPLINM1+2', 'EPLINM1+2P', 'EPSRVC','BASERATE4','BASERATE3','HURDLEEXP','BASERATE2','EPAPP','EPCAG','EPCCSP','EPLINM1+2','EPLINM1+2P','EPPNT','EPQCB1','EPSRVC','Fixed','HURDLEEXP2','HURDLENACC','OCP1','OSP1','SUBSSYB','SVCSYB','SYB1TRUEUP','SYBHURDLE','TB1TRUEUP','TB2TRUEUP'
])]
df = df[df['Component Label'].notnull()]
#^the above remove the fields listed and any lines that have a blank in the component label field.




# In[30]:

#This cell turns the Dtype into float 64 for relevant columns
#df.to_csv('example.csv')

#df[['Quota Amount Q1', 'Amount Attained Q1', 'Weighted TIC Q1', 'Amount Earned Q1','Quota Amount Q2', 'Amount Attained Q2', 'Weighted TIC Q2', 'Amount Earned Q2','Quota Amount Q3', 'Amount Attained Q3', 'Weighted TIC Q3', 'Amount Earned Q3','Quota Amount Q4', 'Amount Attained Q4', 'Weighted TIC Q4', 'Amount Earned Q4',  'Weighted TIC Yr','Amount Earned Yr']]

df[['Quota Amount Q1', 'Amount Attained Q1', 'Weighted TIC Q1', 'Amount Earned Q1','Quota Amount Q2', 'Amount Attained Q2', 'Weighted TIC Q2', 'Amount Earned Q2','Quota Amount Q3', 'Amount Attained Q3', 'Weighted TIC Q3', 'Amount Earned Q3','Quota Amount Q4', 'Amount Attained Q4', 'Weighted TIC Q4', 'Amount Earned Q4',  'Weighted TIC Yr','Amount Earned Yr']] = df[['Quota Amount Q1', 'Amount Attained Q1', 'Weighted TIC Q1', 'Amount Earned Q1','Quota Amount Q2', 'Amount Attained Q2', 'Weighted TIC Q2', 'Amount Earned Q2','Quota Amount Q3', 'Amount Attained Q3', 'Weighted TIC Q3', 'Amount Earned Q3','Quota Amount Q4', 'Amount Attained Q4', 'Weighted TIC Q4', 'Amount Earned Q4',  'Weighted TIC Yr','Amount Earned Yr']].astype('float64')
#^the above fields pulled in as Objects due to a '1471.01-' value in column, converted to float64

df['Annual Attainment %'] = df['Amount Attained Yr'] / df['Quota Amount Yr']

df4 = df.copy()


# In[31]:

df.dtypes


# In[32]:

df.set_index('Salesrep Name', inplace=True)

df2 = df[df['Component Label'] == gm_comp]
q4_gm = df2.loc[gm].at['Amount Attained Q4']
q3_gm = df2.loc[gm].at['Amount Attained Q3']
q2_gm = df2.loc[gm].at['Amount Attained Q2']
q1_gm = df2.loc[gm].at['Amount Attained Q1']
#The below if statements decide what quarter to use and tells the subsequent code what columns based on the quarter

print(df.index)

if q4_gm > 0:
    df = df[['Currency','Plan Name','Component Period','Quota Amount Q4', 'Amount Attained Q4', 'Weighted TIC Q4', 'Amount Earned Q4',  'Weighted TIC Yr','Amount Earned Yr','Component Label','Manager ID','Salesrep ID','Annual Attainment %']]
    q_att = 'Amount Attained Q4'
    q_quota = 'Quota Amount Q4'
    qtic_earned = 'Amount Earned Q4'
    qtic = 'Weighted TIC Q4'  
    quarter = 'Q4'
elif q3_gm > 0:
    df = df[['Currency','Plan Name','Component Period','Quota Amount Q3', 'Amount Attained Q3', 'Weighted TIC Q3', 'Amount Earned Q3',  'Weighted TIC Yr','Amount Earned Yr','Component Label','Manager ID','Salesrep ID','Annual Attainment %']]
    q_att = 'Amount Attained Q3'
    q_quota = 'Quota Amount Q3'
    qtic_earned = 'Amount Earned Q3'
    qtic = 'Weighted TIC Q3' 
    quarter = 'Q3'
elif q2_gm > 0:
    df = df[['Currency','Plan Name','Component Period','Quota Amount Q2', 'Amount Attained Q2', 'Weighted TIC Q2', 'Amount Earned Q2', 'Weighted TIC Yr','Amount Earned Yr','Component Label','Manager ID','Salesrep ID','Annual Attainment %']]
    q_att = 'Amount Attained Q2'
    q_quota = 'Quota Amount Q2'
    qtic_earned = 'Amount Earned Q2'
    qtic = 'Weighted TIC Q2'  
    quarter = 'Q2'
elif q1_gm > 0:
    df = df[['Currency','Plan Name','Component Period','Quota Amount Q1', 'Amount Attained Q1', 'Weighted TIC Q1', 'Amount Earned Q1','Weighted TIC Yr','Amount Earned Yr','Component Label','Manager ID','Salesrep ID','Annual Attainment %']]
    q_att = 'Amount Attained Q1'
    q_quota = 'Quota Amount Q1'
    qtic_earned = 'Amount Earned Q1'
    qtic = 'Weighted TIC Q1'
    quarter = 'Q1'

    
df['Attainment %'] = df[q_att] / df[q_quota] 

df=df.sort_values(by=[q_att],ascending=False)

df.head(5)


# In[33]:

main_comp = df.loc[(df['Component Label'] == 'TB1') | (df['Component Label'] == 'SYB1') | (df['Component Label'] == 'REV1')]


main_comp = main_comp[[q_quota,q_att,'Attainment %','Amount Earned Yr','Component Label','Currency','Plan Name','Component Period','Annual Attainment %']]

main_comp = main_comp[main_comp['Amount Earned Yr']>0]
main_comp = main_comp[['Currency','Plan Name','Component Period','Component Label',q_quota,q_att,'Attainment %','Annual Attainment %']]



# In[34]:

tic = df[[qtic,qtic_earned,'Weighted TIC Yr','Amount Earned Yr','Manager ID']]

tic_temp = tic.groupby(level=0).sum()

tic = tic_temp.join(tic[['Manager ID']])

tic = tic[~tic.index.duplicated(keep='first')]

#####
tic['Quarterly Payout %'] = tic[qtic_earned] / tic[qtic]

tic['Annual Payout %'] = tic['Amount Earned Yr'] / tic['Weighted TIC Yr']


tic=tic.reset_index()



# In[35]:


df_mgr = df[['Manager ID','Salesrep ID']]
df_mgr = df_mgr.reset_index()
#just need manager Name in 
df_mgr = df_mgr.loc[:,('Manager ID')]
df_mgr = df_mgr.to_frame().reset_index()
df_mgr.columns = ['Salesrep Name', 'Salesrep ID']

df_mgr = df_mgr.merge(df4,on='Salesrep ID',how='left')
df_mgr = df_mgr[['Salesrep ID','Salesrep Name_y']]
df_mgr.columns = ['Manager ID', 'Manager Name']
df_mgr = df_mgr.set_index('Manager ID')
df_mgr = df_mgr[~df_mgr.index.duplicated(keep='first')].dropna()
df_mgr = df_mgr.reset_index()


# In[36]:

tic = tic.merge(df_mgr,on="Manager ID",how="left")
tic = tic.set_index('Salesrep Name')

tic = tic[~tic.index.duplicated(keep='first')]



# In[37]:

df3 = main_comp.join(tic)

df3 = df3.dropna(subset=['Attainment %'])

df3[" "]=""

df3 = df3[['Currency','Plan Name','Component Period','Component Label', q_quota, q_att,
       'Attainment %','Annual Attainment %'," ", qtic, qtic_earned,
       'Weighted TIC Yr', 'Amount Earned Yr','Quarterly Payout %', 'Annual Payout %','Manager Name']]
df3 = df3.reset_index()


# In[38]:

email = pd.read_csv('email.csv', encoding = "ISO-8859-1")
email = email[['Name','E-mail Address']]
email.rename(columns = {'Name':'Manager Name'}, inplace = True)


# In[39]:

df3 = df3.merge(email,on='Manager Name',how='left')
df3 = df3.set_index('Salesrep Name')
df3.rename(columns = {'E-mail Address':'Permissions',qtic:'TIC '+quarter,q_quota:'Quota '+quarter, q_att:'Attainment '+quarter,'Weighted TIC Yr':'Annual TIC','Amount Earned Yr':'Annual Amount Earned'}, inplace = True)
df3 = df3.sort_values(by=[qtic_earned],ascending=False)
df3 = df3.drop_duplicates()
df3.head(100)

df3 = df3.reset_index()




# In[40]:

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from gspread_dataframe import get_as_dataframe
from gspread_pandas import Spread
import sys,os,os.path
import csv
import certifi
import json

key_path = 'credentials.json'
json_key = json.load(open(key_path))


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
gc = gspread.authorize(credentials)

wks = gc.open("Current_Accruals").worksheet('sheet1')
wks.clear()
set_with_dataframe(wks, df3, include_column_header = True, include_index = False)


#wks.insert_row('',index=1)


