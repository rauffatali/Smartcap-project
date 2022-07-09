import re
import requests
import pandas as pd
import pytz
from datetime import datetime

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from surprise import Reader, Dataset
from surprise import KNNWithMeans, SVD
from surprise import accuracy
from surprise.model_selection import train_test_split

from dataframes import *
from config import weatherAPI

class PopularityBasedFiltering:
    def __init__(self, df):

        self.df = df.copy()
        # mean rating across the whole data
        self.C = self.df['average_rating'].mean()
        # minimum ratings required to be listed in the chart
        if self.df['user_ratings_total'].mean() > 225:
            self.m = self.df['user_ratings_total'].quantile(0.575)
        elif 225 > self.df['user_ratings_total'].mean() > 90:
            self.m = self.df['user_ratings_total'].quantile(0.375)
        else:
            self.m = self.df['user_ratings_total'].quantile(0.175)

    def weighted_rating(self, X):
        
        v = X['user_ratings_total']
        R = X['average_rating']

        # IMBD's weighted rating formula
        return (v/(v+self.m) * R) + (self.m/(self.m+v) * self.C)
    
    def popularity_scores(self):
        self.df = self.df.copy().loc[self.df['user_ratings_total'] >= self.m]
        self.df['pop_score'] = self.df.apply(self.weighted_rating, axis=1)
        self.df['pop_score'] = self.df['pop_score'].apply(lambda s: round(s, 3))
        return self.df
        
class DemographicFiltering:
    def __init__(self, user_id, df):
        
        self.user_id = user_id
        self.df = df

        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(self.df['user_profile'])
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)

        self.indices = pd.Series(self.df.index, index=self.df['user_id']).drop_duplicates()

    def make_recommendation(self, tresh=3):
        # obtain the index of the user
        idx = self.indices[self.user_id]
        # get the pairwsie similarity scores of all users with that obtained user
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        # sort users based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # get scores of the 10 most similar users with ignoring the first one
        sim_scores = sim_scores[1:16]
        # obtain all selected user indices
        user_indices = [i[0] for i in sim_scores]
        # return top 10 most similar users
        similar_user_ids = self.df['user_id'].iloc[user_indices]
        # get rated places by similar users
        ratings = ratings_df[ratings_df['user_id'].isin(similar_user_ids)]
        # reduce place number by selecting place ratings
        ratings = ratings[ratings['rating']>tresh]
        # obtain all selected place indices
        place_ids = set(ratings['place_id'].tolist())
        # return places to recommend
        return places_df[places_df['place_id'].isin(place_ids)]
    
class ModelBasedCF:
    def __init__(self, test_size=0.25, algo_name='SVD'):

        self.reader = Reader(rating_scale=(1, 5))
        self.data = Dataset.load_from_df(ratings_df[['user_id', 'place_id', 'rating']], self.reader)

        # split into train adn test set
        self.trainset, self.testset = train_test_split(self.data, test_size=test_size, random_state=42)
        
        if algo_name == 'SVD':
            # init recommender algorithm
            self.algo = SVD(n_epochs=30, lr_all=0.2, reg_all=0.1).fit(self.trainset)

            # make predictions
            self.test_preds = self.algo.test(self.testset)

            # calculate loss
            self.rmse = round(accuracy.rmse(self.test_preds, verbose=False), 3)
            self.mae = round(accuracy.mae(self.test_preds, verbose=False), 3)
        
        elif algo_name == 'KNN': 
            # init recommender algorithm
            self.algo = KNNWithMeans(k=9).fit(self.trainset)

            # make predictions
            self.test_preds = self.algo.test(self.testset)

            # calculate loss
            self.rmse = round(accuracy.rmse(self.test_preds, verbose=False), 3)
            self.mae = round(accuracy.mae(self.test_preds, verbose=False), 3)
        else: 
            print('Invalid Algorithm Name')

    def make_recommendations(self, user_id):

        rated_places = list(ratings_df[ratings_df['user_id']==user_id]['place_id'])
        rated_places_indices = [places_df[places_df['place_id']==p].index[0] for p in rated_places]
        unrated_places = places_df.drop(rated_places_indices).reset_index(drop=True)
    
        predictions = []
        for place_id in unrated_places['place_id'].tolist():
            predictions.append(self.algo.predict(uid=user_id, iid=place_id).est)
        
        # cols = ['place_name', 'place_types', 'average_rating', 'user_ratings_total']
        df = pd.concat([unrated_places, pd.DataFrame(predictions, columns=['prediction'])], axis=1)

        return df.sort_values('prediction', ascending=False).head(100)

