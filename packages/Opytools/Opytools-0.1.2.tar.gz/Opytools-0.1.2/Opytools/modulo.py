
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
    


class integracion:
    
        """
        Esta clase se encarga de realizar la integracion de una funcion usando el metodo de montecarlo
        Input:
        a: limite inferior
        b: limite superior
        n: numero de iteraciones
        f: funcion a integrar

        Output:
        data: plot de los datos y su ajuste
            
            """

    def __init__(self, a, b, n, f):
        """Constructor de la clase"""
        self.a = a #limite inferior
        self.b = b #limite superior
        self.n = n #numero de iteraciones
        self.f = f #funcion a integrar
        x = sp.Symbol('x')
        self.f2 = sp.lambdify('x', self.f(x), 'numpy')
    
    def montecarlo(self,n):
        """Metodo de montecarlo para calcular la integral de una funcion"""
        x = np.random.uniform(self.a, self.b, n) #genera n numeros aleatorios entre a y b
        return (self.b - self.a) * np.mean(self.f2(x)) #retorna el area
    
    def analitica(self):
        """Calcula la integral analitica de la funcion"""
        x = sp.Symbol('x')
        integral = sp.integrate(self.f(x), (x, self.a, self.b))
        return integral
    
    def run(self):
        """Metodo que ejecuta el metodo de montecarlo y grafica los resultados"""
        Y = []
        X = []
        for i in range(1,self.n):
            Y.append(self.montecarlo(i))
            X.append(i)
            if i % 1000 == 0:
                print("Iteracion {}".format(i))
        plt.plot(X,Y,color='blue',label='Montecarlo')
        plt.plot([1,self.n],[self.analitica(),self.analitica()],color='red',label='Analitica')
        plt.xlabel('Numero de iteraciones')
        plt.ylabel('Area')
        plt.title('Metodo de Montecarlo para la funcion {}'.format(self.f))
        plt.legend()
        plt.savefig('montecarlo.png')
        return True

