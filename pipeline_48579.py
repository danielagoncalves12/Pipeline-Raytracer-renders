from imagem_48579 import Imagem
from cor_rgb_48579 import CorRGB
from ponto_48579 import Ponto3D
from cor_phong_48579 import CorPhong
from matriz_48579 import Matriz
from face_48579 import FaceTriangular
from luz_48579 import LuzPontual
from vetor_48579 import Vetor3D
from camara_48579 import Camara
from reta_48579 import Reta

class Pipeline:

    global LONGE
    LONGE = 10**6

    # Construtor
    def __init__(self, lista_faces, lista_luzes, camara, cor_fundo):
        '''Construtor
        :param lista_faces: Lista com as faces da cena.
        :param lista_luzes: Lista com as luzes da cena.
        :camara: Camara usada para observar a cena.
        :cor_fundo: Cor do fundo.'''

        self.lista_faces = lista_faces
        self.lista_luzes = lista_luzes
        self.camara      = camara
        self.cor_fundo   = cor_fundo

        self.z_buffer = []  
        num_linhas    = camara.resolucao_vertical
        num_colunas   = camara.resolucao_horizontal

        for n in range(num_linhas):
            linha = []
            for m in range(num_colunas):
                linha.append(LONGE)
            self.z_buffer.append(linha)

    
    def __repr__(self):
        '''Representacao do Pipeline.

        :return: Pipeline em String.'''

        lista1 = ''
        for face in self.lista_faces:
            lista1 = lista1 + str(face) + '\n'
            
        lista2 =  ''
        for luz in self.lista_luzes:
            lista2 = lista2 + str(luz) + '\n'
            
        camara = str(self.camara)
        fundo  = str(self.cor_fundo)
        
        return 'Pipeline(' + lista1 + ', \n' + lista2 + ', \n' \
               + camara + ', \n' + fundo + ')\n'


    def renderiza(self):
        '''Renderização Pipeline em uma imagem formato .ppm.'''
        #### PASSO 1 ####
        
        # Resolucao da imagem
        num_linhas  = self.camara.resolucao_vertical
        num_colunas = self.camara.resolucao_horizontal
        cor_pixel   = CorRGB(0.0, 0.0, 0.0)
        imagem      = Imagem(num_linhas, num_colunas)

        origem = self.camara.get_posicao()
        
        # Renderizacao da imagem
        for lin in range(num_linhas):
            linha = []
            for col in range(num_colunas):
                linha.append(cor_pixel)
            imagem.append(linha)


        #### PASSO 2 ####

        for n in range(len(self.z_buffer)):
            for m in range(len(self.z_buffer[0])):
                self.z_buffer[n][m] = LONGE

        self.renderiza_fase3()

     
    def get_lista_faces_camara(self):
        '''Lista de faces com as coordenadas dos pontos e 
        das normais convertidas para o sistema de coordenadas da câmara.

        :return: Lista faces da camara.'''

        # lista de faces no sistema de coordenadas da câmara
        lista_faces_camara = []

        # lista_faces contem faces do mundo
        for face in self.lista_faces:
            
            p1 = face.ponto1
            p2 = face.ponto2
            p3 = face.ponto3

            # Obtem as coordenadas dos pontos no sist. coordenadas da camara
            p1_camara = camara.get_ponto_local(p1)
            p2_camara = camara.get_ponto_local(p2)
            p3_camara = camara.get_ponto_local(p3)

            # Obtem a coordenada do vetor no sist. coordenadas da camara
            normal_camara = camara.get_vetor_local(face.normal)

            face_camara = FaceTriangular(p1_camara, p2_camara, p3_camara, face.cor_phong)
            face_camara.normal = normal_camara
            lista_faces_camara.append(face_camara)
            
        return lista_faces_camara


    def get_lista_faces_projetadas(self, lista_faces_camara):
        '''Projeta todas as faces da lista de faces da camara.

        :return: Lista com as faces projetadas.'''
        lista_faces_projetadas = []

        # Para cada face guardada na lista de faces da camara, projetar os 3 pontos
        for face in lista_faces_camara:
            
            p1 = face.ponto1
            p2 = face.ponto2
            p3 = face.ponto3
            
            p1_projetado = camara.projeta(p1)
            p2_projetado = camara.projeta(p2)
            p3_projetado = camara.projeta(p3)
            
            face_projetada = FaceTriangular(p1_projetado, p2_projetado, p3_projetado, face.cor_phong)

            lista_faces_projetadas.append(face_projetada)
            
        return lista_faces_projetadas

    def get_lista_faces_em_pixels(self, lista_faces_projetadas):
        '''Lista de faces onde cada face é uma lista de 3 listas.

        :return: Lista de faces em pixeis.'''
        lista_faces_em_pixels = []

        for face in lista_faces_projetadas:
   
            p1 = face.ponto1
            p2 = face.ponto2
            p3 = face.ponto3
            
            p1_pixels = camara.em_pixels(p1)
            p2_pixels = camara.em_pixels(p2)
            p3_pixels = camara.em_pixels(p3)
            face_pixels = [p1_pixels, p2_pixels, p3_pixels]

            lista_faces_em_pixels.append(face_pixels)
            
        return lista_faces_em_pixels

    def bounding_box(self, face_pixels):
        '''Cria um bounding box à volta das faces.

        :return: Coordenadas minimas e maximas da bounding box.'''

        p1x = face_pixels[0][0]
        p2x = face_pixels[1][0]
        p3x = face_pixels[2][0]

        p1y = face_pixels[0][1]
        p2y = face_pixels[1][1]
        p3y = face_pixels[2][1]

        x_max = min(max(p1x, p2x, p3x), camara.resolucao_horizontal)
        x_min = max(min(p1x, p2x, p3x), 1)
        y_max = min(max(p1y, p2y, p3y), camara.resolucao_vertical)
        y_min = max(min(p1y, p2y, p3y), 1)

        return [x_min, x_max, y_min, y_max]

    def get_lista_bounding_boxes(self, lista_faces_em_pixels):
        '''listas de bounding boxescorrepondentes a cada face triangular.

        :return: Lista de bounding boxes.'''
        lista_bbs = []
        for face in lista_faces_em_pixels:

            bb = self.bounding_box(face)
            lista_bbs.append(bb)

        return lista_bbs


    def renderiza_fase1(self):
        '''Fase 1 da renderização.

        :return: Imagem na fase 1 da renderização Pipeline.'''

        # Passo 1     
        camara    = self.camara
        n_linhas  = camara.get_resolucao_vertical()
        n_colunas = camara.get_resolucao_horizontal()
        imagem    = Imagem(n_linhas, n_colunas)

        # Passo 2
        for n in range(len(self.z_buffer)):
            for m in range(len(self.z_buffer[0])):
                self.z_buffer[n][m] = LONGE

        # operação 1 a) e b) 
        lista_faces_camara = self.get_lista_faces_camara()
 
        # operação 2 (a partir daqui não preserva a distancia)
        lista_faces_projetadas = self.get_lista_faces_projetadas(lista_faces_camara)

        # operação 3 
        lista_faces_em_pixels = self.get_lista_faces_em_pixels(lista_faces_projetadas)

        # operação 4
        lista_bounding_boxes = self.get_lista_bounding_boxes(lista_faces_em_pixels)

        # operação 5
        for n in range(len(lista_bounding_boxes)):
            
            bbox = lista_bounding_boxes[n]
            face_projetada = lista_faces_projetadas[n]

            [x_min, x_max, y_min, y_max] = bbox

            # Percorre todos os pixeis dentro da box
            # Adiciona a cor branca nos pixeis que fazem parte do triangulo
            for nx in range(x_min, x_max + 1):
                for ny in range(y_min, y_max + 1):
                    
                    pixel = camara.get_pixel_local(ny, nx)
                    [alfa, beta, gama] = face_projetada.baricentricas_2D(pixel)
                    a = alfa
                    b = beta
                    g = gama
                    if a > 0.0 and a < 1.0 and \
                       b > 0.0 and b < 1.0 and \
                       g > 0.0 and g < 1.0:
                        imagem.set_cor(ny, nx, branco)
                        
        return imagem

    def renderiza_fase2(self):
        '''Fase 2 da renderização.

        :return: Imagem na fase 2 da renderização Pipeline.'''

        # Passo 1     
        camara    = self.camara
        n_linhas  = camara.get_resolucao_vertical()
        n_colunas = camara.get_resolucao_horizontal()
        imagem    = Imagem(n_linhas, n_colunas)

        # Passo 2
        for n in range(len(self.z_buffer)):
            for m in range(len(self.z_buffer[0])):
                self.z_buffer[n][m] = LONGE

        # operação 1 a) e b) 
        lista_faces_camara = self.get_lista_faces_camara()
 
        # operação 2 (a partir daqui não preserva a distancia)
        lista_faces_projetadas = self.get_lista_faces_projetadas(lista_faces_camara)

        # operação 3 
        lista_faces_em_pixels = self.get_lista_faces_em_pixels(lista_faces_projetadas)

        # operação 4
        lista_bounding_boxes = self.get_lista_bounding_boxes(lista_faces_em_pixels)

        # operação 5
        for n in range(len(lista_bounding_boxes)):
            
            bbox = lista_bounding_boxes[n]
            face_projetada = lista_faces_projetadas[n]

            [x_min, x_max, y_min, y_max] = bbox

            # Percorre todos os pixeis dentro da box
            # Adiciona a cor branca nos pixeis que fazem parte do triangulo
            for nx in range(x_min, x_max + 1):
                for ny in range(y_min, y_max + 1):
                    
                    pixel = camara.get_pixel_local(ny, nx)
                    [alfa, beta, gama] = face_projetada.baricentricas_2D(pixel)
                    a = alfa
                    b = beta
                    g = gama
                    
                    if a > 0.0 and a < 1.0 and \
                       b > 0.0 and b < 1.0 and \
                       g > 0.0 and g < 1.0:
                        imagem.set_cor(ny, nx, branco)

                        # Baricentricas com correção de prespetiva

                        face = lista_faces_camara[n] # Pontos face nao projetada
                        az = face.ponto1.get_z()  # coordenada z do ponto1
                        bz = face.ponto2.get_z()  # coordenada z do ponto2
                        cz = face.ponto3.get_z()  # coordenada z do ponto3

                        nz = 1.0 / (((a * 1.0)/az) + ((b * 1.0)/bz) + ((g * 1.0)/cz))

                        # Pinta de amarelo se o pixel ja foi projetado antes
                        if (nz > self.z_buffer[ny][nx]):
                            imagem.set_cor(ny, nx, amarelo)

                        self.z_buffer[ny][nx] = nz

        return imagem


    def renderiza_fase3(self):
        '''Fase 3 da renderização.

        :return: Imagem na fase 3 da renderização Pipeline.''' 

        # Passo 1     
        camara    = self.camara
        n_linhas  = camara.get_resolucao_vertical()
        n_colunas = camara.get_resolucao_horizontal()
        imagem    = Imagem(n_linhas, n_colunas)

        # Passo 2
        for n in range(len(self.z_buffer)):
            for m in range(len(self.z_buffer[0])):
                self.z_buffer[n][m] = LONGE

        # operação 1 a) e b) 
        lista_faces_camara = self.get_lista_faces_camara()
 
        # operação 2 (a partir daqui não preserva a distancia)
        lista_faces_projetadas = self.get_lista_faces_projetadas(lista_faces_camara)

        # operação 3 
        lista_faces_em_pixels = self.get_lista_faces_em_pixels(lista_faces_projetadas)

        # operação 4
        lista_bounding_boxes = self.get_lista_bounding_boxes(lista_faces_em_pixels)

        # operação 5

        for n in range(len(lista_bounding_boxes)):

            bbox = lista_bounding_boxes[n]
            face_projetada = lista_faces_projetadas[n]

            [x_min, x_max, y_min, y_max] = bbox

            for nx in range(x_min, x_max + 1):
                for ny in range(y_min, y_max + 1):
                    pixel = camara.get_pixel_local(ny, nx)
                    [alfa, beta, gama] = face_projetada.baricentricas_2D(pixel)
                    a = alfa
                    b = beta
                    g = gama
                    if a > 0.0 and a < 1.0 and \
                       b > 0.0 and b < 1.0 and \
                       g > 0.0 and g < 1.0:

                        # Baricentricas com correção de prespetiva
                        face = lista_faces_camara[n] # Pontos face nao projetada
                        
                        az = face.ponto1.get_z()  # coordenada z do ponto 1
                        bz = face.ponto2.get_z()  # coordenada z do ponto 2
                        cz = face.ponto3.get_z()  # coordenada z do ponto 3

                        pz = 1.0 / (((a * 1.0) / az) + ((b * 1.0) / bz) + ((g * 1.0) / cz))

                        # Encontra a cor presente em cada face, em um certo ponto
                        corA = self.get_cor_face(face, face.ponto1) # obter a cor do ponto 1 do triangulo
                        corB = self.get_cor_face(face, face.ponto2) # obter a cor do ponto 2 do triangulo
                        corC = self.get_cor_face(face, face.ponto3) # obter a cor do ponto 3 do triangulo
                        
                        corP = (corA * ((a / az) ) + (corB * (b / bz)) + (corC * (g / cz))) * pz

                        # Se for menor que o z guardado no z_buffer é porque está visivel
                        if (pz < self.z_buffer[ny][nx]):
                            imagem.set_cor(ny, nx, corP)

                        self.z_buffer[ny][nx] = pz

        return imagem

    def get_cor_face(self, face, ponto):
        '''Calcula a cor presente na face.

        :return: CorRGB da face em um certo ponto.'''

        cor_total = CorRGB(0.0, 0.0, 0.0)
        
        cor_face = face.get_cor_phong()
        normal = face.normal
        direcao_olho = (self.camara.get_posicao() - ponto).versor

        for luz in self.lista_luzes:

            direcao_luz = (luz.get_posicao() - ponto).versor()
  
            # O renderizador Pipeline não suporta sombras, logo sombra = False
            cor = cor_face.get_cor_rgb(luz, direcao_luz, normal, direcao_olho, False)
            cor_total = cor_total + cor

        return cor_total

