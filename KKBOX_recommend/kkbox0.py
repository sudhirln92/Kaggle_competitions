#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:42:57 2017
@author: sudhir
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split,KFold
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
seed = 23

#Load data set
train = pd.read_csv('train.csv',dtype=({'msno':'category','song_id':'category', 'source_system_tab':'category',
                                        'source_screen_name':'category','source_type':'category','target':'category'}))
test = pd.read_csv('test.csv',dtype=({'msno':'category','song_id':'category', 'source_system_tab':'category',
                                        'source_screen_name':'category','source_type':'category'}))
members = pd.read_csv('members.csv',parse_dates=['registration_init_time','expiration_date'],
                      dtype=({'msno':'category','gender':'category'}))
songs = pd.read_csv('songs.csv',dtype=({'song_id':'category','genre_ids':'category','artist_name':'category',
                                        'composer':'category','lyricist':'category','language':'category'}))

#Data exploration
train.head()
test.head()
members.head()
songs.head()
train.info()
members.info()
test.info()
songs.info()
print('Number of rows and columns in train:',train.shape[0])
print('Number of rows and columns in test:',test.shape[0])
print('Number of rows and columns in members:',members.shape[0])
print('Number of rows and columns in songs',songs.shape[0])

df_train = train.merge(members,how='left',on='msno')
df_test = test.merge(members,how='left',on='msno')
df_train = df_train.merge(songs,how='left',on='song_id')
df_test = df_test.merge(songs, how='left',on='song_id')
df_train.head(3).T
df_train.info()

del train,test,members,songs
df_train.describe().T
# Missing value in data set
df_train.isnull().sum()
df_test.isnull().sum()
cat = ['source_system_tab','source_screen_name','source_type', 'gender',
       'genre_ids','artist_name','composer','lyricist','song_length','language']

def missing(df,var):
    for i in var:
        df[i].fillna(df[i].mode()[0], inplace=True)

missing(df_train,cat)
missing(df_test,cat)

# Univariate analysis
df_train['target'].nunique()
plt.figure(figsize=(12,10))
sns.countplot(df_train['target'])
plt.xlabel('Target')

df_train['msno'].nunique()
k = df_train['msno'].value_counts()
k
k[k==1].count()
plt.figure(figsize=(12,10))
sns.distplot(k)
plt.xlabel('')

df_train['song_id'].nunique()
df_train['song_id'].unique()
df_train.groupby(['song_id']).count()['msno']

k = df_train['song_id'].value_counts()
k
k[k==1].sum()
plt.figure(figsize=(12,10))
sns.distplot(k[k>1000])
plt.xlabel('')


df_train['source_system_tab'].nunique()
df_train['source_screen_name'].nunique()
df_train['source_type'].nunique()
df_train['target'].nunique()
df_train['city'].nunique()
df_train['bd'].nunique()
df_train['gender'].nunique()
df_train['registered_via'].nunique()
df_train['genre_ids'].nunique()
df_train['artist_name'].nunique()
df_train['composer'].nunique()
df_train['lyricist'].nunique()
df_train['language'].nunique()
sns.countplot(df_train['language'])
plt.yscale('log')

# Date time feature
def date_feature(df):
    var = ['registration_init_time','expiration_date']
    k = ['reg','exp']
    df['sub_duration'] = (df[var[1]] - df[var[0]]).dt.days
    for i ,j in zip(var,k):
        df[j+'_day'] = df[i].dt.day
        df[j+'_weekday'] = df[i].dt.weekday
        df[j+'_week'] = df[i].dt.week
        df[j+'_month'] = df[i].dt.month
        df[j+'_year'] =df[i].dt.year

date_feature(df_train)
date_feature(df_test)

sns.countplot(df_train['exp_year'])
sns.heatmap( df_train.loc[0:10000,:].corr())
# Preprocessing 
df_train.columns
le = LabelEncoder()
cat = ['msno', 'song_id', 'source_system_tab', 'source_screen_name',
       'source_type','gender','genre_ids','artist_name','composer',
       'lyricist']
 1a
 9 y678bel(df,var):
    for i in var:
        df[i]= le.fit_transform(df[i])

label(df_train,cat)
label(df_test,cat)

df_train.head(2).T

#split data set 
X = df_train.drop(['target','registration_init_time', 'expiration_date'],axis=1)
y = df_train['target']
x_test = df_test.drop(['id','registration_init_time', 'expiration_date'],axis=1)

xtr,xvl,ytr,yvl = train_test_split(X,y,test_size=0.3,random_state=None)
del X, y

#Model
lr = LogisticRegression(max_iter=100,random_state=seed)
lr.fit(xtr,ytr)
pred = lr.predict(xvl)

# accuracy
confusion_matrix(yvl,pred)

#Rf
rf = RandomForestClassifier(max_depth=7,n_estimators=200,)
rf.fit(xtr,ytr)
rf_pred = rf.predict(xvl)
print(rf.feature_importances_)
rf.score(xvl,yvl)

#Accuracy
confusion_matrix(yvl,rf_pred)

#Submission result
y_pred = rf.predict(x_test)
submit = pd.DataFrame({'id':df_test['id'],'target':y_pred})
submit.to_csv('kk_target.csv',index=False)