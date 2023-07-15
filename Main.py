from libs.Main import Recommender
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# INPUT
genres = input("Enter the genres (ex: war, science fiction, horror) : ").split(", ")
years = input("Minimum Release Year (ex: 2012) : ")
years = None if years == "" else int(years)

recsys = Recommender(data="data/movie.csv")
recommend = recsys.recommend(genre=genres, release=years)
print(recommend.to_string(index=False))