

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
