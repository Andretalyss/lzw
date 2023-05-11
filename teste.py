import bitarray
from datetime import datetime
import sys
import os

arg1 = sys.argv[1] # Recebe 'txt' ou 'mp4'
arg2 = sys.argv[2] # Recebe 'nomedoarquivo.txt' ou 'nomedoarquivo.mp4'


# LER ARQUIVO BYTE A BYTE E ADICIONA NUMA LIST O VALOR INTEIRO REFERENTE AO BYTE.
def ler_arquivo():
    with open(arg2, 'rb') as file:
        bytes_array = []
        byte = file.read(1)
        while byte:
            value = int.from_bytes(byte, byteorder='little')
            bytes_array.append(value)
            byte = file.read(1)
    
    return bytes_array

def lzw_compress(data):
    dicionario = {i.to_bytes(): i for i in range(256)} # Dicionário referencia o caracterer em byte e seu código ascii
    mensagem = bitarray.bitarray() # BitArray que armazena os bits comprimidos.

    flag = 0
    s = data[0].to_bytes()  # Recebe valor em inteiro e converte para bytes.
    for char in range(len(data)):

        # Verifica se o próximo caracterer chegou no final da lista de data, adiciona o ultima sequencia no array de bits
        if (char+1) >= len(data):
            if s in dicionario:
                mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))
                break
        else:
            c = data[char+1].to_bytes()
        
        # Cria uma lista de bytes e depois converte a lista para string, decodificando para iso-8859-1, pois o default é utf-8 e alguns códigos dariam erro.
        seq = [s, c]
        seq = ''.join([byte.decode('iso-8859-1') for byte in seq])

        # Verifica se a seq em byte existe no dicionario.
        if seq.encode() in dicionario:
            s = seq.encode()
        else:
            mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))   # Adiciona código ascii em n_bits no array de bits.

            # Verifica se o dicionário chegou no limite e torna estático.
            if len(dicionario) == tam_dicionario:
                flag = 1
                s = c
                continue
            else:
                dicionario[seq.encode()] = len(dicionario)  # Adiciona no dicionário com key = byte e código em inteiro.
                
            s = c
    if flag:
        print("Dicionário encheu")
    return mensagem
    

def lzw_decompress(data):
    dicionario = {i: i.to_bytes() for i in range(256)} # Dicionário referencia o codigo ascii com seu caracterer em byte
    s = ""
    msg_descomprimida = []  # Lista que irá armazenar o data descomprimido.
    index = 0

    while index < len(data):
        cod =  int(data[index:index+N_BITS].to01(), 2)  # Converter o byte do index para seu valor em inteiro.
        index += N_BITS # Percorre o array de bits de n_bits em n_bits.

        # Verifica se o código está no dicionario
        if cod in dicionario:
            saida_atual = dicionario[cod]   # A saida atual se torna o caractere em byte do código encontrado.
        elif cod >= len(dicionario):    # Verifico se código recebido tem um valor maior que o tamanho do dicionário (significa que não está inserido ainda)
            if s:
                saida_atual = s + s[0].to_bytes() # Adiciona a saida atual como o caractere anterior + caractere inicial dele em bytes.
            else:
                saida_atual = s 
        else:
            raise ValueError('Erro')

        msg_descomprimida.append(saida_atual) # Adiciona na lista de saída o valor da saida atual.
        if s:
            if len(dicionario) == tam_dicionario: # Se o dicionário chegou ao limite, torna estático.
                s = saida_atual
                continue
            else:
                dicionario[len(dicionario)] = s + saida_atual[0].to_bytes() # Adiciona no dicionário a key = código e seu caractere anterior + caractere inicial da saida atual em bytes.
        
        s = saida_atual
    
    return msg_descomprimida

def gera_arquivo_lzw(data):
    with open('arquivo-comprimido.lzw', 'wb') as f:  # Gera arquivo comprimido.
        f.write(data.tobytes())

def gera_arquivo_descomprimido(data):
    if arg1 == 'mp4':
        with open('disco-descomprimido.mp4', 'wb') as f: # Gera arquivo mp4 descomprimido e "tocável"
            for b in data:
                f.write(b)

    elif arg1 == 'txt':
        msg_nova = ''.join([b.decode('iso-8859-1') for b in data]) # Concatena todos os bytes presentes na lista descomprimida e decodifica para utf8, tornando string.
        with open('arquivo-descomprimido.txt', 'w') as f: # Gera arquivo txt descomprimido.
            f.write(msg_nova)

# Executa compressão e descompressão de 9bits até 16bits.
for i in range(9,17):
    N_BITS = i
    print(f"EXECUTANDO COM {N_BITS} bits - arquivo {arg1}\n")
    tam_dicionario = 2**N_BITS
    msg = ler_arquivo()
    start = datetime.now()
    msg_comprimida = lzw_compress(msg)
    end = datetime.now()
    print(f"Tempo de compressão = {end - start}")

    gera_arquivo_lzw(msg_comprimida)
    tamanho_arquivo = os.path.getsize("arquivo-comprimido.lzw")
    mb = tamanho_arquivo/(1024*1024)
    print(f"Arquivo comprimido gerado com tamanho = {mb:.2f}mb")

    start = datetime.now()
    msg_descomprimida = lzw_decompress(msg_comprimida)
    end = datetime.now()
    print(f"Tempo de descompressão = {end - start} \n")
    gera_arquivo_descomprimido(msg_descomprimida)

