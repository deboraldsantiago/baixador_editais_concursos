import os
import requests
from bs4 import BeautifulSoup
import re

# URL da página de editais do Concurso Nacional Unificado;
url = 'https://www.gov.br/gestao/pt-br/concursonacional/editais'

# Cabeçalhos para evitar bloqueio da requisição;
headers = {'User-Agent': 'Mozilla/5.0'}

# Faz a requisição HTTP;
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Encontra todos os links <a> que apontam para arquivos PDF;
links_pdf = soup.find_all('a', href=re.compile(r'\.pdf$'))

# Define a pasta base onde os arquivos serão salvos;
pasta_base = 'Editais_ConcursosNacional'
os.makedirs(pasta_base, exist_ok=True)

# Função auxiliar para categorizar o link pelo texto;
def extrair_categoria(texto):
    texto = texto.lower()
    if 'retifica' in texto:
        return 'Retificacoes'
    elif 'convoca' in texto:
        return 'Convocacoes'
    elif 'resultado' in texto:
        return 'Resultados'
    elif 'edital' in texto:
        return 'Editais'
    else:
        return 'Outros'

# Processa os links e salva os arquivos nas subpastas;
for tag in links_pdf:
    texto_link = tag.get_text(strip=True)
    href = tag['href']

    # Corrige URL se for relativa;
    if href.startswith('/'):
        href = 'https://www.gov.br' + href

    categoria = extrair_categoria(texto_link)
    pasta_destino = os.path.join(pasta_base, categoria)
    os.makedirs(pasta_destino, exist_ok=True)

    # Nome limpo para o arquivo;
    nome_arquivo = texto_link.replace(' ', '_').replace('\n', '_')
    if not nome_arquivo.lower().endswith('.pdf'):
        nome_arquivo += '.pdf'
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    # Baixa o PDF;
    try:
        print(f'Baixando {nome_arquivo}...')
        pdf = requests.get(href, headers=headers)
        with open(caminho_arquivo, 'wb') as f:
            f.write(pdf.content)
        print(f'Salvo em: {caminho_arquivo}\n')
    except Exception as e:
        print(f'Erro ao baixar {href}: {e}')

print('Download concluído. Arquivos organizados por categoria.')