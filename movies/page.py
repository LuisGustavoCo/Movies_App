import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
from movies.service import MovieService
from datetime import datetime
from actors.service import ActorService
from genres.service import GenreService


def show_movies():
    movie_service = MovieService()
    movies = movie_service.get_movies()

    if movies:
        st.write('Lista de Filmes: ')

        movies_df = pd.json_normalize(movies)
        movies_df = movies_df.drop(columns=['genre.id', 'actors'])

        AgGrid(
            data=movies_df,
            reload_data=True,
            key='movies_grid',
            )
    else:
        st.warning('Nenhum filme encontrado')

    st.title('Cadastrar Novo Filme')

    title = st.text_input('Título')

    release_date = st.date_input(
        label='Data de lançamento',
        value=datetime.today(),
        min_value=datetime(1800, 1, 1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY',
    )

    genre_service = GenreService()
    genres = genre_service.get_genres()
    genres_names = {genre['name']: genre['id'] for genre in genres}
    selected_genre_name = st.selectbox('Gênero', list(genres_names.keys()))

    actor_service = ActorService()
    actors = actor_service.get_actors()
    actor_names = {actor['name']: actor['id'] for actor in actors}
    selected_actors_name = st.multiselect('Atores/Atrizes', list(actor_names.keys()))
    selected_actors_ids = [actor_names[name] for name in selected_actors_name]

    resume = st.text_area('Resumo')
    if st.button('Cadastrar'):
        new_movie = movie_service.create_movie(
            title=title,
            release_date=release_date,
            genre=genres_names[selected_genre_name],
            actors=selected_actors_ids,
            resume=resume,
        )
        if new_movie:
            st.rerun()
        else:
            st.error('Erro ao cadastrar o filme. Verifique os campos')


    
