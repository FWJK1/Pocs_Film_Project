Things to do:

Fitz
* Clean letterboxd (later this weekend)
    * load the tropes_year_movie csv in and 
        * get only those rows with an empty movie column. 
        * make a frame with just those rows, and push to a new tropes_year_movie_round2.csv (just for safe keeping)
    * merge the empty movie col rows against the tropes_imdb_year csv. then we have only those rows that failed to get to letterboxd properly. we can then run the get_movie function on this with a longer sleep time (to hopefully get better results) and append its chunk csv to the NEW csv.
    * we can then load the new round2.csv in, get only the rows that aren't already in the troes_year_movie.csv, and process those comments. This should get us another 1000 or so movies, at least. 

* today 
    * merge the tropes_year_movie.csv and the movie_n_comments.csv. then make a new column for all the movies comments, and for the genre of the movie 
    * create different dataframes for each of the genres with movie name, comments, and genre.
    * do zipfian, allotaxometric, and sentiment analysis for the words in the comments for each of them'
        *zipf: smash all the words together into a text file, do frequency count, then do Nk stuff
        *allotaxometric: see the babynames notebook from earlier assignment // the online resource
        *sentiment analysis: jeremy


Short Video Ideas
- Studying Film community and criticism across Letterboxd and TV Tropes
- goal 1: study how 'microcultures' differ, if at all, across the subcultures of different genre fans
- 