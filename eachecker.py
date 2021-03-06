#!/usr/bin/env python3

# pip3 install ecdsa
# pip3 install pysha3

# ethereum private key to public key to account address brute force attack
#
# export ethereum account list from google BigQuery open data (https://cloud.google.com -> BigQuery cosole)
#
# SELECT `address`
# FROM `bigquery-public-data.crypto_ethereum.balances`
# WHERE `eth_balance` > 1
# ORDER BY `eth_balance` DESC
# LIMIT 4000000
#
# export it to ethacclist.csv
#
# modifed from https://github.com/vkobel/ethereum-generate-wallet
#
# date : 2021.07.08

from ecdsa import SigningKey, SECP256k1
import sha3
import pandas as pd
import logging
import math
import os

LOGFILENAME = 'search_result.log'

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def genrephex(elementsize, ordernum):
    finalval = ordernum
    repcnt = (int)(64/elementsize)
    for i in range(1, repcnt):
        finalval = finalval * (int)(math.pow(16, elementsize)) + ordernum

    return finalval

def checksum_encode(addr_str): # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

def get_addr(priv_int, isprint=0):
    privinp = priv_int.to_bytes(32, byteorder='big')
    priv = SigningKey.from_string(privinp, curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak = sha3.keccak_256()
    keccak.update(pub)
    addr = '0x' + keccak.hexdigest()[24:]

    if isprint!=0:
        print("Private key:", priv.to_string().hex())
        print("Public key: ", pub.hex())
        print("Address0:   ", addr)
        f = open(LOGFILENAME,'a')
        f.write('BINGO private_key:')
        f.write(priv.to_string().hex())
        f.write('\n')
        f.write('addr:')
        f.write(addr)
        f.write('\n')
    return addr

def get_addr_from32bytes(privinp, isprint=0):
    priv = SigningKey.from_string(privinp, curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak = sha3.keccak_256()
    keccak.update(pub)
    addr = '0x' + keccak.hexdigest()[24:]

    if isprint!=0:
        print("Private key:", priv.to_string().hex())
        print("Public key: ", pub.hex())
        print("Address0:   ", addr)
        f = open(LOGFILENAME,'a')
        f.write('private_key:')
        f.write(priv.to_string().hex())
        f.write('\n')
        f.write('addr:')
        f.write(addr)
        f.write('\n')
    return addr


def get_addr_fromhexstr(priv_str, isprint=0):
    privinp = int(priv_str, 16).to_bytes(32, byteorder='big')
    priv = SigningKey.from_string(privinp, curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak = sha3.keccak_256()
    keccak.update(pub)
    addr = '0x' + keccak.hexdigest()[24:]

    if isprint!=0:
        print("Private key:", priv.to_string().hex())
        print("Public key: ", pub.hex())
        print("Address:   ", addr)
        f = open(LOGFILENAME,'a')
        f.write('private_key:')
        f.write(priv.to_string().hex())
        f.write('\n')
        f.write('addr:')
        f.write(addr)
        f.write('\n')

    return addr

def getrevsint(numval):
    revs_number = 0

    for i in range(0,64):
        remainder = numval % 16
        revs_number = (revs_number * 16) + remainder
        numval = numval // 16

    return revs_number

def example():
    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak = sha3.keccak_256()
    keccak.update(pub)
    address = keccak.hexdigest()[24:]

    print("Private key:", priv.to_string().hex())
    print("Public key: ", pub.hex())
    print("Address:    ", address)

    return

def test(addrstr):
    assert(addrstr == checksum_encode(addrstr))

def check_key(dict, key):
    ret = False
    if key in dict.keys():
        ret = True

    return ret

print('Ethereum account search tool ver 0.1\n')

#ethereum account address generation test with 32bytes hex string
get_addr_fromhexstr("0000000000000000000000000000000000000000000000000000000000000001",1)
get_addr_fromhexstr("7777777777777777777777777777777777777777777777777777777777777777",1)
get_addr_fromhexstr("3141592653589793238462643383279502884197169399375105820974944592",1)
get_addr_fromhexstr("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",1)

#ethereum account address generation test with random private key
example()

logging.info('acc list file loading..')

dict_from_csv = pd.read_csv('ethacclist.csv', dtype={'address': object}).set_index('address').T.to_dict()
print('\nsample searching on the account list/richest account for dictionary validation.. 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
print(check_key(dict_from_csv, '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'))

logging.info('start pair guessing..')

runmode = 3    # 1,2 for full searching between startn and endn (and 2=reversed bits mode), and 0 for repeated simple pattern

if runmode == 0:
    print('\nrunmode 0 : repeated simple pattern searching...')
    for i in [1,2,4,8,16,32]:
        rangeval = (int)(math.pow(16, i)) - 1
        logging.info('range : ' + str(i) + ' ' + str(rangeval))
        for j in range(1, rangeval):
            curval = genrephex(i, j)
            addr_str = get_addr(curval)

            if check_key(dict_from_csv, addr_str):
                print('BINGO:', addr_str)
                get_addr(curval, 1)

            if j % 100000 == 1:
                logging.info(curval.to_bytes(32, byteorder='big').hex())
                f = open(LOGFILENAME,'a')
                f.write(curval.to_bytes(32, byteorder='big').hex())
                f.write('\n')
elif runmode ==1:
    print('\nrunmode 1 : full sequence searching from startn to endn...')

    startn = int("0000000000000000000000000000000000000000000000000000000000000001", 16)
    endn =   int("0000000000000000000000000000000000000000000000000000000100000000", 16)

    print('\nstart num:')
    print(startn.to_bytes(32, byteorder='big').hex())
    print('end num:')
    print(endn.to_bytes(32, byteorder='big').hex())


    for i in range(startn, endn):
        addr_str = get_addr(i)
        if check_key(dict_from_csv, addr_str):
            print('BINGO:', addr_str)
            get_addr(i, 1)
        if i % 100000 == 1:
            logging.info(i.to_bytes(32, byteorder='big').hex())
            f = open(LOGFILENAME,'a')
            f.write(i.to_bytes(32, byteorder='big').hex())
            f.write('\n')
elif runmode == 2:
    print('\nrunmode 2 : full sequence searching reverse order : 0000 -> 1000 -> 2000 -> .. 0100 .. -> 1100 -> 2100..')

    startn = int("0000000000000000000000000000000000000000000000000000000003cf0961", 16)
    endn =   int("0000000000000000000000000000000000000000000000000000000100000000", 16)

    print('\nstart num:')
    print(startn.to_bytes(32, byteorder='big').hex())
    print('end num:')
    print(endn.to_bytes(32, byteorder='big').hex())

    for i in range(startn, endn):
        revsnum = getrevsint(i)
        addr_str = get_addr(revsnum)
        if check_key(dict_from_csv, addr_str):
            print('BINGO:', addr_str)
            get_addr(revsnum, 1)
        if i % 100000 == 1:
            logging.info(revsnum.to_bytes(32, byteorder='big').hex())
            f = open(LOGFILENAME,'a')
            f.write(revsnum.to_bytes(32, byteorder='big').hex())
            f.write('\n')
else: 
    i=0
    while True:
        i=i+1
        prvnum = os.urandom(32)
        addr_str = get_addr_from32bytes(prvnum)
        if check_key(dict_from_csv, addr_str):
            print('BINGO:', addr_str)
            get_addr(prvnum, 1)
        if i % 100000 == 1:
            logging.info(prvnum.hex())
            f = open(LOGFILENAME,'a')
            f.write(prvnum.hex())
            f.write('\n')
