import math
if not "raw_input" in dir(__builtins__):
    raw_input = input
def blocoToValue(b):
    if not len(b):
        return []
    r = []
    for k in range(max(b.keys())+1):
        if k in b.keys():
            r.append(int(b[k]))
        else:
            r.append(3)
    return r
TRACE = False
# Cria lista de vizinhos dos itens dados
def vizinhos(item):
    lista_vizinhos = []
    bits_fixos = lista_bits(item)
    # Para cada bit que não muda, crie uma entrada nova
    for bit_fixo in bits_fixos:
        bloco = []
        # Para cada valor, crie um vizinho
        for valor in item:
            n = []
            # Mude apenas um bit por vez para cada entrada individual
            for bit in range(len(valor)):
                if bit == bit_fixo:
                    n.append(1-valor[bit])
                else:
                    n.append(valor[bit])
            # Agrupe por quantidade de itens
            bloco.append(n)
        # Monte a lista
        lista_vizinhos.append(tuple(bloco))
    return lista_vizinhos
# Lista os bits que não mudam de valor na lista de itens
def lista_bits(itens):
    lista = []
    # Para cada bit
    for j in range(len(itens[0])):
        igual = True
        for k in range(len(itens)-1):
            # Verifica se o bit do item atual é igual ao do proximo item
            if itens[k][j] != itens[k+1][j]:
                igual = False
                break
        if igual:
            # Adiciona na lista somente se passar pelo teste
            lista.append(j)
    return lista
# transforma um indice em vetor de bits
def indiceEmVetor(valor, bits):
    v = []
    # Para cada bit do vetor
    for i in range(bits):
        # Divida o numero por 2^i e adicione o bit lsb do resultado no vetor
        v.append((valor >> i) & 1)
    return v
# transforma um vetor de bits em um indice
def vetorEmIndice(vetor):
    v = 0
    # Para cada bit do vetor, começando pelo último valor (MSB)
    for i in reversed(vetor):
        # Multiplique o valor atual por 2 e adicione o novo bit
        v = (v << 1) + i
    return v
# calcula o numero minimo de bits necessarios para o vetor de indices
def numeroMinimoDeBits(valores, irrelevante, fixo=0):
    # maximo indice na tabela + 1 para evitar log2(0)
    # concatene 0 a lista para evitar max([])
    maxval = max(valores+irrelevante+[0])+1
    # calcule log2(maxval), arredondando para o inteiro acima
    bits = int(math.ceil(math.log(maxval)/math.log(2)))
    # no caso onde maxval é 1, numero de bits é 0.
    # o mínimo necessario deve ser 1, corrija
    if bits < 1:
        bits = 1
    if fixo:
        if fixo < bits:
            print("Numero de variaveis requisitado '%d' nao eh suficiente para definir a funcao, utilizando '%d' variaveis" % (
                fixo, bits))
            return bits
        else:
            return fixo

    return bits
# Transforma a lista de vetores na funcao do bloco
def criarBloco(vetor):
    funcao = dict()
    # somente os bits fixos
    bits = lista_bits(vetor)
    # para cada bit da funcao
    for i in bits:
        # adicione seu valor ao dicionario
        funcao[i] = vetor[0][i] == 1
    return funcao
def blocoEmTexto(bloco):
    f = []
    char_a = ord('A')
    # para cada bit do bloco

    for i in sorted(bloco):
        #    sufixo = " "
        prefixo = ""
        # se o valor do bit é 0, adicione a barra
        # if not bloco[i]: sufixo = u"\u0305"
#    if not bloco[i]: sufixo = u"'"
        if not bloco[i]:
            prefixo = u"/"
        # adicione a variavel
#    f.append(chr(char_a+i) + sufixo)
        f.append(prefixo+chr(char_a+i))
    if len(f) == 0:
        return u"1"
    return "".join(f)
def funcaoEmTexto(funcao):
    ret = []
    # para cada bloco da funcao
    for bloco in sorted(funcao, key=blocoToValue):
        # converte para texto
        ret.append(blocoEmTexto(bloco))

    if ret == []:
        return u"0"
    return u" + ".join(ret)
def calcularPeso(testados, irrelevante, vetores):
    peso = 0
    # para cada entrada nos vetores
    for v in vetores:
        k = vetorEmIndice(v)
        # incremente o peso para cada entrada ainda nao utilizada, somente se não está no irrelevante
        if not (k in testados.keys()) and not (k in irrelevante):
            peso = peso+1
    return peso
