from plano_48579 import Plano
from plano_48579 import ErroPontosColineares
from ponto_48579 import Ponto3D
from cor_rgb_48579 import CorRGB
from cor_phong_48579 import CorPhong
from matriz_48579 import Matriz

class FaceTriangular(Plano):

    def __init__(self, ponto1, ponto2, ponto3, cor_phong):
        '''Construtor

        :param ponto1: Ponto 1 do Triangulo.
        :param ponto2: Ponto 2 do Triangulo.
        :param ponto3: Ponto 3 do Triangulo.
        :param cor_phong: CorPhong da face do Triangulo.'''

        super().__init__(ponto1, ponto2, ponto3)

        self.cor_phong = cor_phong

        # Alterações a FaceTriangular

        vetor_1 = self.ponto2 - self.ponto1
        vetor_2 = self.ponto3 - self.ponto1

        self.M  = Matriz(2, 2)
        self.M.set_coluna(1, [vetor_1.get_x(), vetor_1.get_y()])
        self.M.set_coluna(2, [vetor_2.get_x(), vetor_2.get_y()])
        
        self.M1   = self.M.copia()
        self.M2   = self.M.copia()
        self.Mdet = self.M.det()

    def __repr__(self):
        '''Representação da face.
        :return: Representação da face em String.'''

        return 'FaceTriangular(' + super().__repr__() + ', ' + str(self.cor_phong) + ')'

    def get_cor_phong(self):
        '''Corphong da face do Triangulo.

        :return: CorPhong presente na face.'''

        return self.cor_phong

    def baricentricas_2D(self, um_ponto):
        '''Calcula as coordenadas baricentricas de um ponto 2D na face triangular.

        :return: Coordenadas baricentricas.'''

        matriz = Matriz(2, 2)

        # M1 e M2 sao copias da matriz M, substituir a coluna respetivamente ao 
        # eixo x na matriz M1 e coluna respestiva do eixo dos y na matriz M2.
        
        coluna = [um_ponto.get_x() - self.ponto1.get_x(), um_ponto.get_y() - self.ponto1.get_y()]
        self.M1.set_coluna(1, coluna)
        self.M2.set_coluna(2, coluna)

        detM1 = self.M1.det()
        detM2 = self.M2.det()

        # Utilizando a Regra de Cramer
        beta = detM1 / self.Mdet
        gama = detM2 / self.Mdet
        alfa = 1.0 - beta - gama

        return [alfa, beta, gama]

if __name__ == '__main__':

    # teste ao construtor

    a = Ponto3D(0.0, 0.0, 0.0)
    b = Ponto3D(1.0, 0.0, 0.0)
    c = Ponto3D(0.0, 1.0, 0.0)
    k_ambiente  = CorRGB(0.0, 0.0, 0.1)
    k_difusa    = CorRGB(0.0, 0.0, 0.75)
    k_especular = CorRGB(1.0, 1.0, 1.0)
    brilho      = 100.0
    cor = CorPhong(k_ambiente, k_difusa, k_especular, brilho)
    face1 = FaceTriangular(a, b, c, cor)
    print(face1.normal)

    print('Até aqui não foram lançadas exceções.')
    # teste à exceção ErroPontosColineares
    try:
        face2 = FaceTriangular(a, a, c, cor)
        
    except ErroPontosColineares:
        print('Ao tentar definir-se a face face2 = FaceTriangular(a, a, c, cor)')
        print('foi lançada a exceção ErroPontosColineares.')
        print('É o comportamento herdado da classe Plano.')

    # teste a __repr__
    print(face1)
    # teste a get_cor_phong
    print(face1.get_cor_phong())
