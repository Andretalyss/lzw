import bitarray
from datetime import datetime
import random

# LER ARQUIVO BYTE A BYTE E ADICIONA NUMA LIST O VALOR INTEIRO REFERENTE AO BYTE.
def ler_arquivo(arq_name):
    with open(arq_name, 'rb') as file:
        bytes_array = []
        byte = file.read(1)
        while byte:
            value = int.from_bytes(byte, byteorder='little')
            bytes_array.append(value)
            byte = file.read(1)
    
    return bytes_array

def lzw_compress(data, N_BITS):
    dicionario = {i.to_bytes(): i for i in range(256)} # Dicionário referencia o caracterer em byte e seu código ascii
    mensagem = bitarray.bitarray() # BitArray que armazena os bits comprimidos.

    flag = 0
    for dados in data:
        s = dados[0].to_bytes()  # Recebe valor em inteiro e converte para bytes.
        for char in range(len(dados)):

            # Verifica se o próximo caracterer chegou no final da lista de data, adiciona o ultima sequencia no array de bits
            if (char+1) >= len(dados):
                if s in dicionario:
                    mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))
                    break
            else:
                c = dados[char+1].to_bytes()
            
            # Cria uma lista de bytes e depois converte a lista para string, decodificando para iso-8859-1, pois o default é utf-8 e alguns códigos dariam erro.
            seq = [s, c]
            seq = ''.join([byte.decode('iso-8859-1') for byte in seq])

            # Verifica se a seq em byte existe no dicionario.
            if seq.encode() in dicionario:
                s = seq.encode()
            else:
                mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))   # Adiciona código ascii em n_bits no array de bits.

                # Verifica se o dicionário chegou no limite e torna estático.
                if len(dicionario) == 2**N_BITS:
                    flag = 1
                    s = c
                    continue
                else:
                    dicionario[seq.encode()] = len(dicionario)  # Adiciona no dicionário com key = byte e código em inteiro.
                    
                s = c
    
    return dicionario
    
def lzw_compress_test(dados, dicionario, N_BITS):
    mensagem = bitarray.bitarray() # BitArray que armazena os bits comprimidos.

    flag = 0
    
    s = dados[0].to_bytes()  # Recebe valor em inteiro e converte para bytes.
    for char in range(len(dados)):

        # Verifica se o próximo caracterer chegou no final da lista de data, adiciona o ultima sequencia no array de bits
        if (char+1) >= len(dados):
            if s in dicionario:
                mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))
                break
        else:
            c = dados[char+1].to_bytes()
        
        # Cria uma lista de bytes e depois converte a lista para string, decodificando para iso-8859-1, pois o default é utf-8 e alguns códigos dariam erro.
        seq = [s, c]
        seq = ''.join([byte.decode('iso-8859-1') for byte in seq])

        # Verifica se a seq em byte existe no dicionario.
        if seq.encode() in dicionario:
            s = seq.encode()
        else:
            mensagem.extend(bin(dicionario[s])[2:].zfill(N_BITS))   # Adiciona código ascii em n_bits no array de bits.

            # Verifica se o dicionário chegou no limite e torna estático.
            if len(dicionario) == 2**N_BITS:
                flag = 1
                s = c
                continue
            else:
                dicionario[seq.encode()] = len(dicionario)  # Adiciona no dicionário com key = byte e código em inteiro.
                
            s = c

    return len(mensagem)

K = [9,10,11,12,13,14,15,16]
NUM_PESSOAS = 40
NUM_FACES = 10
acertos = []

for k in K:
    start = datetime.now()
    img_testes = []
    dicionarios = []
    qtd_acertos = 0

    for i in range(0, NUM_PESSOAS):
        imagem = []

        for j in range(0,NUM_FACES):
            arq_name = "orl_faces/s" + str(i+1) + "/" + str(j+1) + ".pgm"
            content = ler_arquivo(arq_name)
            imagem.append(content)
        
        number = random.randint(0,9)
        img_testes.append(imagem[number])
        del imagem[number]
        
        dicionarios.append(lzw_compress(imagem, k))
    
    for i in range(len(img_testes)):
        m_value = 10000000000

        for j in range(len(dicionarios)):
            tam = lzw_compress_test(img_testes[i], dicionarios[j], k)

            if(tam < m_value):
                m_value = tam
                indice = j
        
        if (i == indice):
            qtd_acertos+=1
    
    end = datetime.now()
    print("k = "+str(k)+", acertos: " + str(qtd_acertos))
    print(f"Tempo de execução = {end - start}\n")
    acertos.append(qtd_acertos)
