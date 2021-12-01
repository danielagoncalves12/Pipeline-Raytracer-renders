from ponto_48579 import Ponto3D
from matriz_48579 import Matriz
from reta_48579 import Reta

TOLERANCIA_ZERO = 10.0**(-10)

class ErroPontosColineares(Exception):
    ''' exceção lançada com pontos colienares '''

class Plano:

    def __init__(self, ponto1, ponto2, ponto3):
        '''Construtor
        :param ponto1: Ponto 1 do plano.
        :param ponto2: Ponto 2 do plano.
        :param ponto3: Ponto 3 do plano.'''

        self.ponto1 = ponto1
        self.ponto2 = ponto2
        self.ponto3 = ponto3

        v12 = ponto2 - ponto1
        v13 = ponto3 - ponto1

        externo = v12.externo(v13)

        ## if externo.comprimento() == 0.0: proibido
        if externo.comprimento() < TOLERANCIA_ZERO:
            raise ErroPontosColineares

        self.normal = externo.versor()

    def __repr__(self):
        '''Representação do plano.

        :return: Representação do plano em String.'''

        return 'Plano(' + str(self.ponto1) + ', ' \
               + str(self.ponto2) + ', ' \
               + str(self.ponto3) + ', ' \
               + str(self.normal) + ')'

    def interceta_triangulo(self, reta):
        '''Verifica se a reta 'reta' interceta o triângulo.

        :return: retorna o ponto de interseção caso existir.'''

        ax = self.ponto1.get_x()
        ay = self.ponto1.get_y()
        az = self.ponto1.get_z()

        bx = self.ponto2.get_x()
        by = self.ponto2.get_y()
        bz = self.ponto2.get_z()

        cx = self.ponto3.get_x()
        cy = self.ponto3.get_y()
        cz = self.ponto3.get_z()

        vx = reta.get_vetor_diretor().get_x()
        vy = reta.get_vetor_diretor().get_y()
        vz = reta.get_vetor_diretor().get_z()

        px = reta.get_origem().get_x()
        py = reta.get_origem().get_y()
        pz = reta.get_origem().get_z()

        matriz_A = Matriz(3, 3)
        matriz_A.set_coluna(1, [bx - ax, by - ay, bz - az])
        matriz_A.set_coluna(2, [cx - ax, cy - ay, cz - az])
        matriz_A.set_coluna(3, [-vx, -vy, -vz])

        # Passo 1
        det_A = matriz_A.det()
        
        if abs(det_A) < TOLERANCIA_ZERO:
            return [False, None, None]

        # Passo 2
        matriz_t = matriz_A.copia()
        matriz_t.set_coluna(3, [px - ax, py - ay, pz - az])
        det_t = matriz_t.det()
        t = det_t / det_A

        if t < 0.0:
            return [False, None, None]
        
        # Passo 3
        matriz_tB = matriz_A.copia()
        matriz_tB.set_coluna(1, [px - ax, py - ay, pz - az])
        det_tB = matriz_tB.det()
        tB = det_tB / det_A

        if tB < 0.0 or tB > 1.0:
            return [False, None, None]

        # Passo 4
        matriz_tC = matriz_A.copia()
        matriz_tC.set_coluna(2, [px - ax, py - ay, pz - az])
        det_tC = matriz_tC.det()
        tC = det_tC / det_A

        if tC < 0.0 or tC > 1.0:
            return [False, None, None]

        # Passo 5
        tA = 1.0 - tB - tC
        
        if tA < 0.0 or tA > 1.0:
            return [False, None, None]

        # Passo 6
        A = self.ponto1
        B = self.ponto2
        C = self.ponto3
        vAB = B - A
        vAC = C - A

        ponto_intercecao = A + ((vAB * tB) + (vAC * tC))
        return [True, ponto_intercecao, t]

if __name__ == '__main__':

    # teste ao construtor
    a = Ponto3D(0.0, 0.0, 0.0)
    b = Ponto3D(2.0, 0.0, 0.0)
    c = Ponto3D(0.0, 2.0, 0.0)

    try:
        plano1 = Plano(a, b, c)
    except ErroPontosColineares:
        print('não é possível criar o plano')

    try:
        plano2 = Plano(c, b, c)
    except ErroPontosColineares:
        print('não é possível criar o plano')

    print(plano1)



    # testes a interceta_triangulo
    p1 = Ponto3D(0.5, 0.5, 10.0)
    p2 = Ponto3D(0.5, 0.5, 5.0)
    r1 = Reta(p1, p2)
    lista = plano1.interceta_triangulo(r1)

    if lista[0] == True:
        print('r1 interceta plano1.')
        print('lista[1] = interceção  ='+ str(lista[1]))
        print('lista[2] = parâmetro t ='+ str(lista[2]))
        print('interceção calculada com a equação da reta e t.')
        print('(tem que dar o mesmo que lista[1])')
        t = lista[2]
        pi = r1.get_origem() + (r1.get_vetor_diretor() * t)
        print(pi)
    else:
        print('r1 NÃO interceta plano1.')
        
    p3 = Ponto3D(2.0, 2.0, 5.0)
    r2 = Reta(p1, p3)
    lista = plano1.interceta_triangulo(r2)
    
    if lista[0] == True:
        print('r2 interceta plano1.')
        print('lista[1] = interceção  ='+ str(lista[1]))
        print('lista[2] = parâmetro t ='+ str(lista[2]))
    else:
        print('r2 NÃO interceta plano1.')
