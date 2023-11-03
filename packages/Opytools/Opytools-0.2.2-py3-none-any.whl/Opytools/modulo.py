
class KernelFit:

    """
    Esta clase se encarga de realizar el analisis de datos usando un kernel gaussiano
    Input:  
    path: ruta del archivo csv con columnas "nuevos_casos"

    Output:
    data: plot de los datos y su ajuste

    """

    def __init__(self,path):
        self.path = path
        self.data = None
        self.casos= None
        self.fechas= None
        self.sigma= 10
        self.kernel = lambda x,N: N*np.exp(-np.abs(x)**2/(2*self.sigma))

    

    def read_data(self):
        """Lee los datos del archivo csv"""
        try:
            self.data = pd.read_csv(self.path)
            self.casos = self.data["nuevos_casos"]
            self.fechas = np.arange(0,len(self.casos),1)
        
        except:
            print("Error al leer el archivo")
        return True
    
    def calcularpunto(self,xi,N):
        """x: arreglo 
            xi: punto a evaluar
        """
        try:
            x_xi = self.fechas-xi #Resta de arreglos
            
            K = np.zeros(len(x_xi))
            for i in range(len(x_xi)):
                K[i] = self.kernel(x_xi[i],self.casos[i]) #Evaluacion del kernel
        except:
            print("Error al calcular el kernel")
        return sum(K)
    
    def fit(self):
        """Calcula el suavizado de los datos
        """
        try:
            y = []
            for i in range(len(self.fechas)):#Recorre todos los puntos
                y.append(self.calcularpunto(self.fechas[i],self.casos[i]))
        except:
            print("Error al calcular el suavizado")
        return np.array(y)
    
    def dataplot(self):
        """Retorna los datos y el suavizado
        """
        x = self.fechas
        y_data = self.casos
        y_fit = self.fit()
        return x,y_data,y_fit*max(y_data)/max(y_fit)
    
    def plot(self):
        """Grafica los datos y el suavizado"""
        
        x,yd,yf = self.dataplot()
        plt.plot(x,yd,label="Datos")
        plt.plot(x,yf,label="Suavizado")
        plt.legend()
        plt.savefig("casos.png")
        print("Terminado")
        return True
    
    def run(self):
        """Ejecuta el analisis"""
        self.read_data()    
        self.plot()
        return True
    

