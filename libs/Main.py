import pandas as pd

class Recommender:
    def __init__(self, data):
        self.df = pd.read_csv(data)

    def recommend(self, genre=None, release=None, topk=10):
        df = self.df.copy()
        genre = [item.title() for item in genre]
        df = self.demographic_filtering(df, genre=genre, min_release=release)
        df = self.calc_imdb_score(df)

        result = df.loc[:, "title":"release_year"].sort_values("vote_average", ascending=False).head(topk)
        return result[["title", "vote_average", "vote_count", "release_year"]]

    @staticmethod
    def demographic_filtering(df, min_release=None, genre=None):
        if min_release is not None:
            df = df[df.release_year >= min_release]
        if genre is not None:
            df = df[df[genre].all(axis="columns")]

        return df
        
    @staticmethod
    def calc_imdb_score(df, q=0.95):
        df = df.copy()
        m = df.vote_count.quantile(q)
        C = (df.vote_average * df.vote_count).sum() / df.vote_count.sum()
        # Minimum Rate
        df = df[df.vote_count >= m]
        df["score"] = df.apply(lambda x: (x.vote_average * x.vote_count + C * m) / (x.vote_count + m), axis=1)
        return df.loc[:, "title":"release_year"].sort_values("vote_average", ascending=False)
    