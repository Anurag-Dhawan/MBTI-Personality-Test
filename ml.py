import numpy as np 
import pandas as pd 
import pickle
from joblib import dump
import joblib
import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV, StratifiedKFold
from xgboost import XGBClassifier,plot_importance
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.feature_selection import SelectFromModel
from itertools import compress

import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\HP\OneDrive\Desktop\VI Pro\mbti_1.csv')
df.head()
df['seperated_post'] = df['posts'].apply(lambda x: x.strip().split("|||"))
df['num_post'] = df['seperated_post'].apply(lambda x: len(x))
df.head()
df['id'] = df.index
df.head()
expanded_df = pd.DataFrame(df['seperated_post'].tolist(), index=df['id']).stack().reset_index(level=1, drop=True).reset_index(name='idposts')
expanded_df=expanded_df.join(df.set_index('id'), on='id', how = 'left')
expanded_df=expanded_df.drop(columns=['posts','seperated_post','num_post'])
def clean_text(text):
    result = re.sub(r'http[^\s]*', '',text)
    result = re.sub('[0-9]+','', result).lower()
    result = re.sub('@[a-z0-9]+', 'user', result)
    return re.sub('[%s]*' % string.punctuation, '',result)

final_df = expanded_df.copy()
final_df['idposts'] = final_df['idposts'].apply(clean_text)
cleaned_df = final_df.groupby('id')['idposts'].apply(list).reset_index()
df['clean_post'] = cleaned_df['idposts'].apply(lambda x: ' '.join(x))
vectorizer = CountVectorizer(stop_words = ['and','the','to','of',
                                           'infj','entp','intp','intj',
                                           'entj','enfj','infp','enfp',
                                           'isfp','istp','isfj','istj',
                                           'estp','esfp','estj','esfj',
                                           'infjs','entps','intps','intjs',
                                           'entjs','enfjs','infps','enfps',
                                           'isfps','istps','isfjs','istjs',
                                           'estps','esfps','estjs','esfjs'],
                            max_features=1500,
                            analyzer="word",
                            max_df=0.8,
                            min_df=0.1)
corpus = df['clean_post'].values.reshape(1,-1).tolist()[0]
vectorizer.fit(corpus)
X_cnt = vectorizer.fit_transform(corpus)
tfizer = TfidfTransformer()
tfizer.fit(X_cnt)
X = tfizer.fit_transform(X_cnt).toarray()
joblib.dump(tfizer,"tfizer.dat")
all_words = vectorizer.get_feature_names()
joblib.dump(all_words,"all_words.dat")
n_words = len(all_words)
df['fav_world'] = df['type'].apply(lambda x: 1 if x[0] == 'E' else 0)
df['info'] = df['type'].apply(lambda x: 1 if x[1] == 'S' else 0)
df['decision'] = df['type'].apply(lambda x: 1 if x[2] == 'T' else 0)
df['structure'] = df['type'].apply(lambda x: 1 if x[3] == 'J' else 0)
X_df = pd.DataFrame.from_dict({w: X[:, i] for i, w in enumerate(all_words)})
def sub_classifier(keyword):
    y_f = df[keyword].values
    X_f_train, X_f_test, y_f_train, y_f_test = train_test_split(X_df, y_f, stratify=y_f)
    f_classifier = XGBClassifier()
    print(">>> Train classifier ... ")
    f_classifier.fit(X_f_train, y_f_train, 
                     early_stopping_rounds = 10, 
                     eval_metric="logloss", 
                     eval_set=[(X_f_test, y_f_test)], verbose=False)
    print(">>> Finish training")
    print("%s:" % keyword, sum(y_f)/len(y_f))
    print("Accuracy %s" % keyword, accuracy_score(y_f_test, f_classifier.predict(X_f_test)))
    print("AUC %s" % keyword, roc_auc_score(y_f_test, f_classifier.predict_proba(X_f_test)[:,1]))
    return f_classifier

fav_classifier = sub_classifier('fav_world')
info_classifier = sub_classifier('info')
decision_classifier = sub_classifier('decision')
str_classifier = sub_classifier('structure')

#fav_classifier.save('fav_classifier.h5')
#info_classifier.save('info_classifier.h5')
#decision_classifier.save('decision_classifier.h5')
#str_classifier.save('str_classifier.h5')
#filename = 'fav_classifier.dat'
joblib.dump(vectorizer,"vectorizer.dat")
joblib.dump(fav_classifier,"fav_classifier.dat")
joblib.dump(info_classifier,"info_classifier.dat")
joblib.dump(decision_classifier,"decision_classifier.dat")
joblib.dump(str_classifier,"str_classifier.dat")