#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import getrandbits
from src.Util import *

# Constantes
# Décalage de R bits
R = 49
# premier tweak sur 64 bits (cogranne)
tweak0 = 99111103114097110110101
# second tweak sur 64 bits (gs15love)
tweak1 = 103115049053108111118101
tweak2 = tweak0 ^ tweak1
tweaks = [tweak0, tweak1, tweak2]
# soit 0x1bd11bdaa9fc1a22 en hexa C = constante pour la génération des clés des tournées
C = 513129967392069919254


# Création / génération de la clé symétrique
def keygen(L_block, fichier):
    key = []
    hexkey = []
    k = 0
    for i in range(0, int(L_block/64) - 1):
        n = getrandbits(64)
        key.append(n)
        k ^= n
        hexk = int2hexa(n)
        # padding pour que le nombre convertis en hex soit sur 16bits
        if len(hexk) != 16:
            pad = "0"
            hexk = (16 - (len(str(hexk)))) * pad + str(hexk)
            hexkey.append(hexk)
        else:
            hexkey.append(hexk)
        # keyuser est la clé symétrique que l'on va afficher à l'utilisateur
        keyuser = ""
        # pour qu'il la note et s'ne serve pour le déchiffrement
        for i in hexkey:
            keyuser += i
    k ^= C
    key.append(k)
    return key, keyuser


def keygenturn(key):
    N = len(key) - 1
    VingtKeys = []
    k = 0
    for i in range(0, 20):
       tabKey = []
       for n in range(0, (N - 3)):
          t = key[(i + n) % (N + 1)]
          tabKey.append(t)
          k ^= t
       # N - 3
       n = N - 3
       t = (key[(i + n) % (N + 1)]) + (tweaks[i % 3])
       # We want t % 2^64
       # We truncate the hexadecimal characters over the range of 2^64
       tHex = hex(t)
       tStr = str(tHex)
       tStr = tStr[len(tStr)-16:len(tStr)]
       t = int(tStr, 16)
       # cela calcul le modulo sans calculer 2^64 même si les puissances de 2 sont optimiser sur les processeur
       tabKey.append(t)
       k ^= t
       # N - 2
       n = N - 2
       t = (key[(i + n) % (N + 1)]) + (tweaks[(i + 1) % 3]) % (2**64)
       tabKey.append(t)
       k ^= t
       # N - 1
       n = N - 1
       t = (key[(i + n) % (N + 1)]) + i % (2**64)
       tabKey.append(t)
       k ^= t
       k ^= C
       # k est le dernier mot de 64 bits kn = k0+..+kn-1+C
       tabKey.append(k)
       VingtKeys.append(tabKey)
    return VingtKeys


def mixcolumn(datalist):
    # en fonction de la taille du block on execute 2, 4 ou 8 fois le mélange
    datalistmix = []
    for i in range(0, len(datalist) - 1, 2):
        m11 = additionMod(intToByteArray(datalist[i]), intToByteArray(datalist[i + 1]))
        m11 = strToInt(m11)

        Rotation = ROTD(intToByteArray(datalist[(i + 1)]))

        m22 = xor_function(intToByteArray(m11), intToByteArray(Rotation))
        m22 = strToInt(m22)
        datalistmix.append(m11)
        datalistmix.append(m22)
    return datalistmix


def inv_mixcolumn(datalist):
    # en fonction de la taille du block on execute 2, 4 ou 8 fois le mélange
    datalist_unmix = []
    for i in range(0, len(datalist) - 1, 2):
        varXor = xor_function(intToByteArray(datalist[i]), intToByteArray(datalist[(i + 1)]))
        m2 = ROTG(varXor)
        m1 = soustracMod(intToByteArray(datalist[i]), intToByteArray(m2))
        m1 = strToInt(m1)
        datalist_unmix.append(m1)
        datalist_unmix.append(m2)
    return datalist_unmix


def permute(n):
    # invertion de l'ordre des mots
    return list(reversed(n))


def ECB_threefish_cipher(datalist, tabkeys):
    encryp_list = []
    for j in datalist:
        for k in range(0, 19):
            j = addition_modulaire_listes(j, tabkeys[k])
            for i in range(4):
                j = mixcolumn(j)
                j = permute(j)
        j = addition_modulaire_listes(j, tabkeys[19])
        encryp_list.append(j)
    return encryp_list


def ECB_threefish_decipher(datalist, tabkeys):
    decrypt_list = []
    for j in datalist:
        counter = 18
        j = soustraction_modulaire_listes(j, tabkeys[19])
        for k in range(0, 19):
            for i in range(4):
                j = permute(j)
                j = inv_mixcolumn(j)
            j = soustraction_modulaire_listes(j, tabkeys[counter])
            counter -= 1
        decrypt_list.append(j)
    return decrypt_list


# Todo : terminer CBC cipher and decipher function
def CBC_threefish_cipher(datalist, tabkeys, L_bloc):
    encryp_list = []
    for j in datalist:
        for k in range(0, 19):
            j = addition_modulaire_listes(j, tabkeys[k])
            for i in range(4):
                j = mixcolumn(j)
                j = permute(j)
        j = addition_modulaire_listes(j, tabkeys[19])
        encryp_list.append(j)
    return encryp_list


def CBC_threefish_decipher(datalist, tabkeys, L_bloc):
    decrypt_list = []
    for j in datalist:
        counter = 18
        j = soustraction_modulaire_listes(j, tabkeys[19])
        for k in range(0, 19):
            for i in range(4):
                j = permute(j)
                j = inv_mixcolumn(j)
            j = soustraction_modulaire_listes(j, tabkeys[counter])
            counter -= 1
        decrypt_list.append(j)
    return decrypt_list


def ROTD(Barray):
    longBarray = len(Barray)
    ROTDBarray = Barray[(longBarray - R):longBarray] + Barray[0:(longBarray - R)]
    ROTDBarray = strToInt(ROTDBarray)
    # return an int value
    return ROTDBarray


def ROTG(Barray):
    longBarray = len(Barray)
    ROTGBarray = Barray[R:longBarray] + Barray[0:R]
    ROTGBarray = strToInt(ROTGBarray)
    # return an int value
    return ROTGBarray


def IV_function(L_bloc):
    IV = []
    for i in range(0, int(L_bloc / 64)):
        IV.append(getrandbits(64))
    return IV