if __name__ == '__main__':

    # cores
    vermelho = CorRGB(1.0, 0.0, 0.0)
    verde    = CorRGB(0.0, 1.0, 0.0)
    azul     = CorRGB(0.0, 0.0, 1.0)
    amarelo  = CorRGB(1.0, 1.0, 0.0)
    ciao     = CorRGB(0.0, 1.0, 1.0)
    branco   = CorRGB(1.0, 1.0, 1.0)
    preto    = CorRGB(0.0, 0.0, 0.0)
    cinzento = CorRGB(0.25, 0.25, 0.25)
    brilho = 100.0
    
    cor_h = CorPhong(vermelho*0.25, vermelho*0.75, vermelho*0.75, brilho)
    cor_o = CorPhong(verde*0.25,    verde*0.75,    verde*0.75, brilho)
    cor_m = CorPhong(azul*0.25,     azul*0.75,     azul*0.75, brilho)
    cor_e = CorPhong(ciao*0.25,     ciao*0.75,     ciao*0.75, brilho)

    # letra H - triângulo 1
    # prefixos h v
    # prefixo h: da letra H; prefixo v: de vértice

    h1_v1 = Ponto3D(-2.5+1.5, 0.0, 0.0)
    h1_v2 = Ponto3D(-2.5+1.5, 3.0, 0.0)
    h1_v3 = Ponto3D(-3.5+1.5, 1.5, 0.0-0.5)

    h1 = FaceTriangular(h1_v1, h1_v2, h1_v3, cor_h)
    
    # letra H - triângulo 2
    h2_v1 = Ponto3D(-4.5+1.5, 0.0, 0.0-1.0)
    h2_v2 = Ponto3D(-3.5+1.5, 1.5, 0.0-0.5)
    h2_v3 = Ponto3D(-4.5+1.5, 3.0, 0.0-1.0)
    h2 = FaceTriangular(h2_v1, h2_v2, h2_v3, cor_h)

    # letra O - triângulo 1
    o1_v1 = Ponto3D(-1.25+0.75, 0.0, 0.0-0.5)
    o1_v2 = Ponto3D(-0.25+0.75, 1.5, 0.0)
    o1_v3 = Ponto3D(-2.25+0.75, 1.5, 0.0-1.0)
    o1 = FaceTriangular(o1_v1, o1_v2, o1_v3, cor_o)

    # letra O - triângulo 2
    o2_v1 = Ponto3D(-0.25+0.75, 1.5, 0.0)
    o2_v2 = Ponto3D(-1.25+0.75, 3.0, 0.0-0.5)
    o2_v3 = Ponto3D(-2.25+0.75, 1.5, 0.0-1.0)
    o2 = FaceTriangular(o2_v1, o2_v2, o2_v3, cor_o)

    # letra M - triângulo 1
    m1_v1 = Ponto3D(0.0, 0.0, 0.0-1.0)
    m1_v2 = Ponto3D(0.75, 0.0, 0.0-0.625)
    m1_v3 = Ponto3D(0.0, 3.0, 0.0-1.0)
    m1 = FaceTriangular(m1_v1, m1_v2, m1_v3, cor_m)

    # letra M - triângulo 2
    m2_v1 = Ponto3D(1.0, 1.5, 0.0-0.5)
    m2_v2 = Ponto3D(2.0, 3.0, 0.0)
    m2_v3 = Ponto3D(0.0, 3.0, 0.0-1.0)
    m2 = FaceTriangular(m2_v1, m2_v2, m2_v3, cor_m)

    # letra M - triângulo 3
    m3_v1 = Ponto3D(1.25, 0.0, 0.0-0.375)
    m3_v2 = Ponto3D(2.0, 0.0, 0.0)
    m3_v3 = Ponto3D(2.0, 3.0, 0.0)
    m3 = FaceTriangular(m3_v1, m3_v2, m3_v3, cor_m)

    # letra E - triângulo 1
    e1_v1 = Ponto3D(2.25-0.75, 2.0, 0.0-1.0)
    e1_v2 = Ponto3D(4.25-0.75, 3.0, 0.0)
    e1_v3 = Ponto3D(2.25-0.75, 3.0, 0.0-1.0)
    e1 = FaceTriangular(e1_v1, e1_v2, e1_v3, cor_e)

    # letra E - triângulo 2
    e2_v1 = Ponto3D(2.25-0.75, 1.0, 0.0-1.0)
    e2_v2 = Ponto3D(4.25-0.75, 1.5, 0.0)
    e2_v3 = Ponto3D(2.25-0.75, 2.0, 0.0-1.0)
    e2 = FaceTriangular(e2_v1, e2_v2, e2_v3, cor_e)

    # letra E - triângulo 3
    e3_v1 = Ponto3D(2.25-0.75, 0.0, 0.0-1.0)
    e3_v2 = Ponto3D(4.25-0.75, 0.0, 0.0)
    e3_v3 = Ponto3D(2.25-0.75, 1.0, 0.0-1.0)
    e3 = FaceTriangular(e3_v1, e3_v2, e3_v3, cor_e)

    lista_faces = [h1, h2, o1, o2, m1, m2, m3, e1, e2, e3]
    # lista de luzes
    luz1_posicao = Ponto3D(-3.0, 3.0, 1.5)
    luz2_posicao = Ponto3D( 3.0, 7.0, -1.9)
    luz1         =  LuzPontual(luz1_posicao, branco, branco, branco)
    luz2         =  LuzPontual(luz2_posicao, branco, branco, branco)
    lista_luzes  = [luz1, luz2]

    # a câmara
    camara_posicao                       = Ponto3D(0.0, 1.5, 3.0)
    camara_olhar_para                    = Ponto3D(0.0, 1.5, 0.0)
    camara_vertical                      = Vetor3D(0.0, 1.0, 0.0)
    camara_distancia_olho_plano_projecao = 3.0
    camara_largura_retangulo_projecao    = 8.0
    camara_altura_retangulo_projecao     = 6.0
    camara_resolucao_horizontal          = 320
    camara_resolucao_vertical            = 240

    camara = Camara(camara_posicao,
                    camara_olhar_para,
                    camara_vertical,
                    camara_distancia_olho_plano_projecao,
                    camara_largura_retangulo_projecao,
                    camara_altura_retangulo_projecao,
                    camara_resolucao_horizontal,
                    camara_resolucao_vertical)
    cor_fundo  = preto

    # teste ao construtor
    renderizador = Pipeline(lista_faces, lista_luzes, camara, cor_fundo)

    # teste à primeira fase da implementação
    imagem = renderizador.renderiza_fase1()
    print("Criando o projeto fase 1")
    imagem.guardar_como_ppm("projeto_fase1.ppm")

    # teste à segunda fase da implementação
    imagem = renderizador.renderiza_fase2()
    print("Criando o projeto fase 2")
    imagem.guardar_como_ppm("projeto_fase2.ppm")

    # teste à terceira fase da implementação
    imagem = renderizador.renderiza_fase3()
    print("Criando o projeto fase 3")
    imagem.guardar_como_ppm("projeto_fase3.ppm")
