import pandas as pd
import git



def get_git_root():
    repo = git.Repo(search_parent_directories=True)
    return repo.git.rev_parse("--show-toplevel")
root = get_git_root()

df = pd.read_csv(f"{root}/Data/liteweight/2020_genre_counts_by_trope.csv", index_col=0)

# convert the counts into ratios -- for now, this is our score.
# eventually  we need a function for a more sophisticated approach.
tropes = [col for col in df.columns if col not in ["Unnamed: 0", "Trope",  r"\N", "Associated_Movies", "Number_movies"]]
ratio_df = df[['Trope']].copy() 
ratio_df[[col + '_ratio' for col in tropes]] = df[tropes].div(df['Number_movies'], axis=0)
ratio_cols = [col for col in ratio_df.columns if col != 'Trope']


## create individual ranked dataframes for each of them.
## for now, we'll just use the ratio as the 'score'
for genre in ratio_cols:
    rank_df = ratio_df[['Trope', genre]].copy()
    rank_df['rank'] = ratio_df[genre].rank(ascending=True)
    rank_df.sort_values(by='rank', ascending=False, inplace=True)
    rank_df.fillna(0, inplace=True)

    ## normalize the columns
    rank_df['rank_norm'] = (rank_df['rank'] - rank_df['rank'].min()) / (rank_df['rank'].max() - rank_df['rank'].min())

    # print(rank_df)
    # print(rank_df.head(30))

    ## save the csvs somewhere programatically 

## these are basically 'scoring dictionaries.' 

## for the trope_shifterator code itself, I think there's another csv that is one-hot encoded 
## we can use to get frequency distributions of these.

## hmm. but wait ... the frequency will always just be either 0 or 1.

## maybe we can do "by director" or some other grouping like that?