"""
source code: https://github.com/yadavgaurav251/Context-Aware-Recommender
"""
class ContextualizedRecommendations:
    def __init__(self):
        
        self.current_datetime = datetime.now(pytz.timezone('Europe/Paris'))

    def weather(self, lat, lon):
        
        base_url = 'https://api.openweathermap.org/data/2.5/weather?'

        payload = {
            'lat': lat,
            'lon': lon,
            'appid': weatherAPI
        }
        
        response = requests.get(base_url, params=payload)

        weather = response.json()['weather'][0]['main']

        return weather
    
    def is_eating_time(self):

        hour = self.current_datetime.hour

        if 7 <= hour < 9:
            return True
        elif 12 <= hour < 14:
            return True
        elif 18 <= hour < 20:
            return True
        else:
            return False

    def day_time(self):
        
        now = self.current_datetime.time()
        # time ranges for morning
        morning_start = now.replace(hour=6, minute=0, second=0, microsecond=0)
        morning_end = now.replace(hour=12, minute=0, second=0, microsecond=0)
        # time ranges for afternoon
        afternoon_start = now.replace(hour=12, minute=0, second=0, microsecond=0)
        afternoon_end = now.replace(hour=18, minute=0, second=0, microsecond=0)
        # time ranges for evening
        evening_start = now.replace(hour=18, minute=0, second=0, microsecond=0)
        evening_end = now.replace(hour=22, minute=0, second=0, microsecond=0)
        # time ranges for night
        night_start = now.replace(hour=22, minute=0, second=0, microsecond=0)
        night_end = now.replace(hour=6, minute=0, second=0, microsecond=0)

        if morning_start <= now < morning_end:
            return 'morning'
        elif afternoon_start <= now < afternoon_end:
            return 'afternoon'
        elif evening_start <= now < evening_end:
            return 'evening'
        elif night_start <= now < night_end:
            return 'night'
        else:
            return 'invalid time'

    def is_weekend(self):
        day = self.current_datetime.isoweekday()
        if day < 6:
            return False
        else:
            return True
    
    def contextual_scores(self, df):
        
        # reducing score to take account for contextual update within 1-5 ranges
        effect = 0.65
        category = 8
        effect_rate = (effect/category)

        try:
            df['c_score'] = df['prediction']-effect
        except:
            df['c_score'] = df['pop_score']-effect

        if self.day_time() == "morning":
            scores = {
                'cultural': 0.25*effect_rate,
                'nature': 0.2*effect_rate
            }
        elif self.day_time() == "afternoon":
            scores = {
                'cultural': 0.25*effect_rate,
                'nature': 0.2*effect_rate,
                'entertainment': 0.2*effect_rate
            }
        elif self.day_time() == "evening":
            scores = {
                'night_life': 0.3*effect_rate,
                'accommodation': 0.2*effect_rate,
                'entertainment': 0.25*effect_rate,
            }
        elif self.day_time() == "night":
            scores = {
                'night_life': 0.5*effect_rate,
                'entertainment': 0.25*effect_rate,
            }
        
        for idx in df.index:
            new_score = 0
            place_type_1 = df['type_1'][idx]
            if place_type_1 in scores:
                new_score+=scores[place_type_1]
            df.loc[idx, 'c_score'] = df.loc[idx, 'c_score']+new_score
        
        if self.is_eating_time():
            scores = {
                'restaurant': 0.55*effect_rate,
                'bar': 0.45*effect_rate,
                'cafe': 0.25*effect_rate,
                'tea_house': 0.2*effect_rate,
                'pub': 0.3*effect_rate, 
            }
        
        for idx in df.index:
            new_score = 0
            place_type_2 = df['type_2'][idx]
            if place_type_2 in scores:
                new_score+=scores[place_type_2]
            df.loc[idx, 'c_score'] = df.loc[idx, 'c_score']+new_score
        
        if self.is_weekend():
            for idx in df.index:
                new_score = (0.25*effect_rate)
                if df.loc[idx, 'distance_type'] == 'far':
                    df.loc[idx, 'c_score'] = df.loc[idx, 'c_score']+new_score

        if self.weather == 'Rain' or self.weather == 'Snow' or self.weather == 'Extreme':
            for idx in df.index:
                new_score = (0.7*effect_rate)
                place_type_2 = df['type_2'][idx]
                if place_type_2 in ['nature', 'sport']:
                    df.loc[idx, 'c_score'] = df.loc[idx, 'c_score']-new_score

        return df