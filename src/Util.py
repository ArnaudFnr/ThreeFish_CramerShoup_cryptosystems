#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Contain  utility function such as exponentation or pgcd or read/write functions

from random import randrange
import os
import random
import fnmatch

# function that calculate the PGCD between 2 int
# input0 = int
# input1 = int
# ouput = int
def pgcd(a, b):
    # recursive calcul of a and b PGCD
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)

# function that factorize an int
# input = int
# output = list of int
def factorize(n):
    factors = []
    i = 2
    while i <= n / i:
        while n % i == 0:
            factors.append(i)
            n /= i
        i += 1

    if n > 1:
        factors.append(n)

    return factors

# Rabin-Miller primality test, use in big prime number generation
# input0 = int
# input1 = int
# ouput = boolean (true or false)
def rabin_miller(n, t = 7):
    isPrime = True
    if n < 6:
        return [not isPrime, not isPrime, isPrime, isPrime, not isPrime, isPrime][n]
    elif not n & 1:
        return not isPrime

    def check(a, s, r, n):
        x = pow(a, r, n)
        if x == 1:
            return isPrime
        for i in range(s-1):
            if x == n - 1:
                return isPrime
            x = pow(x, 2, n)
        return x == n-1

    # Find s and r such as n - 1 = 2^s * r
    s, r = 0, n - 1
    while r & 1:
        s = s + 1
        r = r >> 1

    for i in range(t):
        a = randrange(2, n-1)
        if not check(a, s, r, n):
            return not isPrime

    return isPrime

# function that convert an int value into a hexa
# input = int
# output = hexa
def int2hexa(n):
    hexk = hex(n)
    hexk = hexk.replace('\'', '')
    hexk = hexk.replace('0x', '', 1)
    hexk = str(hexk)
    return hexk

# function that read a file with binary method and can do padding if the last word
# does not match wih the blck length
# input0 = str
# input1 = int (256, 512 or 1024)
# input2 = boolean
# output = list
def readfile(fichier, L_block, do_padding):
    # file length information
    stat = os.stat(fichier)
    tailleFich = stat.st_size
    # conversion of L_block in byte
    L_block_bytes = int(L_block / 8)
    # nbr of blocks without padding
    nbr_block_nopad = int(tailleFich / L_block_bytes)
    # length of last block
    last_bloc_length = tailleFich - L_block_bytes * nbr_block_nopad
    # last_bloc is where the last block start
    last_bloc =  int(L_block_bytes * nbr_block_nopad)
    datalist = []

    for i in range(0, (tailleFich - last_bloc_length), L_block_bytes):
        with open(fichier, 'rb') as rfile:
            rfile.seek(i)
            data = rfile.read(L_block_bytes)
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)

    # do padding if the file length / L_block_bytes != int
    if last_bloc_length != 0:
        with open(fichier, 'rb') as rfile:
            rfile.seek(last_bloc)
            data = rfile.read(last_bloc_length)
            nbr_byte_pad = L_block_bytes - len(data)
            # add padding data in byte in the end of the block to inform how much padding byte has been add
            data = (nbr_byte_pad - 1) * b'0' + data + bytes([nbr_byte_pad])
            data = int.from_bytes(data, byteorder='little', signed=False)
            datalist.append(data)
    else:
        if do_padding == 1:
            pad_last_byte = bytes([L_block_bytes])
            data_pad = b'0' * (L_block_bytes - 1) + pad_last_byte
            data_pad = int.from_bytes(data_pad, byteorder='little', signed=False)
            datalist.append(data_pad)
    return datalist

# function that organised a list into a tab of list of L_block / 64
# input0 = list
# input1 = int (256,512 or 1024)
# ouput = tab of list
def organize_data_list(data_list, L_bloc):
    l = int(L_bloc / 64)
    datalistorder = []
    for i in range(0, len(data_list), l):
        datalistorder.append(data_list[i:(i + l)])
    return datalistorder

