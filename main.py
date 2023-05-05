import bitarray
N_BITS = 9
tam_dicionario = 2**N_BITS
dicionario = {}

def read_archive():
    messagem = []
    arq = open("arqui2.txt", "r")
    for linha in arq:
        for i in linha:
            messagem.append(i)
    
    arq.close()

    return messagem


def lzw_compress(messagem):
    dicionario = {chr(i): i for i in range(256)} # Inicializa dicionário ASCII
    msg_comprimida = bitarray.bitarray()

    print(dicionario)
    s = messagem[0] 
    for caracter in range(len(messagem)):
        if (caracter+1) >= len(messagem):
            for i in dicionario:
                if s == i:
                    msg_comprimida.extend(bin(dicionario[i])[2:].zfill(N_BITS))
                    break
            
            if len(dicionario) == tam_dicionario:
                print("Dicionário está cheio!")
            else:
                dicionario[f"{s}EOF"] = len(dicionario)

            break
        else:
            c = messagem[caracter+1]
        
        sequencia = [s,c]
        sequencia = ''.join(sequencia)

        if sequencia not in dicionario:
            if len(dicionario) == tam_dicionario:
                print("Dicionário cheio!")
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
        print(messagem[index:index+code_size].to01(), 2)
        index+=code_size
        # print(f"Index = {index}")
        # print(f"Tamanho messagem: {len(messagem)}")

        if code in dicionario_2:
            # print(f"entoru no if: {code} - {len(dicionario_2)}")
            saida_atual = dicionario_2[code]
        elif code >= len(dicionario):
            saida_atual = saida_anterior + saida_anterior[0]
            # print(f"entrou no elif : {code} - {len(dicionario_2)}")
        else:
            # print(f"erro em {code}")
            raise ValueError("Erro na compressão")
        
        msg_descomprimida += saida_atual
        if saida_anterior:
            if len(dicionario_2) == tam_dicionario:
                print("Dicionário cheio")
            else:
                dicionario_2[len(dicionario_2)] = saida_anterior + saida_atual[0]    
            # if len(dicionario_2) == 2**code_size:
            #     code_size += 1
        
        saida_anterior = saida_atual

    return msg_descomprimida
    

messagem = read_archive()
compressed_data = lzw_compress(messagem)
descompressed_data = lzw_decompress(compressed_data)
print(messagem)
print(compressed_data)
print(descompressed_data)