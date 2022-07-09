import pandas as pd
import datatable as dt

from ast import literal_eval

# load dataframes
ratings_df = dt.fread('./data/fake_users.csv').to_pandas()
demographics_df = dt.fread('./data/user_demographics.csv').to_pandas()
places_df = dt.fread('./data/point_of_interests.csv').to_pandas()

# preprocess places dataframe
def mergeTypes(df):
    try:
        types = [df['type_1']] + [df['type_2']] + literal_eval(df['type_3'])
        return ', '.join(types)
    except:
        types = [df['type_1']] + [df['type_2']]
        return  ', '.join(types)

places_df['distance_type'] = places_df['distance'].apply(lambda d: 'near' if float(d.split()[0]) <= 1.2 else 'far')
places_df['distance_in_km'] = places_df['distance'].apply(lambda d: float(d.split()[0]))
places_df['place_types'] = places_df.apply(mergeTypes, axis=1)
places_df['average_rating'] = places_df['average_rating'].apply(lambda x: round(x, 2))

# merge ratings and places dataframes based on unique id of each place
merged_df = pd.merge(ratings_df, places_df, on='place_id', how='left')

# preprocess demographics dataset
def clean_demographics(row):
        splitted_row = row.split(' ')
        if len(splitted_row) > 1:
            return ''.join(splitted_row)
        else:
            return row