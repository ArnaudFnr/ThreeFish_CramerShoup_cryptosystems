#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Menu import *
from Cramer_Shoup import *
import binascii

def main():
    x = show()
    apply(x)

if __name__ == "__main__":
    x = 'y'
    while x == 'y' or x == 'Y':


        #toto = 'C:/Users/aurélien/Google Drive/DGSE.txt'
        #fich = open(toto, "rb")
        #data = fich.read()
        #print("La taille du fichier est : ", len(data))
        #print(binascii.hexlify(data))
        #fich.close()

        main()
        x = 'z'
        while x != 'y' and x != 'Y' and x != 'n' and x != 'N':
            x = input("Recommencer ? (y/n)")