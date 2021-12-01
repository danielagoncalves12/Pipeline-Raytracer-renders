
def soma_produto_listas(lista1, lista2):
    '''Soma do produto de duas listas.

    :return: Soma da multiplicação dos valores das duas listas.'''

    resultado = 0.0

    for i in range(len(lista1)):
        produto = lista1[i] * lista2[i]
        resultado = resultado + produto

    return resultado

class Matriz:

    def __init__(self, numero_linhas, numero_colunas):
        '''Construtor

        :param numero_linhas: Número de linhas da Matriz.
        :param numero_colunas: Número de colunas da Matriz.'''

        self.numero_linhas = numero_linhas
        self.numero_colunas = numero_colunas

        self.linhas = []

        for m in range(numero_linhas):
            linha = []
            for n in range(numero_colunas):
                linha.append(0.0)
            self.linhas.append(linha)

    def __repr__(self):
        '''Representação da Matriz.

        :return: Representação da Matriz em String.'''

        resultado = 'Matriz(' + str(self.numero_linhas) + ', ' \
                    + str(self.numero_colunas) + ')\n'

        for m in range(self.numero_linhas):
            for n in range(self.numero_colunas):
                resultado = resultado + str(self.linhas[m][n]) + ' '
            resultado = resultado + '\n'

        return resultado

    def set_entrada(self, linha, coluna, valor):
        '''Atribui um valor à entrada na linha 'linha' e coluna 'coluna'.'''

        self.linhas[linha - 1][coluna - 1] = valor

    def get_entrada(self, linha, coluna):
        ''' Retorna o valor da linha 'linha' e coluna 'coluna'.'''

        return self.linhas[linha - 1][coluna - 1]

    def adiciona(self, outra_matriz):
        '''Soma duas matrizes.

        :return: Soma das duas matrizes.'''

        resultado = Matriz(self.numero_linhas, self.numero_colunas)

        for l in range(resultado.numero_linhas):
            for c in range(resultado.numero_colunas):

                soma = self.get_entrada(l + 1, c + 1) \
                       + outra_matriz.get_entrada(l + 1, c + 1)
                resultado.set_entrada(l + 1, c + 1, soma)
            
        return resultado

    def __add__(self, outra_matriz):
        '''Soma duas matrizes.(+)

        :return: Soma das duas matrizes.'''

        return self.adiciona(outra_matriz)

    def get_linha(self, linha):
        '''Valores guardados na linha 'linha' como lista.

        :return: Lista com os valores da linha 'linha'.'''

        resultado = []

        for c in range(self.numero_colunas):
            entrada = self.get_entrada(linha, c + 1)
            resultado.append(entrada)

        return resultado

    def get_coluna(self, coluna):
        '''Valores guardados na coluna 'coluna' como lista.

        :return: Lista com os valores da coluna 'coluna'.'''

        resultado = []

        for l in range(self.numero_linhas):
            entrada = self.get_entrada(l + 1, coluna)
            resultado.append(entrada)

        return resultado


    def multiplica(self, outra_matriz):
        '''Multiplicação de duas matrizes.

        :return: Produto da multiplicação das duas matrizes.'''

        resultado = Matriz(self.numero_linhas, outra_matriz.numero_colunas)

        for l in range(resultado.numero_linhas):
            for c in range(resultado.numero_colunas):
                linha = self.get_linha(l + 1)
                coluna = outra_matriz.get_coluna(c + 1)
                entrada = soma_produto_listas(linha, coluna)
                resultado.set_entrada(l + 1, c + 1, entrada)

        return resultado

    def multiplica_v2(self, outra_matriz):
        '''Multiplicação de duas matrizes.(Versão 2)

        :return: Produto da multiplicação das duas matrizes.'''

        resultado = Matriz(self.numero_linhas, outra_matriz.numero_colunas)

        for l in range(resultado.numero_linhas):
            for c in range(resultado.numero_colunas):
                soma = 0.0
                for k in range(self.numero_colunas):
                    soma = soma + self.get_entrada(l + 1, k + 1) \
                           * outra_matriz.get_entrada(k + 1, c + 1)
                    
                resultado.set_entrada(l + 1, c + 1, soma)
                
        return resultado

    def multiplica_escalar(self, escalar):
        '''Multiplicação da matriz por um escalar.

        :return: Produto da multiplicação da matriz por um escalar.'''

        resultado = Matriz(self.numero_linhas, self.numero_colunas)

        for l in range(resultado.numero_linhas):
            for c in range(resultado.numero_colunas):

                entrada = self.get_entrada(l + 1, c + 1) * escalar
                resultado.set_entrada(l + 1, c + 1, entrada)
            
        return resultado

    def __mul__(self, valor):
        '''Multiplicação da matriz por um escalar.(*)

        :return: Produto da multiplicação da matriz por um escalar.'''

        if isinstance(valor, Matriz):
            return self.multiplica(valor)
        else:
            return self.multiplica_escalar(valor)

    def det_2x2(self):
        '''Calcula o determinante de uma matriz 2x2.

        :return: Determinante da matriz 2x2.'''

        a = self.linhas[0][0]
        b = self.linhas[0][1]
        c = self.linhas[1][0]
        d = self.linhas[1][1]

        return a*d - b*c

    def det_3x3(self):
        '''Calcula o determinante de uma matriz 3x3.

        :return: Determinante da matriz 3x3.'''

        a = self.get_entrada(1, 1)
        b = self.get_entrada(1, 2)
        c = self.get_entrada(1, 3)
        d = self.get_entrada(2, 1)
        e = self.get_entrada(2, 2)
        f = self.get_entrada(2, 3)
        g = self.get_entrada(3, 1)
        h = self.get_entrada(3, 2)
        i = self.get_entrada(3, 3)

        return a*e*i + b*f*g + c*d*h - g*e*c - h*f*a - i*d*b

    def sub_matriz(self, linha_a_remover, coluna_a_remover):
        '''Encontra uma sub matriz dentro da Matriz.

        :return: Sub matriz da Matriz.'''

        resultado = Matriz(self.numero_linhas - 1, self.numero_colunas - 1)

        for l in range(resultado.numero_linhas):
            for c in range(resultado.numero_colunas):
                ll = l
                cc = c
                if l >= linha_a_remover - 1:
                    ll = l + 1
                if c >= coluna_a_remover - 1:
                    cc = c + 1
                    
                entrada = self.get_entrada(ll + 1, cc + 1)
                resultado.set_entrada(l + 1, c + 1, entrada)

        return resultado

    def det(self):
        '''Calcula o determinante de uma matriz.

        :return: Determinante de qualquer matriz.'''

        if self.numero_linhas == 1:
            return self.get_entrada(1, 1)
        elif self.numero_linhas == 2:
            return self.det_2x2()
        elif self.numero_linhas == 3:
            return self.det_3x3()
        else:
            soma = 0.0
            for j in range(self.numero_linhas):
                soma = soma + (-1.0)**(1+j+1)*self.get_entrada(1, j+1) \
                       * self.sub_matriz(1, j+1).det()           
            return soma

    def transposta(self):
        '''Calculo da matriz transposta da matriz.

        :return: Matriz transposta.'''

        resultado = Matriz(self.numero_colunas, self.numero_linhas)

        for l in range(resultado.numero_linhas):
            for c in range(resultado.numero_colunas):
                entrada = self.get_entrada(c + 1, l + 1)
                resultado.set_entrada(l + 1, c + 1, entrada)

        return resultado

    
    def copia(self):
        '''Efetua uma cópia da matriz.

        :return: Cópia da matriz.'''

        resultado = Matriz(self.numero_linhas, self.numero_colunas)

        for l in range(resultado.numero_linhas):
            for c in range(resultado.numero_colunas):
                entrada = self.get_entrada(l + 1, c + 1)
                resultado.set_entrada(l + 1, c + 1, entrada)

        return resultado

    def set_linha(self, linha, uma_lista):
        '''Preenche a linha 'linha' com os valores de uma lista.'''

        for c in range(self.numero_colunas):
            self.set_entrada(linha, c + 1, uma_lista[c])

        return self

    def set_coluna(self, coluna, uma_lista):
        '''Preenche a coluna 'coluna' com os valores de uma lista.'''

        for l in range(self.numero_linhas):
            self.set_entrada(l + 1, coluna, uma_lista[l])

        return self

    def e(self):
        '''Método do TPC.

        :return: Matriz inversa.'''

        ## Determinante da Matriz
        detA = self.det_3x3()
      
        ########## Primeiro sistema ##########
        m1x = self.copia()
        m1y = self.copia()
        m1z = self.copia()

        m1x.set_entrada(1, 1, 1.0)
        m1x.set_entrada(2, 1, 0.0)
        m1x.set_entrada(3, 1, 0.0)

        m1y.set_entrada(1, 2, 1.0)
        m1y.set_entrada(2, 2, 0.0)
        m1y.set_entrada(3, 2, 0.0)

        m1z.set_entrada(1, 3, 1.0)
        m1z.set_entrada(2, 3, 0.0)
        m1z.set_entrada(3, 3, 0.0)

        x1 = m1x.det_3x3() / detA
        y1 = m1y.det_3x3() / detA
        z1 = m1z.det_3x3() / detA

        ########## Segundo sistema ##########
        m2x = self.copia()
        m2y = self.copia()
        m2z = self.copia()

        m2x.set_entrada(1, 1, 0.0)
        m2x.set_entrada(2, 1, 1.0)
        m2x.set_entrada(3, 1, 0.0)

        m2y.set_entrada(1, 2, 0.0)
        m2y.set_entrada(2, 2, 1.0)
        m2y.set_entrada(3, 2, 0.0)

        m2z.set_entrada(1, 3, 0.0)
        m2z.set_entrada(2, 3, 1.0)
        m2z.set_entrada(3, 3, 0.0)

        x2 = m2x.det_3x3() / detA
        y2 = m2y.det_3x3() / detA
        z2 = m2z.det_3x3() / detA

        ########## Terceiro sistema ##########
        m3x = self.copia()
        m3y = self.copia()
        m3z = self.copia()

        m3x.set_entrada(1, 1, 0.0)
        m3x.set_entrada(2, 1, 0.0)
        m3x.set_entrada(3, 1, 1.0)

        m3y.set_entrada(1, 2, 0.0)
        m3y.set_entrada(2, 2, 0.0)
        m3y.set_entrada(3, 2, 1.0)

        m3z.set_entrada(1, 3, 0.0)
        m3z.set_entrada(2, 3, 0.0)
        m3z.set_entrada(3, 3, 1.0)

        x3 = m3x.det_3x3() / detA
        y3 = m3y.det_3x3() / detA
        z3 = m3z.det_3x3() / detA

        ## inversa
        
        inversa = Matriz(3, 3)
        inversa.set_entrada(1, 1, x1)
        inversa.set_entrada(1, 2, x2)
        inversa.set_entrada(1, 3, x3)

        inversa.set_entrada(2, 1, y1)
        inversa.set_entrada(2, 2, y2)
        inversa.set_entrada(2, 3, y3)

        inversa.set_entrada(3, 1, z1)
        inversa.set_entrada(3, 2, z2)
        inversa.set_entrada(3, 3, z3)

        return inversa

