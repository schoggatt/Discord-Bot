import pandas as pd
import numpy as np
from sklearn import preprocessing
import sklearn.metrics.pairwise as pw

#TODO: Need to make a feature that allows you to select the correct anime if multiple are returned

def fill_to_length(array, fill_value):
    if len(array) < 5:
        array = np.pad(array, (0, 5 - len(array)), 'constant', constant_values=(fill_value))
    return array

def search_by_title(title):
    # return df_columns.where(df_columns.Name == title).index()
    search_dataset = anime_dataset['Name'].str.lower()
    return search_dataset.index[search_dataset.str.contains(title.lower())].tolist()

def get_cosine_similarity(item1, item2):
    tags1 = fill_to_length(item1['Tags'], -1)
    tags2 = fill_to_length(item2['Tags'], -1)
    return pw.cosine_similarity([tags1], [tags2])

def generate_dataframe_cosine_similarity(search_index):
    for i in range(len(anime_dataset)):
        similarity = get_cosine_similarity(anime_dataset.iloc[search_index], anime_dataset.iloc[i])[0]
        anime_dataset.at[i, 'CosineSimilarity'] = similarity 
    return anime_dataset

def format_response(query_item, titles):
    response = f'{query_item} is similar to: \n'
    ranking = 1
    for title in titles:
        response += str(ranking) + '. ' + title + '\n'
        ranking += 1
    return response

def clean_and_create_dataframe():
    df = pd.read_csv('recommender/dataset/anime.csv')
    df = df[:1000]
    df_columns = df[['Name', 'Type', 'Tags', 'Description', 'Rating']]
    # df_columns[df_columns['Type'].apply(lambda t: t.strip() == 'TV')]

    df_columns['Tags'] = df_columns['Tags'].str.split(',').fillna('')
    df_columns['Tags'] = df_columns['Tags'].apply(lambda tags: [str.lower(tag.replace(" ", "")) for tag in tags])
    df_columns['Tags'] = df_columns['Tags'].apply(lambda tags: tags[:5])

    # df_columns['Name'] = df_columns['Name'].str.lower()

    df_columns[df_columns['Tags'].apply(lambda x: len(x)) > 0]

    tag_enconder = preprocessing.LabelEncoder()
    title_encoder = preprocessing.LabelEncoder()

    titles = df_columns['Name'].unique()
    tags = df_columns['Tags'].apply(pd.Series).stack().unique()

    # Need to make a copy that is the encoded values for the model
    # Need to clean the tags to not include '' and other trash values

    tag_enconder.fit(tags)
    df_columns['Tags'] = df_columns['Tags'].apply(lambda x: tag_enconder.transform(x))

    return df_columns

# some issue with assignment causing the dataframe to not be updated
# i need to remove the item that was searched for in the dataframe
# issues with the scope of the dataframe that needs to be fixed
def get_recommendations(title, dataset):
    search_item_index_list = search_by_title(title)
    if(len(search_item_index_list) > 0):
        search_item_index = search_item_index_list[0]
        search_item_title = dataset.iloc[search_item_index].Name

        dataset['CosineSimilarity'] = 0
        dataset = generate_dataframe_cosine_similarity(search_item_index)

        item1 = list(dataset.iloc[0]['Tags'])
        item2 = list(dataset.iloc[1]['Tags'])
        cosine_similarity = pw.cosine_similarity([item1], [item2])
        sorted_df = dataset.sort_values(by=['CosineSimilarity'], ascending=False).head(10).sort_values(by=['Rating'], ascending=False)
        response = format_response(search_item_title, list(sorted_df.Name))
        return response
    else:
        return 'No Matching Anime Found In Database'

def initialize_recommender():
    try:
        global anime_dataset 
        anime_dataset = clean_and_create_dataframe()
        print('Recommender Initialized')
    except:
        print('Error Initializing Recommender')

def handle_recommendation_request(title):
    return get_recommendations(title, anime_dataset)


