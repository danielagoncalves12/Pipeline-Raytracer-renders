from vetor_48579 import Vetor3D

class Ponto3D:
    
    def __init__(self, x, y, z):
        '''Construtor
        :param x: Coordenada x do Ponto3D.
        :param y: Coordenada y do Ponto3D.
        :param z: Coordenada z do Ponto3D.'''

        self.x = x
        self.y = y
        self.z = z

    def get_x(self):
        '''Devolve o x do ponto3D.

        :return: coordenada x do ponto.'''

        return self.x

    def get_y(self):
        '''Devolve o y do ponto3D.

        :return: coordenada y do ponto.'''

        return self.y

    def get_z(self):
        '''Devolve o z do ponto3D.

        :return: coordenada z do ponto.'''

        return self.z

    def __repr__(self):
        '''Representação do Ponto3D.

        :return: Representação do Ponto3D em String.'''

        return 'Ponto3D(' + str(self.x) + ', ' + str(self.y) + ', ' \
               + str(self.z) + ')'

    def adiciona_vetor(self, um_vetor):
        '''Adiciona um vetor ao ponto

        :return: Ponto3D obtido pela adição.'''

        novo_x = self.get_x() + um_vetor.get_x()
        novo_y = self.get_y() + um_vetor.get_y()
        novo_z = self.get_z() + um_vetor.get_z()

        resultado = Ponto3D(novo_x, novo_y, novo_z)
        return resultado

    def __add__(self, um_vetor):
        '''Adiciona um vetor ao ponto (+)

        :return: Ponto3D obtido pela adição.'''

        return self.adiciona_vetor(um_vetor)

    def subtrai_ponto(self, ponto_inicial):
        '''Subtrai um ponto ao vetor

        :return: Ponto3D obtido pela subtração.'''

        novo_x = self.get_x() - ponto_inicial.get_x()
        novo_y = self.get_y() - ponto_inicial.get_y()
        novo_z = self.get_z() - ponto_inicial.get_z()

        resultado = Vetor3D(novo_x, novo_y, novo_z)
        return resultado

    def __sub__(self, ponto_inicial):
        '''Subtrai um ponto ao vetor (-)

        :return: Ponto3D obtido pela subtração.'''

        return self.subtrai_ponto(ponto_inicial)

if __name__ == '__main__':

    # teste ao construtor
    p1 = Ponto3D(1.0, 2.0, 3.0)


    # teste a get_x
    print('coordenada x de p1 = ')
    print(p1.get_x())


    # teste a get_y
    print('coordenada y de p1 = ')
    print(p1.get_y())

    # teste a get_z
    print('coordenada z de p1 = ')
    print(p1.get_z())

    # teste a __repr__
    print('p1 = ')
    print(p1)

    # teste a adiciona_vetor
    v1 = Vetor3D(10.0, 20.0, 30.0)
    p2 = p1.adiciona_vetor(v1)
    print('v1 = ')
    print(v1)
    print('p2 = ')
    print(p2)

    # teste a +
    p3 = p1 + v1
    print('p3 = p1 + v1 = ')
    print(p3)

    # teste a subtrai_ponto
    v2 = p2.subtrai_ponto(p1)
    print('v2 = ')
    print(v2)


    # teste a -
    v3 = p2 - p1
    print('v3 = ')
    print(v3)

