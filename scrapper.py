import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size':6})

# Obtendo conteúdo da página
response = requests.get('https://dev2021lab.unacapital.com.br/', auth=('candidato', 'DEVUNA2021'))
content = response.content
site = BeautifulSoup(content, 'html.parser')
table = site.find('table', attrs={'class':'table'})

# Covertendo para DataFrame
table_str = str(table)
df = pd.read_html(table_str)[0] 

# Criando arquivo .xlsx
df.to_excel('./tabelaUna.xlsx', index = False)

# Lendo Tabela e absorvendo dados para criação do gráfico
dados = pd.read_excel('./tabelaUna.xlsx')
date = dados['Date']
openC = dados['Open']
close = dados['Close']
x = np.arange(len(date))
largura = 0.38

# Criação da barras do gráfico
fi, ax = plt.subplots(figsize=(18,8))
grupo1 = ax.bar(x - largura/2, openC, largura, label="Open", color='royalblue')
grupo2 = ax.bar(x + largura/2, close, largura, label="Close", color='purple')

# Função para adicionar valores nas barras
def autolabel(grupos):
    for i in grupos:
        h = i.get_height()
        ax.annotate('{}'.format(h),
            xy = (i.get_x()+i.get_width()/2,h),
            xytext=(0,1),
            textcoords = 'offset points',
            ha = 'center')

# Definição dos titulos e legendas
ax.set_title('Variação dos Preços/Tempo', fontsize=22)
ax.set_ylabel('Open / Close', fontsize=18)
ax.set_xlabel('Tempo(meses)', fontsize=18)
ax.legend()
ax.set_ylim([0,30])
ax.set_xticks(x)
ax.set_xticklabels(date)
autolabel(grupo1)
autolabel(grupo2)

# Salvar grafico em imagem .png
plt.savefig('./graficoVarPrecos.png', dpi=600)