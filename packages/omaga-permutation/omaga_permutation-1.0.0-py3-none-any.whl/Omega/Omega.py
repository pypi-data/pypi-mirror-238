import sys
import argparse
import math

class Omega:
    def __init__(self,string,dec):
        self.string = string
        self.dec = dec
        self.lenstr = len(string)

    def base_montador(self):
        self.base = []
        i = self.lenstr - 1
        p = math.factorial(self.lenstr)
        while i > 0:
            q = math.factorial((self.lenstr - i) + 1)
            r = p // q
            self.base.append(r)
            i = i - 1
        return self.base

    def gera_montador(self,dec,basemontador):
        i = 0
        limite = len(basemontador)
        self.montador = []
        while i < limite:
            if dec >= math.factorial(limite + 1):
                print("Limite do digito decimal ultrapasado")
                sys.exit()
            if dec < basemontador[i]:
                self.montador.append(0)
                i = i + 1
            else:
                result = dec // basemontador[i]
                dec = dec % basemontador[i]
                self.montador.append(result)
                i = i + 1

        return self.montador

    def permuta(self,montador,nome):
        i = len(nome) - 1
        while i > 0:
            e = i
            d = e - montador[i - 1]
            nome[e],nome[d]=nome[d],nome[e]
            i = i - 1
        return nome


    def depermuta(self,montador,nome):
        i = 0
        while i < len(nome)-1:
            e = i + 1
            d = e - montador[i]
            nome[e],nome[d]=nome[d],nome[e]
            i = i + 1
        return nome

    def gera_decimal(self,basemontador,montador):
        limite = len(basemontador)
        i = 0
        dec = 0
        while i < limite:
            dec = dec + basemontador[i] * montador[i]
            i = i + 1
        return(dec)

if __name__ == '__main__':
    nome = sys.argv[1]
    a = Omega(nome, sys.argv[2])
    basemontador = a.base_montador()
    montador = a.gera_montador(int(sys.argv[2]),basemontador)
    string = a.permuta(montador,list(nome))
    decimal = a.gera_decimal(basemontador,montador)
    print (decimal, string)