# function that add padding data if the tab of list last list length is not enought
# input0 = tab of list
# input1 = int (256,512 or 1024)
# output = tab of list
def ajout_padding(datalistorder, Length_chif_bloc):
    last_list = datalistorder[len(datalistorder) - 1]
    # if the last list length match with (4, 8 or 16) then do padding
    if len(last_list) == int(Length_chif_bloc / 64):
        # a list of N(4, 8, 16) - 1 random int of 64bits is add
        new_last_list = []
        for i in range(0, int(Length_chif_bloc / 64) - 1):
            new_last_list.append(random.getrandbits(64))
        pad_info = random.getrandbits(56)
        nbr_pad = int(Length_chif_bloc / 64)
        # convertion in byte of the random 56bit int
        pad_info = pad_info.to_bytes(7, byteorder='little', signed=False)
        pad_info = pad_info + bytes([nbr_pad])
        pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
        # info add in new list
        new_last_list.append(pad_info)
        # add new list in datalistorder
        datalistorder.append(new_last_list)
    else:
        # if only one word need to be add in the last list
        if len(last_list) + 1 == int(Length_chif_bloc / 64):
            nbr_rand = random.getrandbits(56)
            pad_info = nbr_rand.to_bytes(7, byteorder='little', signed=False)
            pad_info = pad_info + bytes([1])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            # last int add in last list
            last_list.append(pad_info)
        else:
            lenght_last_list = int(Length_chif_bloc / 64) - len(last_list)
            for i in range(0, (int(Length_chif_bloc / 64) - len(last_list)) - 1):
                last_list.append(random.getrandbits(64))
            nbr_rand = random.getrandbits(56)
            pad_info = nbr_rand.to_bytes(7, byteorder='little', signed=False)
            pad_info = pad_info + bytes([lenght_last_list])
            pad_info = int.from_bytes(pad_info, byteorder='little', signed=False)
            last_list.append(pad_info)
    return datalistorder

# function that remove padding information in a list
# input0 = tab of list
# input1 = int (256, 512 or 1024)
# output = tab of list
def remove_padding_list(data, Length_chif_bloc):
    # last list of the tab
    data_pad_list = data[len(data) - 1]
    # last element of the last list of the tab
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # last element in byte
    data_pad = data_pad.to_bytes(8, byteorder='little', signed=False)
    # value of the pading
    data_pad_nbr = int(data_pad[7])
    # if padding est is last list then we delete it
    if data_pad_nbr == int(Length_chif_bloc / 64):
        del data[len(data) - 1]
    else:
        data_pad = data_pad_list[:len(data_pad_list) - data_pad_nbr]
        del data[len(data) - 1]
        data.append(data_pad)
    return data

# function that remove padding of an int in a list
# input0 = tab of list
# input1 = int (256, 512 or 1024)
# output = tab of list
def remove_padding_data(data, L_bloc):
    L_bloc_byte = int(L_bloc / 8)
    # last list of the tab
    data_pad_list = data[len(data) - 1]
    # last element of the last list of the tab
    data_pad = data_pad_list[len(data_pad_list) - 1]
    # last element in byte
    data_pad = data_pad.to_bytes(L_bloc_byte, byteorder='little', signed=False)
    # value of the pading
    data_pad_nbr = int(data_pad[7])
    if data_pad_nbr == L_bloc_byte:
        # last element of the last list deleted
        del data_pad_list[len(data_pad_list) - 1]
    else:
        # remove padding
        data_pad_remove = data_pad[(data_pad_nbr - 1):(L_bloc_byte - 1)]
        # convertion of the new data in int
        new_data = int.from_bytes(data_pad_remove, byteorder='little', signed=False)
        # last element of the last list deleted
        del data_pad_list[len(data_pad_list) - 1]
        data_pad_list.append(new_data)
    return data, data_pad_nbr

# function that write str data in a file
# input0 = str
# input1 = str
def writefile(fichier, data):
    with open(fichier, 'w') as wfile:
        wfile.write(data)

