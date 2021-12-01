from cor_rgb_48579 import CorRGB 
from ponto_48579   import Ponto3D
from luz_48579     import LuzPontual
from imagem_48579  import Imagem
from vetor_48579   import Vetor3D

class CorPhong:

    def __init__(self, k_ambiente, k_difusa, k_especular, brilho):
        ''' Construtor 

        :param k_ambiente: CorRGB ambiente
        :param k_difusa: CorRGB difusa
        :param k_especular: CorRGB especular
        :param brilho: Brilho'''

        self.k_ambiente  = k_ambiente
        self.k_difusa    = k_difusa
        self.k_especular = k_especular
        self.brilho      = brilho

    def __repr__(self):
        ''' Representação de uma CorPhong.

        :return: CorPhong representada em String.'''

        return 'CorPhong(' + str(self.k_ambiente) + ', ' \
               + str(self.k_difusa) + ', ' \
               + str(self.k_especular) + ', ' \
               + str(self.brilho) + ')'

    def get_cor_rgb(self, luz, direcao_luz, normal, direcao_olho, sombra):
        '''Calcula a CorRGB de uma face de acordo com a quantidade de luz,
        a direcao da luz, o normal, direcao_olho e se ha sombra.

        :return: CorRGB da face.'''

        cor_ambiente = self.k_ambiente * luz.get_intensidade_ambiente()

        if sombra == True:
            return cor_ambiente

        n_interno_l = normal.interno(direcao_luz)

        if n_interno_l < 0.0:
            return cor_ambiente
        
        cor_difusa = (self.k_difusa * luz.get_intensidade_difusa()) * n_interno_l

        r = direcao_luz * (-1.0) + normal * (2.0 * n_interno_l)

        cor_especular = self.k_especular * luz.get_intensidade_especular() * (abs(direcao_luz.interno(r)**self.brilho))
        
        cor_total = cor_ambiente + cor_difusa + cor_especular
        
        return cor_total

if __name__ == '__main__':
    
    # teste ao construtor
    material_k_ambiente  = CorRGB(0.0, 0.0, 0.1)
    material_k_difusa    = CorRGB(0.0, 0.0, 0.9)
    material_k_especular = CorRGB(1.0, 1.0, 1.0)
    material_brilho      = 100.0

    material_cor = CorPhong(material_k_ambiente,
                            material_k_difusa,
                            material_k_especular,
                            material_brilho)
    
    # teste a __repr__
    print(material_cor)


# teste a get_cor_rgb

    luz_posicao = Ponto3D(1.0, 0.0, 1.0)
    luz_intensidade_ambiente  = CorRGB(1.0, 1.0, 1.0)
    luz_intensidade_difusa    = CorRGB(1.0, 1.0, 1.0)
    luz_intensidade_especular = CorRGB(1.0, 1.0, 1.0)
    luz = LuzPontual(luz_posicao,
                     luz_intensidade_ambiente,
                     luz_intensidade_difusa,
                     luz_intensidade_especular)

    olho = Ponto3D(-1.0, 0.0, 1.0)
    n_pontos   = 100
    imagem     = Imagem(100, 100)
    incremento = 0.02 # 2.0/100.0
    normal     = Vetor3D(0.0, 0.0, 1.0)
    sombra     = False

    for m in range(100): # índice de linhas
        for n in range(100): # índice de colunas
            ponto        = Ponto3D(-1.0 + n*incremento, 1.0 - m*incremento, 0)
            direcao_luz  = (luz.get_posicao() - ponto).versor()
            direcao_olho = (olho - ponto).versor()
            cor = material_cor.get_cor_rgb(luz, direcao_luz, normal,direcao_olho, sombra)
            imagem.set_cor(m+1, n+1, cor)

    imagem.guardar_como_ppm('cor_phong.ppm')
