import pandas as pd
from datetime import datetime

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from surprise import Reader, Dataset
from surprise import KNNWithMeans, SVD
from surprise import accuracy
from surprise.model_selection import train_test_split

from dataframes import *

class PopularityBasedFiltering:
    def __init__(self, df):

        self.df = df
        # mean rating across the whole data
        self.C = self.df['average_rating'].mean()
        # minimum ratings required to be listed in the chart
        if self.df['user_ratings_total'].mean() > 100:
            self.m = self.df['user_ratings_total'].quantile(0.75)
        else:
            self.m = self.df['user_ratings_total'].quantile(0.55)

    def weighted_rating(self, X):
        
        v = X['user_ratings_total']
        R = X['average_rating']

        # IMBD's weighted rating formula
        return (v/(v+self.m) * R) + (self.m/(self.m+v) * self.C)
    
    def generate_scores(self):
        self.df = self.df.copy().loc[self.df['user_ratings_total'] >= self.m]
        self.df['score'] = self.df.apply(self.weighted_rating, axis=1)
        try:
            self.df['score'] = self.df[['prediction', 'score']].sum(axis=1)
            return self.df.sort_values('score', ascending=False)
        except:
            return self.df.sort_values('score', ascending=False)
        
class UserBasedFiltering:
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
        sim_scores = sim_scores[1:11]
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
    def __init__(self):

        self.reader = Reader(rating_scale=(1, 5))
        self.data = Dataset.load_from_df(ratings_df[['user_id', 'place_id', 'rating']], self.reader)

        self.trainset, self.testset = train_test_split(self.data, test_size=0.25, random_state=42)

        self.algo = SVD(n_epochs=30, lr_all=0.2, reg_all=0.1).fit(self.trainset)
        self.test_preds = self.algo.test(self.testset)
        self.rmse = round(accuracy.rmse(self.test_preds, verbose=False), 3)
        self.mae = round(accuracy.mae(self.test_preds, verbose=False), 3)
    
    def make_recommendations(self, user_id):
        rated_places = list(ratings_df[ratings_df['user_id']==user_id]['place_id'])
        rated_places_indices = [places_df[places_df['place_id']==p].index[0] for p in rated_places]
        unrated_places = places_df.drop(rated_places_indices).reset_index(drop=True)
    
        predictions = []
        for place_id in unrated_places['place_id'].tolist():
            predictions.append(self.algo.predict(uid=user_id, iid=place_id).est)
        
        cols = ['place_name', 'place_types', 'average_rating', 'user_ratings_total']
        df = pd.concat([unrated_places[cols], 
                        pd.DataFrame(predictions, columns=['prediction'])], axis=1)

        return df.sort_values('prediction', ascending=False).head(100)

# class ContextualizedRecommendations:
#     def __init__(self):

#         self.current_datetime = datetime.now()

#     # necessary functions for contextual_update function
#     def eating_time(self):
#         # breakfast
#         hour = self.current_datetime
#         if 7 < hour < 9:
#             return True
#         elif 12 < hour < 14:
#             return True
#         elif 18 < hour < 20:
#             return True
#         else:
#             return False

#     def day_time(self):
#         time = self.current_datetime
#         morning=time.replace(hour=12,minute=0,second=0,microsecond=0)
#         afternoon=time.replace(hour=16,minute=0,second=0,microsecond=0)
#         evening=time.replace(hour=19,minute=0,second=0,microsecond=0)

#         if now < morning :
#             return "morning"
#         elif now<afternoon :
#             return "afternoon"
#         elif now<evening :
#             return "evening"
#         else:
#             return "night"

#     def season():
#         month = datetime.now().month
#         if month < 3 or month > 11:
#             return "winter"
#         elif month < 6:
#             return "spring"
#         elif month < 9:
#             return "summer"
#         else :
#             return "autumn"

#     def is_weekend():
#         day=datetime.now().isoweekday()
#         if day < 6:
#             return False
#         return True

#     def contextual_update(df, family=False, device="Mobile", no_of_people=1, date_passed=datetime.now().date()):
#         # Reducing score to take account for contextual_update
#         effect_rate = 0.75
#         category = 4
#         df['prediction'] = df['prediction']-effect_rate

# if __name__ == '__main__':
#     print(ContextualizedRecommendations.season())