# function that write a tab of list data into a file
# input0 = str
# input1 = tab of list
def writefilelist(fichier, data):
    with open(fichier, 'wb') as wfile:
        for i in data:
            for j in i:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)

# function that write the tab of list data into a file and remove the padding
# input0 = str
# input1 = tab of list
# input2 = int
def write_file_list_pad(fichier, data, val_last_data):
    with open(fichier, 'wb') as wfile:
        # write all the data except the last list in the tab, because there is padding
        for i in range(0, len(data) - 1):
            for j in data[i]:
                j = j.to_bytes(8, byteorder='little', signed=False)
                wfile.write(j)
        # last list
        last_list = data[len(data) - 1]
        # write all except the last int of 64bits (int where the padding is)
        for i in range(0, len(last_list) - 1):
            wdata = last_list[i].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        if val_last_data == 8:
            wdata = last_list[len(last_list) - 1].to_bytes(8, byteorder='little', signed=False)
            wfile.write(wdata)
        else:
            wdata = last_list[len(last_list) - 1].to_bytes((8 - val_last_data), byteorder='little', signed=False)
            wfile.write(wdata)

# function that read the key in a file
# input = str
# output = str
def readkey(fichier):
    with open(fichier, 'r') as rfile:
        data = rfile.read()
        return data

# function that convert a 64 bits int value into a list of str
# intput = int
# output = list of str
def intToByteArray(to_convert):
    to_convert = int(to_convert)
    output = []
    result = []
    intByte = 8
    mask = 0xFF

    for i in range(0, intByte):
        output.insert(0, to_convert & mask)
        to_convert >>= 8

    for i in output:
        i = bin(i)[2:].zfill(8)
        result.append(i)
    result = "".join(result)
    result = str(result)
    return result

# function that convert a str value into an int value
# input = str
# output = int
def strToInt(to_convert):
    return (int(to_convert, 2))

# function that xor 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def xor_function(Barray0, Barray1):
    result = str(bin(int(Barray0, 2) ^ int(Barray1, 2)))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result

# function that add 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def additionMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) + int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    return result

# function that substract 2 list of binary str value
# input0 = list of str
# input1 = list of str
# output = str
def soustracMod(Barray0, Barray1):
    result = str(bin((int(Barray0, 2) - int(Barray1, 2)) % 2**64))
    result = result.replace('0b', '', 1)
    if len(result) < 64:
        result = "0" * (64 - len(result)) + result
    return result

# function that convert a list of str into an 64bits int
# input = list of str
# output = int
def bytearrayToInt(to_convert):
    convert = "".join(to_convert)
    convert = int(convert, 2)
    return convert

# function that modular add 2 lists
# input0 = tab of list
# input1 = tab of list
# output = tab of list
def addition_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] + tab_keys[i]) % 2**64
        output. append(result)
    return output

# function that modular substract 2 lists
# input0 = tab of list
# input1 = tab of list
# output = tab of list
def soustraction_modulaire_listes(data_list, tab_keys):
    output = []
    for i in range(0, len(data_list)):
        result = (data_list[i] - tab_keys[i]) % 2 ** 64
        output.append(result)
    return output

# function that xor 2 lists
# input0 = list
# input1 = list
# output = list
def xor_2_lists(list1, list2):
    output = []
    for i in range(0, len(list1)):
        result = list1[i] ^ list2[i]
        output.append(result)
    return output

# function that rename a file
# input0 = str
# input1 = boolean
# output = nothing
def rename_fichier(path_fichier, option):
    rep = path_fichier.split("/")
    fichier = rep[len(rep) - 1]
    if option == 0:
        enc = ".encrypt"
        fichier = fichier + enc
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    else:
        fichier = fichier[:(len(fichier) - 8)]
        rep[len(rep) - 1] = fichier
        new_fichier = "/".join(rep)
    os.rename(path_fichier, new_fichier)
