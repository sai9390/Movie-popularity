import pandas as pd
import numpy as np
import nltk
import json
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten, MaxPooling1D,Input
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_iris
from numpy import unique
#from keras.models import Model

def movie_hit_prediciton(movie_name):
        df_ratings = pd.read_csv("../CBMR/IMDb/movie_metadata.csv")


        original_title = df_ratings['original_title']
        org_title = []
        #Removing white space
        for tile in original_title:
                org_title.append(tile.strip())

        df_ratings['original_title'] = org_title


        ratings = df_ratings["imdb_score"]
        rating_list = []
        for rating in ratings:
                if rating >= 0 and rating <= 4.9:
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
        #print(rating_list[1:10])

        df_ratings['hit_class'] = rating_list


        df = df_ratings[['num_voted_users', 'imdb_score', 'hit_class']]


        x = df.drop('hit_class', axis=1)
        y = df['hit_class']

        # x=x.to_numpy()

        #print(x.shape)
        # x = x.reshape(x.shape[0], x.shape[1], 1)
        #print(x.shape)

        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.15)

        '''input_layer = Input(shape=(4286, 2))
        conv1 = Conv1D(filters=32,
                       kernel_size=8,
                       strides=1,
                       activation='relu')(input_layer)
        pool1 = MaxPooling1D(pool_size=4)(conv1)
        output_layer = Dense(6, activation='sigmoid')(pool1)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss = 'categorical_crossentropy',
             optimizer = "adam",
                      metrics = ['accuracy'])
        model.fit(xtrain, ytrain,epochs=100, verbose=1,batch_size=len(xtrain))'''

        '''model = Sequential()
        model.add(Conv1D(128, 2, activation="relu", input_shape=(len(xtrain), 2)))
        model.add(Dense(16, activation="relu"))
        model.add(MaxPooling1D())
        model.add(Flatten())
        model.add(Dense(6, activation = 'softmax'))
        model.compile(loss = 'categorical_crossentropy',
             optimizer = "adam",
                      metrics = ['accuracy'])
        model.summary()
        print(xtrain.shape)
        model.fit(xtrain, ytrain,epochs=100, verbose=1,batch_size=len(xtrain))
    
        acc = model.evaluate(xtrain, ytrain)
        print("Loss:", acc[0], " Accuracy:", acc[1])
    
        pred = model.predict(xtest)
        pred_y = pred.argmax(axis=-1)
        print(pred_y)'''
        from sklearn.ensemble import RandomForestClassifier
        rf = RandomForestClassifier()
        rf.fit(xtrain, ytrain)
        x_test=[]
        df_rv2 = df_ratings.loc[df_ratings['original_title']==movie_name, ['num_voted_users', 'imdb_score']]
        for votes in df_rv2["num_voted_users"]:
                x_test.append(votes)
        for score in df_rv2["imdb_score"]:
                #print(score)
                x_test.append(score)

        predict_result = rf.predict([x_test])


        return predict_result


#mn='Avatar'

#print(movie_hit_prediciton(mn))


