import tmdbsimple as tmdb
tmdb.API_KEY = '001b749cd9f5c8ea38f29de0bc702158'
search = tmdb.Search()
response = search.movie(query='mandela', year="2021")
for s in search.results:
    print(s)
    # print(s['title'], s['id'], s['release_date'], s['popularity'])