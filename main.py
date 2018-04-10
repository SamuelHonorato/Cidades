from mpl_toolkits.basemap import Basemap
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import random
import copy as cp

class Mapa:
    def __init__(self):
        self.map = Basemap(projection='merc',
              lat_0 = 0, lon_0 = 0,
              resolution = 'h',
              area_thresh = 0.1,
              llcrnrlon=-42,
              llcrnrlat=-7.9,
              urcrnrlon=-37,
              urcrnrlat=-2.7)
        self.map.drawcoastlines()
        self.map.drawcountries()
        self.map.drawstates()
        self.map.drawmapboundary(fill_color='aqua')
        self.map.drawstates(color='0.5')

    def inserir_cidade(self, cidade):
        x,y = self.map(cidade['longitude'], cidade['latitude'])
        self.map.plot(x, y, 'bo', markersize=5)
        dx = 5000
        dy = 2500
        plt.text(x+dx, y+dy, cidade['nome'])

    def liga_cidades(self, cidades):

        for i in range(len(cidades)):
            cidade1 = cidades[i]
            cidade2 = cidades[i+1] if i+1 < len(cidades) else cidades[0]
            self.inserir_cidade(cidade1)
            self.inserir_cidade(cidade2)
            x, y = self.map.gcpoints(cidade1['longitude'], cidade1['latitude'], cidade2['longitude'], cidade2['latitude'], 300)

            self.map.plot(x, y)
    
    def exibir(self):
        plt.show()

        
def abre_arquivo():
    cidades = []
    nome_do_arquivo = '1021990-ceara3.txt'
    arquivo = open('./'+nome_do_arquivo, 'r')
    linhas = arquivo.readlines()
    arquivo.close()
    
    for i in range(len(linhas)):
        cidades.append(formata_linha(i, linhas[i]))
    return cidades

def formata_linha(index, linha):
    dado = linha.split(",")
    codigo = dado[0]
    nome = dado[1]
    longitude = dado[2] + "." + dado[3]
    latitude = dado[4] + "." + dado[5]
    
    return {'index': index, 'codigo': codigo, 'nome': nome, 'longitude': float(longitude), 'latitude': float(latitude)}

def gera_cidades(cidades, quantidade):
    cidades_selecionadas = []
    for i in range(quantidade):
        cidades_selecionadas.append(cidades[i])
    return cidades_selecionadas

def distancia_cidade(cidade1, cidade2):
    degree_in_km = 111.12
    distancia = np.sqrt((cidade1['longitude']-cidade2['longitude'])**2+
                        (cidade1['latitude']-cidade2['latitude'])**2)
    return (np.min(distancia)*degree_in_km)

def distancia_total(cidades):
    total = 0.0
    cidades.append(cidades[0])
    for i in range(len(cidades)-1):
        primeira = cidades[i]
        segunda = cidades[i+1]
        total += distancia_cidade(primeira, segunda)
    return total

class Solucao:
    def __init__(self, cidades):
        self.cidades = cidades[:]
        self.distancia_total = distancia_total(self.cidades[:])

def ordem_cidades(cidades):
    m = 0
    n = 0
    tam = len(cidades)-1
    nova_ordem = []
    while m == n:
        m = random.randint(1, tam)
        n = random.randint(1, tam)

    for i in range(len(cidades)):
        if i == m:
            nova_ordem.append(cidades[n])
        elif i == n:
            nova_ordem.append(cidades[m])
        else:
            nova_ordem.append(cidades[i])

    return nova_ordem

def porcentagem(delta, temperatura):
    return np.exp(delta/temperatura)

def principal():

    cidades = []
    cidades = abre_arquivo()
    solucoes_grafico = []
    quantidade_solucoes = 0

    escolhidas = []
    for i in range(20):
        escolhidas.append(cidades[i])
        
    temperatura = 10000
    alfa = 0.003

    melhor_solucao = Solucao(escolhidas)
    
    while temperatura > 1:
        cidades_linha = ordem_cidades(melhor_solucao.cidades[:])
        solucao_linha = Solucao(cidades_linha)
        
        delta = melhor_solucao.distancia_total - solucao_linha.distancia_total

        r = random.uniform(0, 1)
        
        p = porcentagem(delta, temperatura)

        if delta > 0 or p > r:
            melhor_solucao = solucao_linha
            solucoes_grafico.append(melhor_solucao.distancia_total)
            quantidade_solucoes += 1

        temperatura *= 1 - alfa
    
    mapa = Mapa()
    mapa.liga_cidades(melhor_solucao.cidades)
    mapa.exibir()
    
    eixo_x = []
    for i in range(len(solucoes_grafico)):
        eixo_x.append(i)
        
    plt.bar(eixo_x, solucoes_grafico)
    plt.xlabel('Quantidade: {0}'.format(quantidade_solucoes))
    plt.ylabel('Valor(Km)')
    plt.title('Grafico de Solucoes - melhor: {0} Km'.format(melhor_solucao.distancia_total))
    plt.show()

principal()
