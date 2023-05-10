import bitarray
from datetime import datetime
import sys


arg1 = sys.argv[1]
arg2 = sys.argv[2]

N_BITS = 9
tam_dicionario = 2**N_BITS

def ler_arquivo():
    with open(arg2, 'rb') as file:
        bytes_array = []
        byte = file.read(1)
        while byte:
            value = int.from_bytes(byte, byteorder='big')
            bytes_array.append(value)
            byte = file.read(1)
    
    return bytes_array

def lzw_compress(data):
    dicionario = {i.to_bytes(): i for i in range(256)}
    mensagem = bitarray.bitarray()

    s = data[0]
    for char in range(len(data)):
        if (char+1) >= len(data):
            if s in dicionario:
                mensagem.extend(bin(ord(dicionario[s.to_bytes()]))[2:].zfill(N_BITS))
                break
        else:
            c = data[char+1]
        
        seq = [s.to_bytes(), c.to_bytes()]
        seq = ''.join(str(seq))
        print(seq)
        if seq in dicionario:
            s = seq
        else:
            mensagem.extend(bin(dicionario[s.to_bytes()])[2:].zfill(N_BITS))
            if len(dicionario) == tam_dicionario:
                s = c
                continue
            else:
                dicionario[len(dicionario)] = seq
                
            s = c
    
    print(dicionario)
    return mensagem
    

def lzw_decompress(data):
    dicionario = {i: i.to_bytes() for i in range(256)}
    s = ""
    msg_descomprimida = []
    index = 0

    while index < len(data):
        cod =  int(data[index:index+N_BITS].to01(), 2)
        index += N_BITS

        if cod in dicionario:
            saida_atual = dicionario[cod]
        elif cod >= len(dicionario):
            if s:
                saida_atual = s + s[0]
            else:
                saida_atual = s
        else:
            raise ValueError('Erro')

        msg_descomprimida.append(saida_atual)
        if s:
            if len(dicionario) == tam_dicionario:
                s = saida_atual
                continue
            else:
                dicionario[len(dicionario)] = s + saida_atual[0].to_bytes()
        
        s = saida_atual
    
    return msg_descomprimida

def gera_arquivo_lzw(data):
    with open('arquivo-comprimido.lzw', 'wb') as f:
        f.write(data.tobytes())

def gera_arquivo_descomprimido(data):
    if arg1 == 'mp4':
        with open('disco-descomprimido.mp4', 'wb') as f:
            for b in data:
                f.write(b)

    elif arg1 == 'txt':
        msg_nova = ''.join([chr(int.from_bytes(b, byteorder='little')) for b in data])
        with open('arquivo-descomprimido.txt', 'w') as f:
            f.write(msg_nova)

msg = ler_arquivo()
start = datetime.now()
msg_comprimida = lzw_compress(msg)
end = datetime.now()
print(f"Tempo de compressão = {end - start}")

gera_arquivo_lzw(msg_comprimida)

start = datetime.now()
msg_descomprimida = lzw_decompress(msg_comprimida)
end = datetime.now()
print(f"Tempo de descompressão = {end - start}")

gera_arquivo_descomprimido(msg_descomprimida)

