from .Grafo import Grafo
import matplotlib.pyplot as plt

    
class Caminhos:
    grafo = None
    caminhos = None
    pesos = None
    menor_peso = None
    menores_caminhos = None
    
    def __init__(self, grafo, verbose=True):
        self.grafo = grafo
        
        self.caminhos=[]
        caminho = []
        
        if verbose:
            print('Calculando possíveis caminhos...')
            
        for v in grafo.vertices():
            self.__percorre__(caminho.copy(),v,grafo)
        
        self.caminhos = tuple(self.caminhos)
        
        self.menor_peso = None
        self.menores_caminhos = None
        
        if verbose:
            print('Calculando menores caminhos...')
        
        self.__calculaMenoresCaminhos__()

    
    def __percorre__(self, caminho, i, grafo):
        if i in caminho:
            return False
        
        caminho.append(i)
        
        if len(caminho) >= grafo.size():
            self.caminhos.append(tuple(caminho))
    
        for e in grafo.edges(i):
            self.__percorre__(caminho.copy(),e,grafo)
    
    #Calcula o peso de um caminho
    def __calculaPesoCaminho__(self,caminho):
        soma = 0
        for i in range(len(caminho)-1):
            soma+=self.grafo.weight(caminho[i],caminho[i+1])
        return soma
    
    #Calcula os pesos de diversos caminhos
    def __calculaPesosCaminhos__(self):
        self.pesos = []
        for c in self.caminhos:
            self.pesos.append(self.__calculaPesoCaminho__(c))
            
        self.pesos = tuple(self.pesos)
        return self.pesos
    
    #Calcula quais são os menores caminhos
    def __calculaMenoresCaminhos__(self):
        #Obtém os pesos dos caminhos
        pesos = self.__calculaPesosCaminhos__()
        #obtém o peso de menor valor
        self.menor_peso = min(pesos) #

        #obtêm quais são as posições em que estão os menores pesos
        idx_menor = []
        for p in range(len(pesos)):
            if pesos[p] == self.menor_peso:
                idx_menor.append(p)

        #seleciona os caminhos que têm os menores pesos
        menores_caminhos = []
        for idx in idx_menor:
            menores_caminhos.append(self.caminhos[idx])
        
        self.menores_caminhos = tuple(menores_caminhos)
        return self.menores_caminhos
    
    def plot(self, caminho=None, edges=False, vertices=False, mirror_y=False):
        
        plt.figure()
        
        #caso o caminho a ser plotado não esteja especificado, o primeiro menor é utilizado
        if not caminho:
            caminho = self.menores_caminhos[0]
            
        #calcula as posições das arestas que formam o menor caminho
        
        #obtém a maior posição y, para espelhar
        if mirror_y:
            _, y = self.grafo.coords()
            max_y = max(y)
        
        #Plota as arestas
        if edges:
            #obtém os pontos
            x, y = self.grafo.coords()
            
            #Plot as arestas
            for orig,dest in self.grafo.edges():
                x_orig, y_orig = self.grafo.coords_point(orig)
                x_dest, y_dest = self.grafo.coords_point(dest)
                
                if mirror_y:
                    y_orig = max_y - y_orig
                    y_dest = max_y - y_dest

                plt.plot((x_orig,x_dest),(y_orig,y_dest),c='k')
                
        #Plota os vertices
        if vertices:
            #obtém os pontos
            x, y = self.grafo.coords()
            
            if mirror_y:
                yy = []
                for i in range(len(y)):
                    yy.append(max_y - y[i])    
                y = tuple(yy)
            
            plt.scatter(x,y,c='k',marker='.')
        
        #Plota o caminho
        for idx in range(len(caminho)-1):
            orig = caminho[idx]
            dest = caminho[idx+1]
            
            x_orig, y_orig = self.grafo.coords_point(orig)
            x_dest, y_dest = self.grafo.coords_point(dest)
            
            if mirror_y:
                y_orig = max_y - y_orig
                y_dest = max_y - y_dest
            
            plt.plot((x_orig,x_dest),(y_orig,y_dest),c='r')
        
        #ponto inicial
        x,y = self.grafo.coords_point(caminho[0])
        if mirror_y: y = max_y - y
        plt.scatter((x),(y), c='r',marker='o')
        
        #ponto final
        x,y = self.grafo.coords_point(caminho[-1])
        if mirror_y: y = max_y - y
        plt.scatter((x),(y), c='r', marker='x')
        
        plt.show()
        