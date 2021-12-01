from ponto_48579 import Ponto3D

TOLERANCIA_ZERO = 10.0**(-10)

class ErroPontosCoincidentes(Exception):
    ''' classe do erro da criação de retas com pontos coincidentes '''

class Reta:

    def __init__(self, origem, destino):
        '''Construtor
        :param origem: Coordenada de origem da Reta.
        :param destino: Coordenada de destino da Reta.''' 

        self.origem  = origem
        self.destino = destino
        vetor = destino - origem

        # if vetor.comprimento() == 0.0: proibido
        if vetor.comprimento() < TOLERANCIA_ZERO:
            raise ErroPontosCoincidentes
        
        self.vetor_diretor = vetor.versor()

    def __repr__(self):
        '''Representação da reta.

        :return: Representação da reta em String.'''

        return 'Reta(' + str(self.origem) + ', ' + str(self.destino) + ', ' \
               + str(self.vetor_diretor) + ')'

    def get_origem(self):
        '''Devolve a origem da reta.

        :return: Coordenadas da origem da reta.'''

        return self.origem

    def get_destino(self):
        '''Devolve o destino da reta.

        :return: Coordenadas do destino da reta.'''

        return self.destino

    def get_vetor_diretor(self):
        '''Devolve o vetor diretor da reta.

        :return: Coordenadas do vetor diretor da reta.'''

        return self.vetor_diretor

if __name__ == '__main__':

    # teste ao construtor
    p1 = Ponto3D(0.0, 0.0, 0.0)
    p2 = Ponto3D(0.0, 2.0, 0.0)
    r1 = Reta(p1, p2)

    print('Até aqui não foram lançadas exceções.')

    # teste à exceção ErroPontosCoincidentes
    try:
        r2 = Reta(p2, p2)
    except ErroPontosCoincidentes:
        print('Ao tentar definir-se a reta r2 = Reta(p2, p2)')

    print(r1)
    print(r1.get_origem())
    print(r1.get_destino())
    print(r1.get_vetor_diretor())
