import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime, timedelta

def realizar_login():
    # Substitua a URL pela URL de login da sua API Kapua
    url_login = "http://kapua-api:8080/v1/authentication/user"

    # Substitua os campos "username" e "password" pelos seus dados de login
    dados_login = {
        "username": "User123",
        "password": "Kapu@12345678"
    }

    try:
        # Fazendo a solicitação POST para realizar o login
        resposta = requests.post(url_login, json=dados_login)
        print(resposta)
        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if resposta.status_code == 200:
            # Converte os dados JSON retornados para um dicionário Python
            dados_token = resposta.json()

            # Retorna o token de acesso
            return dados_token.get("tokenId")

        else:
            st.error(f"Erro durante o login. Código de status: {resposta.status_code}")
            return None

    except Exception as e:
        st.error(f"Erro durante o login: {e}")
        return None


# Chama a função para realizar o login e obter o token
token = realizar_login()

# Exibe o token obtido
if token:
    print(f"Token de acesso obtido: {token}")
else:
    st.error("Falha ao obter o token de acesso.")

def obter_dados_kapua(url):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # Fazendo a solicitação GET à API
        resposta = requests.get(url, headers=headers)

        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if resposta.status_code == 200:
            # Converte os dados JSON retornados para um DataFrame do pandas
            dados_json = resposta.json()
            dados = dados_json.get("items", [])

            # Criando um DataFrame pandas com os dados
            df = pd.DataFrame(dados)

            return df

        else:
            return None

    except Exception as e:
        print(f"Erro durante a solicitação: {e}")
        return None

# Configuração do Streamlit
st.title('Dados do Kapua')

# URLs para diferentes métricas
url = "http://kapua-api:8080/v1/_/data/messages?clientId=kuraBroker&sortDir=DESC&limit=50&offset=0"
# Chama a função para obter os dados do Kapua
df_dados = obter_dados_kapua(url)
# Se os resultados foram obtidos com sucesso, exibe na interface
if df_dados is not None and not df_dados.empty:
    # Convertendo os valores de string para float
    df_dados["Temperatura"] = df_dados["payload"].apply(lambda x: float(x["metrics"][2]["value"]))
    df_dados["Sensação Térmica"] = df_dados["payload"].apply(lambda x: float(x["metrics"][1]["value"]))
    df_dados["Umidade"] = df_dados["payload"].apply(lambda x: float(x["metrics"][0]["value"]))

     # Convertendo os horários para o fuso horário de Brasília
    df_dados['receivedOn'] = pd.to_datetime(df_dados['receivedOn'])
    df_dados['Horário'] = df_dados['receivedOn'] - timedelta(hours=3)  # Subtrai 3 horas para converter para Brasília


    ultimo_registro = df_dados.tail(1)
    # Exibindo os resultados
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperatura",  f'{df_dados["Temperatura"].iloc[0]:.2f} °C', f'{(df_dados["Temperatura"].iloc[0] - ultimo_registro["Temperatura"].iloc[0]):.2f} °C')
    col2.metric("Sensação Térmica", f'{df_dados["Sensação Térmica"].iloc[0]:.2f} °C', f'{(df_dados["Sensação Térmica"].iloc[0] - ultimo_registro["Sensação Térmica"].iloc[0]):.2f} °C')
    col3.metric("Umidade", f'{df_dados["Umidade"].iloc[0]:.2f}%', f'{(df_dados["Umidade"].iloc[0] - ultimo_registro["Umidade"].iloc[0]):.2f}%')

    # Criando gráficos com Plotly Express
    fig_temperatura = px.line(df_dados, x='Horário', y='Temperatura', title='Temperatura ao longo do tempo')
    fig_sensacao_termica = px.line(df_dados, x='Horário', y='Sensação Térmica', title='Sensação Térmica ao longo do tempo')
    fig_umidade = px.line(df_dados, x='Horário', y='Umidade', title='Umidade ao longo do tempo')

    # Plotando os gráficos
    st.plotly_chart(fig_temperatura)
    st.plotly_chart(fig_sensacao_termica)
    st.plotly_chart(fig_umidade)

else:
    st.error("Erro ao obter dados do Kapua.")