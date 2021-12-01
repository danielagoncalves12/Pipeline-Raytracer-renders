## Cor branca = 1.0
## Cor preta  = 0.0

class CorRGB:

    def __init__(self, red, green, blue):
        '''Construtor

        :param red: Valor da cor vermelho (0 a 255)
        :param green: Valor da cor verde (0 a 255)
        :param blue: Valor da cor azul (0 a 255)'''

        self.r = min(max(red, 0.0), 1.0)
        self.g = min(max(green, 0.0), 1.0)
        self.b = min(max(blue, 0.0), 1.0)


    def __repr__(self):
        '''Representação da CorRGB.

        :return: CorRGB representada em String.'''

        return str(int(self.r * 255.0)) + ' ' \
              + str(int(self.g * 255.0)) + ' ' \
              + str(int(self.b * 255.0))


    def soma(self, outra_cor):
        '''Soma duas cores RGB.

        :return: Nova cor resultante da soma.'''

        novo_r = self.r + outra_cor.r
        novo_g = self.g + outra_cor.g
        novo_b = self.b + outra_cor.b

        nova_cor = CorRGB(novo_r, novo_g, novo_b)
        
        return nova_cor


    def __add__(self, outra_cor):
        '''Soma duas cores RGB.(+)

        :return: Nova cor resultante da soma.'''
        
        return self.soma(outra_cor)

    def multiplica(self, outra_cor):
        '''Multiplica os valores de duas CorRGB.

        :return: Nova cor resultante da multiplicação.'''

        novo_r = self.r * outra_cor.r
        novo_g = self.g * outra_cor.g
        novo_b = self.b * outra_cor.b

        nova_cor = CorRGB(novo_r, novo_g, novo_b)
        
        return nova_cor

    def multiplica_escalar(self, escalar):
        '''Multiplica os valores da CorRGB com um escalar.

        :return: Nova cor resultante da multiplicação.'''

        novo_r = self.r * escalar
        novo_g = self.g * escalar
        novo_b = self.b * escalar

        nova_cor = CorRGB(novo_r, novo_g, novo_b)
        
        return nova_cor

    def __mul__(self, valor):
        '''Multiplicação com um escalar ou com uma CorRGB. (*)

        :return: Nova cor resultante da multiplicação.'''

        if isinstance(valor, float):
            return self.multiplica_escalar(valor)
        else:
            return self.multiplica(valor)

if __name__ == '__main__':
        
    c1 = CorRGB(1.0, 0.0, 0.0) # vermelho
    c2 = CorRGB(0.0, 1.0, 0.0) # verde
    c3 = CorRGB(0.0, 0.0, 1.0) # azul
    c4 = c1.multiplica(c2)

    print(c4)