def agrupar(testados, tabela, irrelevante, vetores, identacao=">"):
    otimo = False
    if TRACE:
        print(identacao+"Vetores originais", vetores)
    blocos = vizinhos(vetores)
    maior_bloco = vetores
    peso = 0
    for bloco in blocos:
        if TRACE:
            print(identacao+"Testando vizinho", bloco)
        encontrado = True
        for v in bloco:
            # verifique se o indice existe na tabela
            indice = vetorEmIndice(v)
            if not (indice in tabela or indice in irrelevante):
                if TRACE:
                    print(identacao+" Falhou")
                encontrado = False
                break
        if encontrado:
            if TRACE:
                print(identacao+" Funcionou, testar um nivel acima")
            bloco_encontrado, otimo = agrupar(
                testados, tabela, irrelevante, vetores+list(bloco), identacao+">")
            # Calcular peso do bloco_encontrado
            novo_peso = calcularPeso(testados, irrelevante, bloco_encontrado)
            # se o novo bloco é maior que o original ou se o peso do novo bloco é maior substitua
            if (len(bloco_encontrado) > len(maior_bloco) or (len(bloco_encontrado) == len(maior_bloco) and novo_peso > peso)):
                if TRACE and peso > 0:
                    print(
                        (identacao+" Melhor bloco encontrado com peso %d, (anterior era %d), substituindo") % (novo_peso, peso))
                maior_bloco = bloco_encontrado
                peso = novo_peso
            if (otimo):
                break
            if (len(maior_bloco) == (1 << len(vetores[0]))):
                break
        else:
            if (len(vetores) == (1 << (len(vetores[0])-1))):
                otimo = True

    if TRACE:
        print(identacao+"Maior bloco encontrado", maior_bloco, ", peso %d" %
              calcularPeso(testados, irrelevante, maior_bloco))
    return (maior_bloco, otimo)
# Tabela contém os itens que são 1
# ex.: 1,2,5,7
# Irrelevante contém os items irrelevantes
# ex.: 6
#      0,1,1,0,0,1,X,1
def simplificar(tabela, irrelevante, bits=0):
    # calcule o maximo numero de variaveis
    numbits = numeroMinimoDeBits(tabela, irrelevante, bits)
    testados = dict()
    funcao = []
    # para cada entrada na tabela
    for i in tabela:
        if not i in testados.keys():
            # agrupe os valores 1, se a entrada ainda não foi utilizada antes
            if TRACE:
                print("Testando entrada da tabela")
            g, _ = agrupar(testados, tabela, irrelevante,
                           [indiceEmVetor(i, numbits)])
            # minimize e adicione o bloco na lista de funcoes
            funcao.append(criarBloco(g))
            # para cada entrada do grupo
            for v in g:
                k = vetorEmIndice(v)
                # adicione esse indice à lista de entradas já utilizadas
                testados[k] = True
    return funcao
def simplificarEmTexto(tabela, irrelevante, bits=0):
    return funcaoEmTexto(simplificar(tabela, irrelevante, bits))
def avaliar(funcao, indice, bits):
    numbits = numeroMinimoDeBits([indice], [], bits)
    v = indiceEmVetor(indice, numbits)
    valor = 0
    for bloco in funcao:
        valor_bloco = 1
        for i in reversed(list(bloco.keys())):
            if i >= numbits:
                valor_bloco = valor_bloco and (0 == bloco[i])
            else:
                valor_bloco = valor_bloco and (v[i] == bloco[i])
            if not valor_bloco:
                break
        valor = valor or valor_bloco
        if valor:
            break
    return valor


def validar(tabela, irrelevante, bits=0):
    numbits = numeroMinimoDeBits(tabela, irrelevante, bits)
    f = simplificar(tabela, irrelevante, numbits)
    for i in range(1 << numbits):
        if not (i in irrelevante):
            v = avaliar(f, i, numbits)
            if ((i in tabela and v != 1) or (not (i in tabela) and v == 1)):
                print("Falhou na validação: indice", i)
                return []
    return f
def reverseBits(v, bits):
    r = 0
    for i in range(bits):
        r = r | (((v >> i) & 1) << (bits-i-1))
    return r
