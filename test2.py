import pandas as pd
import numpy as np
import nltk
import json
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten, MaxPooling1D
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.datasets import load_iris
from numpy import unique

from sklearn.ensemble import RandomForestClassifier

df_ratings=pd.read_csv("../CBMR/IMDb/movie_metadata.csv")

ratings=df_ratings["imdb_score"]
rating_list=[]
for rating in ratings:
        if rating>=0 and rating<=4.9:
                rating_list.append(0)
        elif rating >= 5 and rating <= 5.9:
                rating_list.append(1)
        elif rating >= 6 and rating <= 6.9:
                rating_list.append(2)
        elif rating >= 7 and rating <= 7.9:
                rating_list.append(3)
        elif rating >= 8 and rating <= 8.9:
                rating_list.append(4)
        else:
                rating_list.append(5)
print(rating_list[1:10])

df_ratings['hit_class']=rating_list

print(df_ratings[['num_voted_users','imdb_score','hit_class']][:5])
df=df_ratings[['num_voted_users','imdb_score','hit_class']]
#print(df)

x= df.drop('hit_class',axis=1)
y = df['hit_class']


#x=x.to_numpy()

print(x.shape)
#x = x.reshape(x.shape[0], x.shape[1], 1)
print(x.shape)

xtrain, xtest, ytrain, ytest=train_test_split(x, y, test_size=0.15)

'''model = Sequential()
model.add(Dense(activation="relu", input_dim=2, units=7, kernel_initializer="uniform"))
model.add(Dense(activation="sigmoid", input_dim=2, units=1, kernel_initializer="uniform"))
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
model.fit(xtrain, ytrain, batch_size=50, epochs=200)
cnn = model.predict(xtest)
acc = accuracy_score(ytest,cnn)
print(acc)'''

rf=RandomForestClassifier()
rf.fit(xtrain,ytrain)

#xtest=[[34567,7.2]]


#predict=rf.predict(xtest)

print(accuracy_score(predict,ytest))