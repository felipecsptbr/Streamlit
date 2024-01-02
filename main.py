import streamlit as st
import pandas as pd
from PIL import Image
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Chave da API do TMDb (obtenha a sua em https://www.themoviedb.org/documentation/api)
TMDB_API_KEY = 'API_KEY'

# Função para carregar dados do TMDb
def load_movie_data(category_id=None):
    # Endpoint para obter os filmes populares ou de uma categoria específica
    if category_id:
        endpoint = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={category_id}'
    else:
        endpoint = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'

    response = requests.get(endpoint)
    data = response.json()
    
    movies = []
    for movie in data['results']:
        movies.append({
            'title': movie['title'],
            'id': movie['id'],
            'poster_path': movie['poster_path'],
            'overview': movie['overview'],
            'genre_ids': movie['genre_ids'],
        })

    df = pd.DataFrame(movies)
    return df

# Função para obter a URL completa do cartaz do filme
def get_movie_poster_url(poster_path):
    base_url = 'https://image.tmdb.org/t/p/w500'  # Escolha o tamanho do cartaz desejado (w500, w300, etc.)
    return f'{base_url}{poster_path}' if poster_path else None

# Função para criar um recomendador baseado no gênero
def create_genre_recommender(movies):
    # Transforma os gêneros em uma string para usar no TfidfVectorizer
    movies['genres'] = movies['genre_ids'].apply(lambda x: ' '.join(map(str, x)))
    
    # Cria uma matriz de termos-por-documento usando TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies['genres'])
    
    # Calcula a similaridade de cosseno entre os filmes
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    return cosine_sim

# Interface do Streamlit
st.title("Sistema de Recomendação de Filmes (usando TMDb API)")

# Carregar dados para as categorias
categories_endpoint = f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US'
categories_response = requests.get(categories_endpoint)
categories_data = categories_response.json()
categories = {category['name']: category['id'] for category in categories_data['genres']}

# Sidebar para seleção de categoria
selected_category = st.sidebar.selectbox("Selecione uma Categoria:", list(categories.keys()))

# Carregar dados com base na categoria selecionada
category_id = categories[selected_category]
movies = load_movie_data(category_id)

# Exibir informações do filme
st.subheader("Detalhes do Filme:")
selected_movie = st.selectbox("Selecione um filme:", movies['title'])

# Obter informações detalhadas do filme
movie_id = movies[movies['title'] == selected_movie]['id'].values[0]
endpoint_movie_details = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US'
response_details = requests.get(endpoint_movie_details)
movie_details = response_details.json()

# Exibir detalhes do filme
st.write("Visão Geral:")
st.write(movie_details['overview'])

st.write("Data de Lançamento:")
st.write(movie_details['release_date'])

st.write("Avaliação Média:")
st.write(movie_details['vote_average'])

# Obter a URL do cartaz e exibir a imagem
poster_url = get_movie_poster_url(movie_details['poster_path'])
if poster_url:
    st.image(Image.open(requests.get(poster_url, stream=True).raw), caption="Cartaz do Filme", use_column_width=True)
else:
    st.warning("Nenhuma imagem disponível para este filme.")

# Adicione uma opção na barra lateral para recomendações de gênero
show_genre_recommendations = st.sidebar.checkbox("Mostrar Recomendações por Gênero")

# Se o usuário escolher ver recomendações por gênero
if show_genre_recommendations:
    st.title(f"Recomendações de Filmes com base no Gênero ({selected_category})")
    
    # Criar o recomendador de gênero
    genre_recommender = create_genre_recommender(movies)

    # Obter índice do filme selecionado
    selected_movie_index = movies[movies['title'] == selected_movie].index[0]

    # Obter as pontuações de similaridade para o filme selecionado
    movie_scores = list(enumerate(genre_recommender[selected_movie_index]))

    # Classificar os filmes com base nas pontuações de similaridade
    movie_scores = sorted(movie_scores, key=lambda x: x[1], reverse=True)

    # Exibir os filmes recomendados
    st.subheader("Filmes Recomendados:")
    num_recommendations = 5
    for i in range(1, num_recommendations + 1):
        rec_movie_index = movie_scores[i][0]
        recommended_movie = movies.iloc[rec_movie_index]
        rec_poster_url = get_movie_poster_url(recommended_movie['poster_path'])
        st.image(Image.open(requests.get(rec_poster_url, stream=True).raw), caption=recommended_movie['title'], use_column_width=True)

else:
    # Exibir várias imagens em uma linha
    st.subheader("Lista de Filmes:")
    num_movies_per_row = 4
    num_rows = len(movies) // num_movies_per_row + (len(movies) % num_movies_per_row > 0)

    for row in range(num_rows):
        cols = st.columns(num_movies_per_row)
        for col in range(num_movies_per_row):
            index = row * num_movies_per_row + col
            if index < len(movies):
                movie = movies.iloc[index]
                poster_url = get_movie_poster_url(movie['poster_path'])
                cols[col].image(Image.open(requests.get(poster_url, stream=True).raw), caption=movie['title'], use_column_width=True)
