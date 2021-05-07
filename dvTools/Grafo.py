import json

def hello():
    print('Hello Grafo')

class Grafo:
    filename = None
    grafo = None
    
    def __init__(self, file):
        self.filename = file
        
        #carrega o arquivo json
        json_file = open(self.filename, mode='r')
        grafo_json = json.load(json_file)
        json_file.close()
        
        #converte os índices para inteiro
        self.grafo = {}
        for p in grafo_json.keys():
            self.grafo[int(p)] = grafo_json[p]
    
        #converte as coordenadas dos pontos para tuplas
        for p in self.grafo.keys():
            self.grafo[p]['coords'] = tuple(self.grafo[p]['coords'])
    
        #Libera a memoria do dicionario com os dados lidos
        del(grafo_json)

    #Obtém quantos pontos há na malha
    def size(self):
        return len(self.grafo)
    
    #Obtém os pontos da malha
    def vertices(self):
        return sorted(list(self.grafo.keys()))
    
    #Obtém as coordenadas do pontos da malha
    def coords_point(self, p=None):
        if p==None:
            coords = []
            for p in self.vertices():
                coords.append(self.grafo[p]['coords'])

            return coords
        
        return self.grafo[p]['coords']
    
    def coords(self):
        x = []
        y = []
        for p in self.coords_point():
            x.append(p[0])
            y.append(p[1])
        x = tuple(x)
        y = tuple(y)
        
        return x,y
    
    #Obtém os pesos de todas as arestas
    def weights(self):
        weights = {}
        for p in self.vertices():
            weights[p] = {}
            for idx, edge in zip( range(len(self.grafo[p]['edges'])) ,self.grafo[p]['edges']):
                weights[p][edge] = self.grafo[p]['weights'][idx]
            
        return weights
    
    #Obtém as arestas
    def edges(self, p=None):
        #Obtém todas as arestas
        if p==None:
            edges = []
            for p in self.vertices():
                for q in self.grafo[p]['edges']:
                    edges.append((p,q))

            return edges
        else:
            #Obtém os vértices que formam aresta com um ponto
            return self.grafo[p]['edges']

        
    
    #Obtém o peso de uma aresta específica
    def weight(self,i,j):
        
        if j not in self.grafo[i]['edges']:
            return False
        
        idx = self.grafo[i]['edges'].index(j)
        return self.grafo[i]['weights'][idx]
    
        
    def plot(self, vertices=True, edges=True, mirror_y = False):
        
        import matplotlib.pyplot as plt
        
        plt.figure()
        
        if mirror_y:
            _, y = self.coords()
            max_y = max(y)
        
        if edges:
            #Plot as arestas
            for orig,dest in self.edges():
                x_orig, y_orig = self.coords_point(orig)
                x_dest, y_dest = self.coords_point(dest)
                
                if mirror_y:
                    y_orig = max_y - y_orig
                    y_dest = max_y - y_dest

                plt.plot([x_orig,x_dest],[y_orig,y_dest],c='k')
        
        if vertices:
            #Plota os vértices
            x,y = self.coords()
            
            if mirror_y:
                yy = []
                for i in range(len(y)):
                    yy.append(max_y - y[i])
                    
                y = tuple(yy)
            
            plt.scatter(x,y)
        
        plt.show()
    
        
        
        
        
        