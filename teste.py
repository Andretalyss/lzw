import bitarray
import time
from datetime import datetime

N_BITS = 9
tam_dicionario = 2**N_BITS

def ler_arquivo():
    with open('arquivo-iso.txt', 'rb') as file:
        bytes_array = []
        byte = file.read(1)
        while byte:
            value = int.from_bytes(byte, byteorder='big')
            bytes_array.append(value)
            byte = file.read(1)
    
    return bytes_array

def lzw_compress(data):
    dicionario = {chr(i): i for i in range(256)}
    mensagem = bitarray.bitarray()
    print(dicionario)

    s = chr(data[0])
    for char in range(len(data)):
        if (char+1) >= len(data):
            if s in dicionario:
                mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))
                # mensagem.append(dicionario[s])
                break
        else:
            c = chr(data[char+1])

        seq = s + c
        if seq in dicionario:
            s = seq
        else:
            mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))
            #mensagem.append(dicionario[s])
            if len(dicionario) == tam_dicionario:
                s = c
                continue
            else:
                dicionario[seq] = len(dicionario)
            
            s = c
            
    return mensagem

def lzw_decompress(data):
    dicionario = {i: chr(i) for i in range(256)}
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
                dicionario[len(dicionario)] = s + saida_atual[0]
        
        s = saida_atual
    
    return msg_descomprimida

msg = ler_arquivo()
start = datetime.now()
msg_comprimida = lzw_compress(msg)
end = datetime.now()
print(f"Tempo de compressão = {end - start}")

with open('arquivo.lzw', 'wb') as f:
    f.write(msg_comprimida.tobytes())

start = datetime.now()
msg_descomprimida = lzw_decompress(msg_comprimida)
end = datetime.now()
print(f"Tempo de descompressão = {end - start}")
msg_descomprimida = ''.join(msg_descomprimida)

# with open('disco1.mp4', 'rb') as f:
#     byte = f.read()


# bytes_desc = bytes(msg_descomprimida.encode())

# print(len(bytes_desc))
# print(len(byte))

# for i in range(len(bytes_desc)):
#     if byte[i] != bytes_desc[i]:
#         print(byte[i])
#         print(bytes_desc[i])

with open('arquivo-novo.txt', 'w') as f:
    f.write(msg_descomprimida)