import pandas as pd
import numpy as np
from sklearn import preprocessing
import sklearn.metrics.pairwise as pw

def fill_to_length(array, fill_value):
    if len(array) < 5:
        array = np.pad(array, (0, 5 - len(array)), 'constant', constant_values=(fill_value))
    return array

def search_by_title(title):
    search_dataset = anime_dataset['Name'].str.lower()
    return search_dataset.index[search_dataset.str.contains(title.lower())].tolist()

def get_cosine_similarity(item1, item2):
    tags1 = fill_to_length(item1['Tags'], -1)
    tags2 = fill_to_length(item2['Tags'], -1)
    return pw.cosine_similarity([tags1], [tags2])

def generate_dataframe_cosine_similarity(search_index):
    search_item = anime_dataset.loc[search_index]
    for index, row in anime_dataset.iterrows():
        iterative_item = anime_dataset.loc[index]
        similarity = get_cosine_similarity(search_item, iterative_item)[0]
        anime_dataset.at[index, 'CosineSimilarity'] = similarity 
    return anime_dataset

def format_response(query_item, titles):
    response = f'{query_item} is similar to: \n'
    ranking = 1
    for title in titles:
        response += str(ranking) + '. ' + title + '\n'
        ranking += 1
    return response

def clean_and_create_dataframe():
    df = pd.read_csv('anime_recommender/dataset/anime.csv')
    df = df[:1000]
    df_columns = df[['Name', 'Type', 'Tags', 'Description', 'Rating']]
    df_columns['Type'] = df_columns['Type'].str.strip()
    df_columns = df_columns.loc[df_columns['Type'] == 'TV']

    df_columns['Tags'] = df_columns['Tags'].str.split(',').fillna('')
    df_columns['Tags'] = df_columns['Tags'].apply(lambda tags: [str.lower(tag.replace(" ", "")) for tag in tags])
    df_columns['Tags'] = df_columns['Tags'].apply(lambda tags: tags[:5])

    df_columns[df_columns['Tags'].apply(lambda x: len(x)) > 0]

    tag_enconder = preprocessing.LabelEncoder()

    tags = df_columns['Tags'].apply(pd.Series).stack().unique()

    # Need to make a copy that is the encoded values for the model
    # Need to clean the tags to not include '' and other trash values

    tag_enconder.fit(tags)
    df_columns['Tags'] = df_columns['Tags'].apply(lambda x: tag_enconder.transform(x))

    return df_columns

def handle_search_query(title):
    search_item_index_list = search_by_title(title)
    query_result = anime_dataset.loc[search_item_index_list].sort_values(by=['Rating'], ascending=False).head(10)
    query_result['SelectionIndex'] = np.arange(1, len(query_result) + 1)
    print(query_result.head(10))
    return query_result
    
def generate_query_response(list):
    # itterows is apparently bad so should think about a different way
    response = ''
    for index, row in list.iterrows():
        response += str(row['SelectionIndex']) + '. ' + row['Name'] + '\n'
    return response

def get_recommendations(index, dataset):
    search_item_title = dataset.loc[index].Name

    dataset['CosineSimilarity'] = 0
    dataset = generate_dataframe_cosine_similarity(index)
    dataset = dataset.loc[dataset['Name'] != search_item_title]

    sorted_df = dataset.sort_values(by=['CosineSimilarity'], ascending=False).head(10).sort_values(by=['Rating'], ascending=False)
    titles = sorted_df['Name'].dropna()
    response = format_response(search_item_title, titles)
    return response

def handle_recommendation_request(index):
    return get_recommendations(index, anime_dataset)

def initialize_recommender():
    try:
        global anime_dataset 
        anime_dataset = clean_and_create_dataframe()
        print('Recommender Initialized')
    except:
        print('Error Initializing Recommender')


