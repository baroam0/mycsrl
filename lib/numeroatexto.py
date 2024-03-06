

from .nw import num2words

def numtxt(valor):
    valor = '%.2f' % valor
    valor_total = str(valor).split(".")
    valor_entero = num2words(int(valor_total[0]), lang="es")
    resultado = str(valor_entero).upper() + " CON " + str(valor_total[1]) + "/100 CENTAVOS"
    return resultado


def numerotxt(valor):
    valor_letras = num2words(int(valor), lang="es").upper()
    return valor_letras

