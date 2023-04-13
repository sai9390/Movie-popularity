import pandas as pd
import numpy as np
import nltk
import json
from sklearn.feature_extraction.text import TfidfVectorizer

def movie_recommends(movie_content):
        df_credits = pd.read_csv("../CBMR/TMDb/tmdb_5000_credits.csv")
        df_movies = pd.read_csv("../CBMR/TMDb/tmdb_5000_movies.csv")

        df_credits.columns = ['id', 'title', 'cast', 'crew']
        credits_movies_df = df_movies.merge(df_credits, on='id')
        # print(df.columns)

        test = [[movie_content]]
        # print(test[0])

        tfidf = TfidfVectorizer(stop_words='english')

        credits_movies_df['overview'] = credits_movies_df['overview'].fillna('')
        tfidf_matrix = tfidf.fit_transform(credits_movies_df['overview'])

        tfidf_test = tfidf.transform(test[0])

        from sklearn.neighbors import NearestNeighbors

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(tfidf_matrix)

        distances, indices = model_knn.kneighbors(tfidf_test, n_neighbors=2)

        movie_name = []
        genres = []
        casts = []
        director = []
        for i in range(0, len(distances.flatten())):
                # print(df.index[indices.flatten()[i]])
                movie_name.append(credits_movies_df['original_title'].iloc[indices.flatten()[i]])
                # print(credits_movies_df['crew'].iloc[indices.flatten()[i]])

                data = json.loads(credits_movies_df['genres'].iloc[indices.flatten()[i]])
                # print(type(data))
                # print(data)
                list_genres = []
                for gen in data:
                        # print(gen['name'])
                        list_genres.append(gen['name'])
                genres.append(list_genres)
                # print("cmd="+str(list1))
                # changing the genres column from json to string
                '''credits_movies_df['genres'] =json.dumps(credits_movies_df['genres'].iloc[indices.flatten()[i]])# .apply(json.loads)
                print(credits_movies_df['genres'] )
                for index, i in zip(credits_movies_df.index, credits_movies_df['genres']):
                        list1 = []
                        print("i=",i)
                        for j in range(len(i)):
                                #print(j)
                                #print("gen="+(i[j]['name']))
                                #list1.append((i[j]['name']))  # the key 'name' contains the name of the genre
                                credits_movies_df.loc[index, 'genres'] = str(list1)
                #print('{0}: {1}, with distance of {2}:'.format(i, credits_movies_df.index[indices.flatten()[i]], distances.flatten()[i]))'''

                data2 = json.loads(credits_movies_df['cast'].iloc[indices.flatten()[i]])
                # print(type(data))
                # print(data2)
                list_cast = []
                for gen2 in data2:
                        # print(gen2['character'])
                        list_cast.append(gen2['name'])

                # print("cmd2=",list2[0:5])
                casts.append(list_cast)
                data3 = json.loads(credits_movies_df['crew'].iloc[indices.flatten()[i]])
                # print(type(data))
                # print(data)
                list_crew = []
                for gen3 in data3:
                        # print(gen2['character'])
                        if gen3['job'] == 'Director':
                                list_crew.append(gen3['name'])

                # print("cmd3=" + str(list3))

                # print(movie_name)
                director.append(list_crew)
                print('{0}: {1}, with distance of {2}:'.format(i, credits_movies_df.index[indices.flatten()[i]],
                                                       distances.flatten()[i]))



        for i in range(len(movie_name)):
                print(movie_name[i], str(genres[i]), casts[i][0:5], director[i])



movie_recommends("The story of an ancient war that is reignited when a young farmhand unwittingly opens a gateway")
