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
from sklearn.neural_network import MLPClassifier

def audience_prediciton(movie_name):
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
                if rating >= 0 and rating <= 5.9:
                        rating_list.append(1)
                elif rating >= 6 and rating <= 6.9:
                        rating_list.append(2)
                elif rating >= 7 and rating <= 7.9:
                        rating_list.append(3)
                else:
                        rating_list.append(4)


        df_ratings['audience_class'] = rating_list


        df = df_ratings[['num_voted_users', 'imdb_score', 'audience_class']]


        x = df.drop('audience_class', axis=1)
        y = df['audience_class']

        # x=x.to_numpy()

        #print(x.shape)
        # x = x.reshape(x.shape[0], x.shape[1], 1)
        #print(x.shape)

        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.15)


        from sklearn.ensemble import RandomForestClassifier
        mlp = MLPClassifier()
        mlp.fit(xtrain, ytrain)
        x_test=[]
        df_rv2 = df_ratings.loc[df_ratings['original_title']==movie_name, ['num_voted_users', 'imdb_score']]
        for votes in df_rv2["num_voted_users"]:
                x_test.append(votes)
        for score in df_rv2["imdb_score"]:
                #print(score)
                x_test.append(score)

        predict_result = mlp.predict([x_test])


        return predict_result


#mn='Avatar'

#print(audience_prediciton(mn))