def funcaoEmIndices(s, bits):
    import re
    s = s.upper()
    # Se contem caracteres invalidos, aborte
    if re.search("[^A-Z +/.]", s):
        raise Exception("Funcao contem caracteres invalidos")
    tabela = []
    bits = max(ord(max(s))-ord('A')+1, bits)

    # crie lista com variaveis esperadas baseado na funcao ou no numero de bits requisitado
    variaveis = [chr(c+ord('A')) for c in range(bits)]
    # para cada bloco da funcao
    for b in s.split("+"):
        r = 0
        # para cada letra+negacao do bloco
        bloco = list(map(lambda x: str.strip(x, " ."), re.findall(
            "(?: |[/.])?(?:[A-Z])", b.replace("//", ""))))
        utilizar_bloco = True
        for variavel in bloco:
            # Se a variavel contem a negacao, seu tamanho é 2
            if len(variavel) == 2:
                # ignore, já que esse bit é 0 para a variavel
                continue
            # calcule o indice (A=0, B=1, etc...)
            idx = ord(variavel[0]) - ord('A')

            # caso variavel e variavel' seja definido, esse bloco é sempre zero
            if "/"+variavel in bloco:
                utilizar_bloco = False
                break

            # ligue o bit correspondente ao bit encontrado
            r = r | (1 << idx)

        # caso variavel e variavel' seja definido, esse bloco é sempre zero
        if not utilizar_bloco:
            continue

        x = [r]
        # para cada variavel esperada
        for variavel in variaveis:
            # se a variavel nao explicitamente mencionada, adicione
            # o indice onde a variavel é 1 também
            # faca o mesmo para cada novo indice adicionado (recursao implementada com loop)
            if not variavel in b:
                i = len(x)
                for k in range(i):
                    idx = ord(variavel[0]) - ord('A')
                    x.append(x[k] | (1 << idx))
        # Adicione os indices na tabela, sem duplicacao
        tabela = list(set(tabela+x))
    return (tabela, bits)
if __name__ == "__main__":
    import sys
    bits = 0
    tabela = []
    irrelevante = []
    usage = '''Sintaxe: %s [tabela [irrelevante [bits]] | --help ]

'tabela' determina os índices onde o resultado da função tem que ser true.
'irrelevante' determina os índices onde o resultado da função é irrelevante.
'bits' define o número de bits que a função contém. Se não for fornecido,
  será definido à partir de 'tabela' e 'irrelevante'.
'-h' ou '--help' mostra esta ajuda.

Os argumentos 'tabela' e 'irrelevante' podem ser uma lista de índices ou uma 
  funçao. Exemplos: '0,2,3', '/A/B+/AB+AB'.
Se nemhum argumento for fornecido, a tabela de verdade será solicitada de forma
  interativa.''' % sys.argv[0]

    if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print(usage)
    else:
        if (len(sys.argv) > 1):
            if len(sys.argv) > 3:
                bits = int(sys.argv[3])
            while (True):
                try:
                    tabela = sys.argv[1].split(",")
                    if len(tabela) == 1 and tabela[0].strip() == '':
                        tabela = []
                    else:
                        tabela = [int(x, 0) for x in tabela]
                except:
                    tabela, bits = funcaoEmIndices(sys.argv[1], bits)

                if (len(sys.argv) > 2):
                    try:
                        ibits = bits
                        irrelevante = sys.argv[2].split(",")
                        if len(irrelevante) == 1 and irrelevante[0].strip() == '':
                            irrelevante = []
                        else:
                            irrelevante = [int(x, 0) for x in irrelevante]
                    except:
                        irrelevante, ibits = funcaoEmIndices(sys.argv[2], bits)
                    if (bits == ibits):
                        break
                    else:
                        bits = max(ibits, bits)
                else:
                    break
        else:
            reverse = True
            if len(sys.argv) > 1 and sys.argv[1] == "A=lsb":
                reverse = False
            bits = int(raw_input("Numero de variaveis: "))
            if (bits < 1):
                print("Entrada invalida")
                exit(1)

            for j in range(1 << bits):
                i = j
                if reverse:
                    i = reverseBits(j, bits)
                ok = False
                while (not ok):
                    ok = True
                    n = raw_input(
                        "Entre o valor para "+blocoEmTexto(criarBloco([indiceEmVetor(i, bits)]))+": ")
                    if n == 'x' or n == 'X' or n == '.':
                        irrelevante.append(i)
                    elif n == '1':
                        tabela.append(i)
                    elif n == '0':
                        pass
                    else:
                        print("Entrada invalida")
                        ok = False
        bits = numeroMinimoDeBits(tabela, irrelevante, bits)
        print("%s \"%s\" \"%s\" %d" % (sys.argv[0], ",".join(
            map(str, tabela)), ",".join(map(str, irrelevante)), bits))
        print(funcaoEmTexto(validar(sorted(tabela), irrelevante, bits)))