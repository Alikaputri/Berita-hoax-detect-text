# -*- coding: utf-8 -*-
"""klasifikasiskripsi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tTuGPUcNWs1bQcqD3lAWCrt6A05FxO0A
"""

import numpy as np
import pandas as pd
from google.colab import drive


drive.mount('/content/drive')

df=pd.read_csv('/content/drive/My Drive/coba skripsi/stemmingnew.csv')
df

'''labels=df.label
labels.head()'''

"""TF-IDF"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(df['narasistem'], df['label'], test_size=0.2, random_state=7)

df_train = pd.DataFrame()
df_train['narasistem'] = x_train
df_train['label'] = y_train

df_test= pd.DataFrame()
df_test['narasistem'] = x_test
df_test['label'] = y_test

df_train

df_test

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# tfidf vectorizer
tfidf=TfidfVectorizer()
tfidf.fit(df['narasistem'].values.astype('U'))
x_train_tfidf = tfidf.transform(df_train['narasistem'].values.astype('U'))
x_test_tfidf = tfidf.transform(df_test['narasistem'].values.astype('U'))

df_train.to_csv('datatrain.csv', index=False)
df_train.to_csv('datatest.csv', index=False)

tfidf

print(x_train_tfidf)

print(x_test_tfidf)

print(x_train_tfidf.shape)
print(x_test_tfidf.shape)

print(tfidf.vocabulary_)

"""SVM"""

from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn import metrics


SVM = SVC(kernel='linear')
SVM.fit(x_train_tfidf,y_train)

"""Data Test SVM"""

from sklearn.metrics import accuracy_score

predictions_SVM = SVM.predict(x_test_tfidf)
test_prediction = pd.DataFrame()
test_prediction['narasistem'] = x_test
test_prediction['label'] = predictions_SVM
model1 = metrics.accuracy_score(y_test, predictions_SVM)
print("The Accuracy is",str('{:04.2f}'.format(model1*100))+'%')

from sklearn.metrics import confusion_matrix
matrix= confusion_matrix(y_test, predictions_SVM)
print(matrix)

import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(matrix, square= True, annot= True, cbar= False, cmap='RdBu', xticklabels=['Real','Hoax'], yticklabels= ['Real','Hoax'], fmt= 'g')
plt.xlabel('prediksi label')
plt.ylabel('true label')

from sklearn.metrics import classification_report

print ("The classification report is:") 
print (classification_report(y_test, predictions_SVM))

test_prediction

test_prediction.to_csv('testpredict.csv', index=False)

"""Data Train SVM"""

from sklearn.metrics import accuracy_score

predictions_SVM1 = SVM.predict(x_train_tfidf)
train_prediction1 = pd.DataFrame()
train_prediction1['narasistem'] = x_train
train_prediction1['label'] = predictions_SVM1
model2 = metrics.accuracy_score(y_train, predictions_SVM1)
print("The Accuracy is",str('{:04.2f}'.format(model2*100))+'%')

from sklearn.metrics import confusion_matrix
matrix= confusion_matrix(y_train, predictions_SVM1)
print(matrix)

import seaborn as sns
sns.heatmap(matrix, square= True, annot= True, cbar= False, cmap='RdBu', xticklabels=['Real','Hoax'], yticklabels= ['Real','Hoax'], fmt= 'g')
plt.xlabel('prediksi label')
plt.ylabel('true label')

from sklearn.metrics import classification_report

print ("The classification report is:") 
print (classification_report(y_train, predictions_SVM1))

train_prediction1

train_prediction1.to_csv('testpredict.csv', index=False)

"""Random Forest"""

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier()
clf.fit(x_train_tfidf, y_train)

from sklearn import metrics
pred_result = clf.predict(x_test_tfidf)
model = metrics.accuracy_score(y_test, pred_result)
print("The Accuracy is",str('{:04.2f}'.format(model*100))+'%')

from sklearn.metrics import confusion_matrix
matrix1= confusion_matrix(y_test, pred_result)
print(matrix1)

import seaborn as sns
sns.heatmap(matrix1, square= True, annot= True, cbar= False, cmap='RdBu', xticklabels=['Real','Hoax'], yticklabels= ['Real','Hoax'], fmt= 'g')
plt.xlabel('prediksi label')
plt.ylabel('true label')

from sklearn.metrics import classification_report
print("The classification report is:")
print(classification_report(y_test, pred_result))

"""Naive Bayes"""

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report 
bayes = MultinomialNB()
bayes.fit(x_train_tfidf,y_train)

nb_result = bayes.predict(x_test_tfidf)
from sklearn import metrics
model = metrics.accuracy_score(y_test, nb_result)
print("The Accuracy is",str('{:04.2f}'.format(model*100))+'%')

from sklearn.metrics import confusion_matrix
matrix2= confusion_matrix(y_test, nb_result)
print(matrix2)

import seaborn as sns
sns.heatmap(matrix2, square= True, annot= True, cbar= False, cmap='RdBu', xticklabels=['Real','Hoax'], yticklabels= ['Real','Hoax'], fmt= 'g')
plt.xlabel('prediksi label')
plt.ylabel('true label')

from sklearn.metrics import classification_report
print("The classification report is:")
print(classification_report(y_test, nb_result))

"""**Hasil**"""

Berita = input('Masukkan Berita : ')
result = SVM.predict(tfidf.transform([Berita]))
if(result == [0]):
  result = 'Berita yang dimasukkan merupakan berita REAL'
elif(result==[1]):
  result = 'Berita yang dimasukkan merupakan berita HOAX'
result

Berita = input('Masukkan Berita : ')
result = SVM.predict(tfidf.transform([Berita]))
if(result == [0]):
  result = 'Berita yang dimasukkan merupakan berita REAL'
elif(result==[1]):
  result = 'Berita yang dimasukkan merupakan berita HOAX'
result

import joblib
filename='svm.sav'
joblib.dump(SVM,filename)

labelfile='vectorizer.sav'
joblib.dump(tfidf,labelfile)

loaded_model = joblib.load('svm.sav')
mlb = joblib.load('vectorizer.sav')

x_tes = []
for i in mlb.inverse_transform(x_test):
    x_tes.append(" ".join(i))
categdf=pd.DataFrame({
                'x_test' : x_test, 
                 'y_true': y_test,
                 'y_pred': predictions_SVM
                 })
print(categdf.count())
categdf['correct'] = np.where(categdf['y_true']==categdf['y_pred'], 'benar', 'salah')
display(categdf.style.highlight_max(color='#f00', subset=pd.IndexSlice[:, ['correct']], axis=0))

categdf.to_csv('categdf.csv', index=False)

predict_score = df['label'].value_counts()
predict_score

import matplotlib.pyplot as plt

labels = ['Real','Hoax']
Category1 = [797,5329]
plt.bar(labels, Category1, tick_label=labels, width=0.5, color=['coral', 'c'])
plt.xlabel('Berita')
plt.ylabel('Data')
plt.title('Diagram Bar pada Deteksi Berita')
plt.savefig("bar.png")
plt.show()

color = ['coral', 'c']
plt.pie(Category1, labels=labels, colors=color,startangle=90, shadow=True, autopct='%1.2f%%', explode=(0.1, 0))
plt.title('Diagram Pie Data Bersih')
plt.legend()
plt.savefig("pie.png")
plt.show()

predict_score = df_train['label'].value_counts()
predict_score

labels = ['Real','Hoax']
Category2 = [644,4256]
plt.bar(labels, Category2, tick_label=labels, width=0.5, color=['coral', 'c'])
plt.xlabel('Berita')
plt.ylabel('Data')
plt.title('Diagram Bar pada Deteksi Berita Data Latih')
plt.savefig("bar1.png")
plt.show()

color = ['coral', 'c']
plt.pie(Category2, labels=labels, colors=color,startangle=90, shadow=True, autopct='%1.2f%%', explode=(0.1, 0))
plt.title('Diagram Pie Deteksi Berita Hoax Data Latih')
plt.legend()
plt.savefig("pie1.png")
plt.show()

predict_score = df_test['label'].value_counts()
predict_score

labels = ['Real','Hoax']
Category3 = [153,1073]
plt.bar(labels, Category3, tick_label=labels, width=0.5, color=['coral', 'c'])
plt.xlabel('Berita')
plt.ylabel('Data')
plt.title('Diagram Bar pada Deteksi Berita Data Tes')
plt.savefig("bar2.png")
plt.show()

color = ['coral', 'c']
plt.pie(Category3, labels=labels, colors=color,startangle=90, shadow=True, autopct='%1.2f%%', explode=(0.1, 0))
plt.title('Diagram Pie Deteksi Berita Hoax Data Tes')
plt.legend()
plt.savefig("pie2.png")
plt.show()

predict_score = test_prediction['label'].value_counts()
predict_score

labels = ['Real','Hoax']
Category4 = [26,1200]
plt.bar(labels, Category4, tick_label=labels, width=0.5, color=['coral', 'c'])
plt.xlabel('Berita')
plt.ylabel('Data')
plt.title('Diagram Bar pada Deteksi Berita klasifikasi svm')
plt.savefig("bar3.png")
plt.show()

color = ['coral', 'c']
plt.pie(Category4, labels=labels, colors=color,startangle=90, shadow=True, autopct='%1.2f%%', explode=(0.1, 0))
plt.title('Diagram Pie Data klasifikasi svm')
plt.legend()
plt.savefig("pie3.png")
plt.show()