from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import Tkinter as tk

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

        for i in range(len(cidades)-1):
            cidade1 = cidades[i]
            cidade2 = cidades[i+1]
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
    
    for linha in linhas:
        cidades.append(formata_linha(linha))
    return cidades

def formata_linha(linha):
    dado = linha.split(",")
    codigo = dado[0]
    nome = dado[1]
    longitude = dado[2] + "." + dado[3]
    latitude = dado[4] + "." + dado[5]
    
    return {'codigo': codigo, 'nome': nome, 'longitude': float(longitude), 'latitude': float(latitude)}

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

def busca_cidade_nome(busca, cidades):
    result = []
    for cidade in cidades:
        nome = cidade['nome']
        if nome[:len(busca)] == busca:
            result.append(cidade)
    return result

def principal():
    cidades = []
    cidades = abre_arquivo()

##    root1 = tk.Tk()
##    label = tk.Label(root1, text='our label widget')
##    entry = tk.Entry(root1)
##
##    label.pack(side=tk.TOP)
##    entry.pack()
##    root1.mainloop()
    

    
#    mapa = Mapa()
#    mapa.inserir_cidade(cidades[0])
#    mapa.inserir_cidade(cidades[1])
#    mapa.liga_cidades(busca_cidade_nome('MA', cidades))
#    mapa.exibir()

##    cidade1 = cidades[0]
##    cidade2 = cidades[1]
##    print(cidade1)
##    print(cidade2)
##    print(distancia_cidade(cidade1, cidade2))


principal()


