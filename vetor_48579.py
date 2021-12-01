class Vetor3D:

    def __init__(self, x, y, z):
        '''Construtor
        :param x: Coordenada x do Vetor3D.
        :param y: Coordenada y do Vetor3D.
        :param z: Coordenada z do Vetor3D.'''

        self.x = x
        self.y = y
        self.z = z

    def get_x(self):
        '''Devolve o valor de x do vetor3D.

        :return: Coordenada x do vetor.'''

        return self.x

    def get_y(self):
        ''' Devolve o valor de y do vetor3D.

        :return: Coordenada y do vetor.'''

        return self.y

    def get_z(self):
        ''' Devolve o valor de z do vetor3D.

        :return: Coordenada z do vetor.'''

        return self.z
   
    def __repr__(self):
        '''Representação do Vetor.

        :return: Representação do Vetor3D em String.'''

        return 'Vetor3D(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def adiciona_old(self, outro_vetor):
        '''Soma de dois vetores. Versão antiga.

        :return: Resultado da soma dos vetores.'''

        resultado_x = self.x + outro_vetor.x
        resultado_y = self.y + outro_vetor.y
        resultado_z = self.z + outro_vetor.z

        resultado = Vetor3D(resultado_x, resultado_y, resultado_z)
        return resultado

    def adiciona(self, outro_vetor):
        '''Soma de dois vetores.

        :return: Resultado da soma dos vetores.'''

        resultado_x = self.get_x() + outro_vetor.get_x()
        resultado_y = self.get_y() + outro_vetor.get_y()
        resultado_z = self.get_z() + outro_vetor.get_z()

        resultado = Vetor3D(resultado_x, resultado_y, resultado_z)
        
        return resultado

    def __add__(self, outro_vetor):
        '''Soma de dois vetores. (+)

        :return: Resultado da soma dos vetores.'''

        return self.adiciona(outro_vetor)

    def multiplica_escalar(self, escalar):
        '''Multiplicação do Vetor3D por um escalar.

        :return: Produto da multiplicação.'''

        novo_x = self.get_x() * escalar
        novo_y = self.get_y() * escalar
        novo_z = self.get_z() * escalar

        resultado = Vetor3D(novo_x, novo_y, novo_z)
        
        return resultado

    def __mul__(self, escalar):
        '''Multiplicação do Vetor3D por um escalar. (*)

        :return: Produto da multiplicação.'''

        return self.multiplica_escalar(escalar)

    def comprimento(self):
        '''Calcula o comprimento do Vetor3D.

        :return: Comprimento do Vetor3D.'''

        resultado = self.get_x() ** 2.0 + self.get_y() ** 2.0 + self.get_z() ** 2.0
        resultado = resultado ** (0.5)
        
        return resultado

    def versor(self):
        '''Calcula o versor (vetor unitário) do Vetor3D.

        :return: Versor do Vetor3D.'''

        fator = 1.0 / self.comprimento()

        return self * fator

    def interno(self, outro_vetor):
        '''Calcula o produto interno de dois vetores.

        :return: Produto interno.'''

        return self.get_x() * outro_vetor.get_x() \
               + self.get_y() * outro_vetor.get_y() \
               + self.get_z() * outro_vetor.get_z()

    def externo(self, outro_vetor):
        '''Calcula o produto externo de dois vetores.

        :return: Produto externo.'''

        # determinante simbólico
        # ex ey ez
        # x1 y1 z1
        # x2 y2 z2

        # coordenadas do produto externo
        # x = y1 * z2 - z1 * y2 
        # y = -(x1 * z2 - z1 * x2)
        # z = x1 * y2 - y1 * x2

        x1 = self.get_x()
        y1 = self.get_y()
        z1 = self.get_z()

        x2 = outro_vetor.get_x()
        y2 = outro_vetor.get_y()
        z2 = outro_vetor.get_z()

        x = y1 * z2 - z1 * y2 
        y = -(x1 * z2 - z1 * x2)
        z = x1 * y2 - y1 * x2

        resultado = Vetor3D(x, y, z)
        return resultado

if __name__ == '__main__':

    v1 = Vetor3D(1.0, 2.0, 3.0)
    print("coordenada x de v1 = ")
    print(v1.get_x())

    # teste a adiciona
    v2 = Vetor3D(10.0, 20.0, 30.0)
    v3 = v1.adiciona(v2)
    print('v1 = ')
    print(v1)
    print('v2 = ')
    print(v2)
    print('v3 = ')
    print(v3)

    # teste a +
    v4 = v1 + v2
    print('v4 = ')
    print(v4)

    # teste a multiplica_escalar
    a = 2.0
    v5 = v1.multiplica_escalar(a)
    print('v5 = ')
    print(v5)

    v6 = v1 * a
    print('v6 = ')
    print(v6)


    # teste a comprimento
    v7 = Vetor3D(3.0, 0.0, 4.0)
    cv7 = v7.comprimento()
    print('v7 = ')
    print(v7)
    print('comprimento de v7 = ')
    print(cv7)

    # teste a versor
    vv7 = v7.versor()
    cvv7 = vv7.comprimento()
    print('vv7 = ')
    print(vv7)
    print('comprimento de vv7 = ')
    print(cvv7)


    # teste a interno
    print('v1 =')
    print(v1)
    print('v7 =')
    print(v7)
    iv1v7 = v1.interno(v7)
    print('v1 interno v7 = ')
    print(iv1v7)


    # teste a externo
    e = v1.externo(v7)
    print('e = v1 externo v7 = ')
    print(e)
    print('v1 interno e = ')
    print(v1.interno(e))
    print('v7 interno e = ')
    print(v7.interno(e))
