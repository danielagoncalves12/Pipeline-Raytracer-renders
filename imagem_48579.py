from io import StringIO
from cor_rgb_48579 import CorRGB

class Imagem:

    def __init__(self, numero_linhas, numero_colunas):
        '''Construtor

        :param numero_linhas: Número de linhas da imagem. 
        :param numero_colunas: Número de colunas da imagem.'''

        self.numero_linhas  = numero_linhas
        self.numero_colunas = numero_colunas
        self.linhas         = []

        for il in range(numero_linhas):
            linha = []
            for ic in range(numero_colunas):
                pixel = CorRGB(0.0, 0.0, 0.0)
                linha.append(pixel)
            self.linhas.append(linha)

    def __repr__(self):
        '''Representação da Imagem.

        :return: Representação da Imagem em String.'''

        resultado = StringIO()

        resultado.write('P3\n')
        resultado.write('# imagem criada em MCG/LEIM/ISEL\n')
        resultado.write(str(self.numero_colunas) + ' ')
        resultado.write(str(self.numero_linhas) + '\n')
        resultado.write('255\n')

        for linha in self.linhas:
            for pixel in linha:
                resultado.write(str(pixel) + ' ')
            resultado.write('\n')

        resultado_string = resultado.getvalue()
        resultado.close()

        return resultado_string

    def set_cor(self, linha, coluna, cor_rgb):
        ''' Muda a cor na linha 'linha' e na coluna 'coluna' para a cor recebida.'''

        self.linhas[linha - 1][coluna - 1] = cor_rgb

    def get_cor(self, linha, coluna):
        '''Pega o valor da cor na linha 'linha' e coluna 'coluna'.

        :return: Cor na linha e coluna respetivas.'''

        return self.linhas[linha - 1][coluna - 1]

    def guardar_como_ppm(self, nome_ficheiro):
        '''Guarda os dados em um ficheiro de formato ppm.'''

        ficheiro = open(nome_ficheiro, 'w')
        ficheiro.write(str(self))
        ficheiro.close()
    
    def l(self, outra_imagem):
        ''' Multiplica a imagem por outra imagem.(TPC)

        :return: Nova imagem resultante da multiplicação.'''

        nova_imagem = Imagem(self.numero_linhas, self.numero_colunas)
        
        for l in range(self.numero_linhas):
            for c in range(self.numero_colunas):
                nova_imagem.set_cor(l + 1, c + 1, self.get_cor(l + 1, c + 1) * outra_imagem.get_cor(l + 1, c + 1))
                
        return nova_imagem

    def __mul__(self, outra_imagem):
        ''' Multiplica a imagem por outra imagem.(TPC)

        :return: Nova imagem resultante da multiplicação.'''

        return self.l(outra_imagem)

if __name__ == '__main__':
    
    # teste ao construtor
    imagem1 = Imagem(5, 5)

    # teste a __repr__
    imagem2 = Imagem(300, 300)
    #print(imagem2)

    # teste a set_cor
    imagem3 = Imagem(5, 5)
    branco = CorRGB(1.0, 1.0, 1.0)
    imagem3.set_cor(3, 3, branco)
    #print(imagem3)

    # teste ao get cor
    imagem4 = Imagem(5, 5)
    branco = CorRGB(1.0, 1.0, 1.0)
    imagem4.set_cor(3, 3, branco)
    #print(imagem4.get_cor(3, 3))
    #print(imagem4.get_cor(5, 5))

    # teste a guardar_como_ppm
    imagem5 = Imagem(3, 5)
    red = CorRGB(1.0, 0.0, 0.0)
    green = CorRGB(0.0, 1.0, 0.0)
    blue = CorRGB(0.0, 0.0, 1.0)
    imagem5.set_cor(2, 2, red)
    imagem5.set_cor(2, 3, green)
    imagem5.set_cor(2, 4, blue)
    imagem5.guardar_como_ppm('imagem5.ppm')

    # teste adicional - HSV
    from colorsys import hsv_to_rgb
    linhas = 256
    colunas = 256
    imagem6 = Imagem(linhas, colunas)
    h = 130.0/360.0
    for l in range(linhas):
        s = l
        for c in range(colunas):
            v = c
            (r, g, b) = hsv_to_rgb(h, s/255.0, v/255.0)
            pixel = CorRGB(r, g, b)
            imagem6.set_cor(l+1, c+1, pixel)
    imagem6.guardar_como_ppm('imagem6.ppm')
