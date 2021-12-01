from ponto_48579 import Ponto3D
from matriz_48579 import Matriz
from vetor_48579 import Vetor3D
from reta_48579 import Reta

class Camara:

    def __init__(self, posicao, olhar_para, vertical, distancia_olho_plano_projecao,
                 largura_retangulo_projecao, altura_retangulo_projecao,
                 resolucao_horizontal, resolucao_vertical):
        '''Construtor 

        :param posicao: Posicao da camara
        :param olhar_para: Para onde a camara esta a olhar
        :param vertical: Posicao vertical da camara
        :param distancia_olho_plano_projecao: A distancia entre o olho e o plano de projecao
        :param largura_retangulo_projecao: Largura do retangulo de projecao
        :param altura_retangulo_projecao: Altura do retangulo de projecao
        :param resolucao_horizontal: Resolucao horizontal
        :param resolucao_vertical: Resolucao vertical'''

        self.posicao                       = posicao
        self.olhar_para                    = olhar_para
        self.vertical                      = vertical
        self.distancia_olho_plano_projecao = distancia_olho_plano_projecao
        self.largura_retangulo_projecao    = largura_retangulo_projecao
        self.altura_retangulo_projecao     = altura_retangulo_projecao
        self.resolucao_horizontal          = resolucao_horizontal
        self.resolucao_vertical            = resolucao_vertical

        eixo_z      = (olhar_para - posicao).versor()
        self.eixo_z = eixo_z

        eixo_y      = (vertical + eixo_z * (-1.0 * vertical.interno(eixo_z))).versor()
        self.eixo_y = eixo_y

        eixo_x      = eixo_z.externo(eixo_y)
        self.eixo_x = eixo_x

        incremento_horizontal      = largura_retangulo_projecao / resolucao_horizontal
        self.incremento_horizontal = incremento_horizontal

        incremento_vertical      = altura_retangulo_projecao / resolucao_vertical
        self.incremento_vertical = incremento_vertical

        canto_superior_esquerdo_x      = -largura_retangulo_projecao / 2.0 + incremento_horizontal / 2.0
        self.canto_superior_esquerdo_x = canto_superior_esquerdo_x

        canto_superior_esquerdo_y      = altura_retangulo_projecao / 2.0 - incremento_vertical / 2.0
        self.canto_superior_esquerdo_y = canto_superior_esquerdo_y

        canto_superior_esquerdo_z      = distancia_olho_plano_projecao
        self.canto_superior_esquerdo_z = canto_superior_esquerdo_z

        matriz = Matriz(4, 4)
        ex = [eixo_x.get_x(), eixo_x.get_y(), eixo_x.get_z(), 0.0]
        ey = [eixo_y.get_x(), eixo_y.get_y(), eixo_y.get_z(), 0.0]
        ez = [eixo_z.get_x(), eixo_z.get_y(), eixo_z.get_z(), 0.0]
        p  = [posicao.get_x(), posicao.get_y(), posicao.get_z(), 1.0]

        matriz.set_coluna(1, ex)
        matriz.set_coluna(2, ey)
        matriz.set_coluna(3, ez)
        matriz.set_coluna(4, p)

        self.matriz = matriz


        # Matriz perspetiva
        matriz_pers = Matriz(4, 4)
   
        # d = Distancia do olho ao plano de projecao
        d = self.distancia_olho_plano_projecao

        matriz_pers.set_linha(1, [1.0, 0.0, 0.0, 0.0])
        matriz_pers.set_linha(2, [0.0, 1.0, 0.0, 0.0])
        matriz_pers.set_linha(3, [0.0, 0.0, 1.0, 0.0])
        matriz_pers.set_linha(4, [0.0, 0.0, 1.0/d, 0.0])

        self.matriz_perspetiva = matriz_pers


    def __repr__(self):
        '''Representação dos dados da camara.

        :return: String com a representação dos dados.'''

        return 'Camara(' + str(self.posicao) + ',\n ' \
               + str(self.olhar_para) + ',\n ' \
               + str(self.vertical) + ',\n ' \
               + str(self.distancia_olho_plano_projecao) + ',\n ' \
               + str(self.largura_retangulo_projecao) + ',\n ' \
               + str(self.altura_retangulo_projecao) + ',\n ' \
               + str(self.resolucao_horizontal) + ',\n ' \
               + str(self.resolucao_vertical) + ',\n ' \
               + str(self.eixo_x) + ',\n ' \
               + str(self.eixo_y) + ',\n ' \
               + str(self.eixo_z) + ',\n ' \
               + str(self.incremento_horizontal) + ',\n ' \
               + str(self.incremento_vertical) + ',\n ' \
               + str(self.canto_superior_esquerdo_x) + ',\n ' \
               + str(self.canto_superior_esquerdo_y) + ',\n ' \
               + str(self.canto_superior_esquerdo_z) + ',\n ' \
               + str(self.matriz) + ')'
    
    def get_posicao(self):
        '''Posição da camara. 

        :return: Ponto3D onde a camara encontra se posicionada.'''

        return self.posicao

    def get_resolucao_vertical(self):
        '''Resolução vertical. 

        :return: Comprimento da resolucao vertical.'''

        return self.resolucao_vertical

    def get_resolucao_horizontal(self):
        '''Resolução horizontal. 

        :return: Comprimento da resolucao horizontal.'''

        return self.resolucao_horizontal

    def get_pixel_local(self, linha, coluna):
        '''Pixel que encontra-se na linha e coluna recebida. 

        :return: Ponto3D que encontra se na linha 'linha' e coluna 'coluna'.'''

        pixel_x = self.canto_superior_esquerdo_x + (coluna - 1) * \
                  self.incremento_horizontal

        pixel_y = self.canto_superior_esquerdo_y - (linha - 1) * \
                  self.incremento_vertical

        pixel_z = self.canto_superior_esquerdo_z

        return Ponto3D(pixel_x, pixel_y, pixel_z)

    def local_para_global(self, ponto):
        '''Transforma o ponto local (coordenadas da camara) em um ponto
        global (coordenadas do mundo). 

        :return: Respetivo Ponto3D nas coordenadas do mundo.'''
        mlocal = Matriz(4, 1)
        llocal = [ponto.get_x(), ponto.get_y(), ponto.get_z(), 1.0]
        mlocal.set_coluna(1, llocal)

        mglobal = self.matriz * mlocal

        global_w = mglobal.get_entrada(4, 1)
        global_x = mglobal.get_entrada(1, 1) / global_w     
        global_y = mglobal.get_entrada(2, 1) / global_w   
        global_z = mglobal.get_entrada(3, 1) / global_w   

        return Ponto3D(global_x, global_y, global_z)

    def get_pixel_global(self, linha, coluna):
        '''Pixel na linha 'linha' e coluna 'coluna'. 

        :return: Pixel global.'''

        pixel_local  = self.get_pixel_local(linha, coluna)
        pixel_global = self.local_para_global(pixel_local)

        return pixel_global


    def matriz_inversa(self):
        '''Calcula Matriz inversa do atributo Matriz, as coordenadas são homogeneas
        e o referencial R' é ortonormodo, isto é os vetores do referencial são perpendiculares
        dois a dois e são versores. 

        :return: Matriz invertida.'''  

        # Atributo matriz - Das coordenadas da camara R', para as coordenadas do mundo R
        # Matriz inversa do atributo matriz - Das coordenadas do mundo R, para as coordenadas da camara R'

        mat     = self.matriz
        inv     = Matriz(4, 4)
        posicao = self.posicao
        
        # Posicao da camara
        p1 = posicao.get_x()
        p2 = posicao.get_y()
        p3 = posicao.get_z()

        # Valores do atributo matriz
        ex = [mat.get_entrada(1, 1), mat.get_entrada(2, 1), mat.get_entrada(3, 1), 0.0]
        ey = [mat.get_entrada(1, 2), mat.get_entrada(2, 2), mat.get_entrada(3, 2), 0.0]
        ez = [mat.get_entrada(1, 3), mat.get_entrada(2, 3), mat.get_entrada(3, 3), 0.0]

        # Matriz de transformacao inversa
        p = [p1 * (-mat.get_entrada(1, 1)) + p2 * (-mat.get_entrada(1, 2)) + p3 * (-mat.get_entrada(1, 3))
            ,p1 * (-mat.get_entrada(2, 1)) + p2 * (-mat.get_entrada(2, 2)) + p3 * (-mat.get_entrada(2, 3))
            ,p1 * (-mat.get_entrada(3, 1)) + p2 * (-mat.get_entrada(3, 2)) + p3 * (-mat.get_entrada(3, 3))
            ,1.0]

        # (Transposta de ex, ey, ez)
        inv.set_coluna(1, ex)
        inv.set_coluna(2, ey)
        inv.set_coluna(3, ez)
        inv.set_coluna(4, p)

        return inv

    def get_ponto_local(self, ponto_global):
        '''Transforma o ponto global (coordenadas do mundo) em
        um ponto local (coordenadas da camara). 

        :return: Respetivo Ponto3D nas coordenadas da camara.'''

        # Ponto Local - nas coordenadas da camara (local)
        # Ponto Global - nas coordenadas do mundo (global)
        
        matriz_global = Matriz(4, 1)
        
        col_global = [ponto_global.get_x(), ponto_global.get_y(), ponto_global.get_z(), 1.0]
        matriz_global.set_coluna(1, col_global)

        # Mudança de referencial R -> R'
        matriz_local = self.matriz_inversa() * matriz_global

        # Pontos locais obtidos
        local_w = matriz_local.get_entrada(4, 1)
        local_x = matriz_local.get_entrada(1, 1) / local_w
        local_y = matriz_local.get_entrada(2, 1) / local_w
        local_z = matriz_local.get_entrada(3, 1) / local_w

        return Ponto3D(local_x, local_y, local_z)


    def get_vetor_local(self, vetor_global):
        '''Transforma o vetor global (coordenadas do mundo) em
        um vetor local (coordenadas da camara). 

        :return: Respetivo Vetor3D nas coordenadas da camara.'''

        # Vetor Local - nas coordenadas da camara (local)
        # Vetor Global - nas coordenadas do mundo (global)
        
        matriz_global = Matriz(4, 1)
 
        col_global = [vetor_global.get_x(), vetor_global.get_y(), vetor_global.get_z(), 0.0]
        matriz_global.set_coluna(1, col_global)

        # Mudança de referencial R -> R'
        matriz_local = self.matriz_inversa() * matriz_global

        # Não divide se pelo local_w porque o valor é igual a 0
        local_x = matriz_local.get_entrada(1, 1)   
        local_y = matriz_local.get_entrada(2, 1)   
        local_z = matriz_local.get_entrada(3, 1)

        return Vetor3D(local_x, local_y, local_z)


    def projeta(self, ponto_local):
        '''Projeta o ponto local (do Triangulo)
        no plano de projecao da camara. 

        :return: Ponto3D local projetado.'''    

        ponto = Matriz(4, 1)
        ponto.set_coluna(1, [ponto_local.get_x(), ponto_local.get_y(), ponto_local.get_z(), 1.0])
       
        mat = self.matriz_perspetiva * ponto

        # Coordenadas do ponto projetado
        pw = mat.get_entrada(4,1)
        px = mat.get_entrada(1,1) / pw
        py = mat.get_entrada(2,1) / pw
        pz = mat.get_entrada(3,1) / pw
        
        ponto_projetado = Ponto3D(px, py, pz)
 
        return ponto_projetado
    

    def em_pixels(self, ponto_local):
        '''Encontra os pixeis do ponto local recebido. 

        :return: Tuplo com os pixeis.'''

        x = ponto_local.get_x()
        y = ponto_local.get_y()
        
        px = round((x - self.canto_superior_esquerdo_x) \
                   /self.incremento_horizontal)

        py = round((self.canto_superior_esquerdo_y - y) \
                   /self.incremento_vertical)

        return [px, py]

    
