Importação de Bibliotecas:

Importamos as bibliotecas necessárias, incluindo o Streamlit para a interface do usuário, o pandas para manipulação de dados, o PIL para processamento de imagens e o scikit-learn para vetorização TF-IDF e cálculos de similaridade.
Chave da API TMDb:

A chave da API do TMDb é necessária para acessar os dados de filmes. Certifique-se de obter sua própria chave em https://www.themoviedb.org/documentation/api e substitua a variável TMDB_API_KEY com sua chave.
Funções para Carregar Dados e Obter URLs de Cartazes:

load_movie_data: Obtém dados de filmes do TMDb com base em uma categoria específica.
get_movie_poster_url: Gera a URL completa do cartaz do filme usando o path fornecido pela API.
Função para Criar Recomendador por Gênero:

create_genre_recommender: Utiliza a técnica TF-IDF para criar uma matriz de termos-por-documento e calcula a similaridade de cosseno entre os filmes com base em seus gêneros.
Interface Streamlit:

Criamos uma interface do Streamlit para a aplicação, incluindo uma barra lateral para seleção de categoria e uma caixa de seleção para mostrar ou ocultar recomendações de gênero.
Exibição de Detalhes do Filme Selecionado:

Apresentamos detalhes do filme selecionado, como visão geral, data de lançamento, avaliação média e cartaz.
Recomendações de Filmes por Gênero:

Se o usuário optar por mostrar recomendações por gênero, o script utiliza o recomendador de gênero para sugerir filmes relacionados com base no filme selecionado.
Lista de Filmes ou Recomendações de Gênero:

Dependendo da escolha do usuário, a interface exibirá ou a lista de filmes da categoria selecionada ou as recomendações de gênero.
Certifique-se de incluir informações sobre a chave da API TMDb, talvez através de um arquivo de configuração ou variável de ambiente, ao compartilhar o código no GitHub para garantir a segurança da sua chave.