if __name__ == '__main__':
    
    m1 = Matriz(3, 4)
    
    print(m1)
    
    m1.set_entrada(1, 2, 1.0)
    m1.set_entrada(2, 2, 2.0)
    m1.set_entrada(3, 2, 3.0)
    print(m1)

    print('m1 entrada 3,1 = ')
    print(m1.get_entrada(3, 1))
    print('m1 entrada 3,2 = ')
    print(m1.get_entrada(3, 2))

    m2 = m1.adiciona(m1)
    print(m2)

    m3 = m1 + m1
    print(m3)

    l3 = m3.get_linha(3)
    print(l3)

    c2 = m3.get_coluna(2)
    print(c2)

    r1 = soma_produto_listas(l3, l3)
    r2 = soma_produto_listas(c2, c2)
    print(r1)
    print(r2)

    m4 = Matriz(4, 3)
    m4.set_entrada(2, 1, 1.0)
    m4.set_entrada(2, 2, 2.0)
    m4.set_entrada(2, 3, 3.0)
    
    m5 = m1.multiplica(m4)
    m6 = m1.multiplica_v2(m4)

    print(m1)
    print(m4)
    print(m5)
    print(m6)

    m5a = m5.multiplica_escalar(-1.0)
    print(m5a)

    print(m1)
    print(m4)
    m6 = m1 * m4
    print(m6)
    m6a = m1 * 2.0
    print(m6a)

    m7 = Matriz(2, 2)
    m7.set_entrada(1, 1, 1.0)
    m7.set_entrada(1, 2, 2.0)
    m7.set_entrada(2, 1, 3.0)
    m7.set_entrada(2, 2, 4.0)
    print(m7)
    print('det(m7) = ' + str(m7.det_2x2()))

    print(m6)
    print('det(m6) = ' + str(m6.det_3x3()))

    m6b = Matriz(3, 3)
    m6b.set_entrada(1, 1, 2.0)
    m6b.set_entrada(2, 2, 3.0)
    m6b.set_entrada(3, 3, -1.0)
    print(m6b)
    print('det(m6b) = ' + str(m6b.det_3x3()))


    m8 = m6.sub_matriz(2, 2)
    print(m6)
    print(m8)

    print(m7)
    print(m7.det())
    print(m6)
    print(m6.det())
    m9 = Matriz(5, 5)
    m9.set_entrada(1, 1, 2.0)
    m9.set_entrada(2, 2, 2.0)
    m9.set_entrada(3, 3, 2.0)
    m9.set_entrada(4, 4, 2.0)
    m9.set_entrada(5, 5, 2.0)
    print(m9)
    print(m9.det())

    print(m1)
    m1t = m1.transposta()
    print(m1t)

    print(m8)
    m10 = m8.copia()
    m10.set_entrada(1, 1, -2.0)
    print(m8)
    print(m10)

    print(m9)
    m9.set_linha(5, [1.0, 2.0, 3.0, 4.0, 5.0])
    print(m9)

    m9.set_coluna(3, [10.0, 20.0, 30.0, 40.0, 50.0])
    print(m9)

    A = Matriz(5, 5)
    A.set_linha(1, [0.774, 0.079, 0.34 , 0.548, 0.462])
    A.set_linha(2, [0.737, 0.381, 0.785, 0.919, 0.255])
    A.set_linha(3, [0.956, 0.77 , 0.284, 0.858, 0.264])
    A.set_linha(4, [0.157, 0.085, 0.625, 0.074, 0.927])
    A.set_linha(5, [0.891, 0.861, 0.986, 0.125, 0.844])

    B_lista = [0.871, 0.648, 0.736, 0.009, 0.69]

    det_A = A.det()
    print('det(A) = ' + str(det_A))

    solucao = []

    for i in range(5):
        A_i = A.copia()
        A_i.set_coluna(i + 1, B_lista)
        x_i = A_i.det() / det_A # Regra de Cramer
        print('o valor da incógnita x_' + str(i+1) + ' é igual a: ' + str(x_i))
        solucao.append(x_i)

    print('verificação')
    for i in range(5):
        linha = A.get_linha(i+1)
        lado_esquerdo = soma_produto_listas(linha, solucao)
        lado_direito = B_lista[i]
        print('equação ' + str(i+1) + ': ' + str(lado_esquerdo) + ' = ' \
              + str(lado_direito))

    print('verificação com 3 casas decimais')
    for i in range(5):
        linha = A.get_linha(i+1)
        lado_esquerdo = round(soma_produto_listas(linha, solucao), 3)
        lado_direito = B_lista[i]
        print('equação'+ str(i+1) +':'+ str(lado_esquerdo) +'=' \
              + str(lado_direito))

    # TPC 5

    mtpc = Matriz(3, 3)
    mtpc.set_entrada(1, 1, 0.0)
    mtpc.set_entrada(1, 2, 1.0)
    mtpc.set_entrada(1, 3, 2.0)
    mtpc.set_entrada(2, 1, 1.0)
    mtpc.set_entrada(2, 2, -2.0)
    mtpc.set_entrada(2, 3, 1.0)
    mtpc.set_entrada(3, 1, 0.0)
    mtpc.set_entrada(3, 2, 3.0)
    mtpc.set_entrada(3, 3, -4.0)
    
    mtpc.e()

    