if __name__ == '__main__':
    
    # teste ao construtor
    posicao    = Ponto3D(0.0, 0.0, 3.0)
    olhar_para = Ponto3D(0.0, 0.0, 0.0)
    vertical   = Vetor3D(0.0, 1.0, 0.0)
    distancia_olho_plano_projecao = 2.0
            
            
    largura_retangulo_projecao    = 4.0
    altura_retangulo_projecao     = 2.0
    resolucao_horizontal          = 8
    resolucao_vertical            = 4
    camara = Camara(posicao, olhar_para, vertical, distancia_olho_plano_projecao,largura_retangulo_projecao, altura_retangulo_projecao,resolucao_horizontal, resolucao_vertical)        

    print(camara.matriz)
    print()
    print(camara.matriz_inversa())
    # teste ao __repr__
    print(camara)

    # teste a get_posicao
    print(camara.get_posicao())

    # teste a get_resolucao_vertical
    print(camara.get_resolucao_vertical())

    # teste a get_resolucao_horizontal
    print(camara.get_resolucao_horizontal())

    # teste a get_pixel_local
    print('sistema de coordenadas LOCAL')
    print('canto superior esquerdo =')
    p1 = camara.get_pixel_local(1, 1)
    print(p1)
    print('canto superior direito =')
    p2 = camara.get_pixel_local(1, 8)
    print(p2)
    print('canto inferior esquerdo =')
    p3 = camara.get_pixel_local(4, 1)
    print(p3)
    print('canto inferior direito =')
    p4 = camara.get_pixel_local(4, 8)
    print(p4)

    print()

    # teste a local_para_global
    print('sistema de coordenadas GLOBAL')
    print('canto superior esquerdo =')
    p1_global = camara.local_para_global(p1)
    print(p1_global)
    print('canto superior direito =')
    p2_global = camara.local_para_global(p2)
    print(p2_global)
    print('canto inferior esquerdo =')
    p3_global = camara.local_para_global(p3)
    print(p3_global)
    print('canto inferior direito =')
    p4_global = camara.local_para_global(p4)
    print(p4_global)

    print()

    # teste a get_pixel_global
    print('sistema de coordenadas GLOBAL')
    print('canto superior esquerdo =')
    p5 = camara.get_pixel_global(1, 1)
    print(p5)
    print('canto superior direito =')
    p6 = camara.get_pixel_global(1, 8)
    print(p6)
    print('canto inferior esquerdo =')
    p7 = camara.get_pixel_global(4, 1)
    print(p7)
    print('canto inferior direito =')
    p8 = camara.get_pixel_global(4, 8)
    print(p8)

    # teste a projeta
    print()
    print(camara.projeta(Ponto3D(1,2,3)))

