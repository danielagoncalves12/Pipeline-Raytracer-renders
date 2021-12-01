from ponto_48579 import Ponto3D
from cor_rgb_48579 import CorRGB

class LuzPontual:

    def __init__(self, posicao, intensidade_ambiente, intensidade_difusa, intensidade_especular):
        '''Construtor
        :param posicao: Posicao da luz.
        :param intensidade_ambiente: Intensidade Ambiente.
        :param intensidade_difusa: Intensidade Difusa.
        :param intensidade_especular: Intensidade Especular.'''
 
        self.posicao               = posicao
        self.intensidade_ambiente  = intensidade_ambiente
        self.intensidade_difusa    = intensidade_difusa
        self.intensidade_especular = intensidade_especular

    def __repr__(self):
        '''Representação da LuzPontual.
        :return: LuzPontual em String.'''

        return 'LuzPontual(' + str(self.posicao) + ', ' \
               + str(self.intensidade_ambiente) + ', ' \
               + str(self.intensidade_difusa) + ', ' \
               + str(self.intensidade_especular) + ')'

    def get_posicao(self):
        ''':return: Posição da LuzPontual.'''

        return self.posicao

    def get_intensidade_ambiente(self):
        ''':return: Intensidade Ambiente.'''

        return self.intensidade_ambiente

    def get_intensidade_difusa(self):
        ''':return: Intensidade Difusa.'''

        return self.intensidade_difusa

    def get_intensidade_especular(self):
        ''':return: Intensidade Especular.'''

        return self.intensidade_especular
        

if __name__ == '__main__':
    
    # teste ao construtor
    posicao = Ponto3D(1.0, 2.0, 3.0)
    i_ambiente = CorRGB(0.1, 0.2, 0.3)
    i_difusa = CorRGB(0.4, 0.5, 0.6)
    i_especular = CorRGB(0.7, 0.8, 0.9)
    luz = LuzPontual(posicao, i_ambiente, i_difusa, i_especular)

    # teste a __repr__
    print(luz)

    # teste a get_posicao
    print(luz.get_posicao())

    # teste a get_intensidade_ambiente
    print(luz.get_intensidade_ambiente())

    # teste a get_intensidade_difusa
    print(luz.get_intensidade_difusa())


    # teste a get_intensidade_especular
    print(luz.get_intensidade_especular())
