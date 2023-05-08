import bitarray
import sys

arg1 = sys.argv[1]
arg2 = sys.argv[2]

N_BITS = 16
tam_dicionario = 2**N_BITS
dicionario = {}

def read_archive():
    if arg1 == 'txt':
        messagem = ""
        arq = open(arg2, "r")
        for linha in arq:
            for i in linha:
                messagem += i
        
        arq.close()

        return messagem
    elif arg1 == 'mp4':
        with open(arg2, "rb") as file:
            dados = file.read()
            
        return str(dados)

def lzw_compress(messagem):
    dicionario = {chr(i): i for i in range(256)} # Inicializa dicionário ASCII
    msg_comprimida = bitarray.bitarray()
    list_encoded = []
    s = messagem[0] 
    for caracter in range(len(messagem)):
        if (caracter+1) >= len(messagem):
            for i in dicionario:
                if s == i:
                    msg_comprimida.extend(bin(dicionario[i])[2:].zfill(N_BITS))
                    break
            
            # if len(dicionario) == tam_dicionario:
            #     break
            # else:
            #dicionario[f"{s}EOF"] = len(dicionario)

            ## FRACIONAR MENSAGEM COMPRIMIDA EM ARRAY
            #list_encoded.append(msg_comprimida)
            break
        else:
            c = messagem[caracter+1]
        
        sequencia = [s,c]
        sequencia = ''.join(sequencia)

        if sequencia not in dicionario:
            if len(dicionario) == tam_dicionario:
            #     if len(list_encoded) == 2:
            #         print(dicionario)
                dicionario = {}
                dicionario = {chr(i): i for i in range(256)}
                #dicionario[sequencia] = len(dicionario)

                for i in dicionario:
                    if s == i:
                        msg_comprimida.extend(bin(dicionario[i])[2:].zfill(N_BITS))
                        break
                s = c

                ## FRACIONAR MENSAGEM COMPRIMIDA EM ARRAY
                #list_encoded.append(msg_comprimida)
                #msg_comprimida = bitarray.bitarray()
                continue

            else:
                dicionario[sequencia] = len(dicionario)
        else:
            s = sequencia
            continue

        for i in dicionario:
            if s == i:
                msg_comprimida.extend(bin(dicionario[i])[2:].zfill(N_BITS))
                break
        
        s = c

    return msg_comprimida

def lzw_decompress(messagem):
    dicionario_2 = {i: chr(i) for i in range(256)}
    saida_anterior = ""
    msg_descomprimida = ""
    code_size = N_BITS
    index = 0

    while index < len(messagem):
        code = int(messagem[index:index+code_size].to01(), 2)
        index+=code_size
        print(f"Index = {index}")
        print(f"Tamanho messagem: {len(messagem)}")

        if code in dicionario_2:
            saida_atual = dicionario_2[code]
        elif code >= len(dicionario_2):
            if saida_anterior:
                saida_atual = saida_anterior + saida_anterior[0]
            else:
                saida_atual = saida_anterior
        else:
            raise ValueError("Erro na compressão")
        
        msg_descomprimida += saida_atual
        if saida_anterior:
            if len(dicionario_2) == tam_dicionario:
                dicionario_2 = {}
                dicionario_2 = {i: chr(i) for i in range(256)}
                #dicionario_2[len(dicionario_2)] = saida_anterior + saida_atual[0] 
            else:
                dicionario_2[len(dicionario_2)] = saida_anterior + saida_atual[0]   
        
        saida_anterior = saida_atual

    return msg_descomprimida
    
def gerar_arquivo_comprimido(msg_comprimida):
    with open('arquivo.lzw', 'w') as arquivo:
        arquivo.write(msg_comprimida)

messagem = read_archive()
compressed_data = lzw_compress(messagem)
print(len(compressed_data))

if arg1 == 'txt':
    decompress_data = lzw_decompress(compressed_data)
    with open('compress', 'a') as arquivo:
        for k in decompress_data:
            arquivo.write(k)
else:
    decompress_data = []
    for i in range(len(compressed_data)):
        decompress_data.append(lzw_decompress(compressed_data[i]))

