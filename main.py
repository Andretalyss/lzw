dicionario = {}
dicionario_inicial = {}
message = ""

def read_message():
    arq = open("arquivo.txt", "r")
    for linha in arq:
        messagem = linha
    arq.close()

    return messagem

def dicionario_arranque(message):
    codigo = 1
    for caract in message:
        if caract not in dicionario:
            dicionario[f"{caract}"] = codigo
            dicionario_inicial[f"{caract}"] = codigo
            codigo +=1 

    return codigo

def codificacao_lzw(message, codigo):
    saida = []
    print(f"Messagem real: \n\t{message}")
    aux_cod = codigo
    s = message[0]
    for caract in range(len(message)):                    
        prox = caract+1
        if prox >= len(message):
            for i in dicionario:
                if s == i:
                    saida.append(str(dicionario[i]))
                    break
            break
        else:    
            c = message[caract+1]  

        sequencia = [s, c]
        sequencia = ''.join(sequencia)

        if sequencia not in dicionario:
            dicionario[f"{sequencia}"] = aux_cod
            aux_cod +=1
        else:
            s = sequencia
            continue

        for i in dicionario:
            if s == i:
                saida.append(str(dicionario[i]))
                break

        s = c

    print(f"\n{saida}")
    print(f"\n{dicionario}")
    return saida
    
            
def decodifica_lzw(dicionario_inicial, codigo_comprimido, codigo):
    saida_anterior = ""
    saida_atual = ""
    msg_decode = []
    flag = 0
    for i in range(len(codigo_comprimido)):
        c = codigo_comprimido[i]
        s = saida_anterior
        for k in dicionario_inicial:
            if int(dicionario_inicial[k]) == int(c):
                saida_atual = k
                msg_decode.append(saida_atual)
                flag = 1
                break
        
        if not flag:
            add = [s, s[0]]
            add = ''.join(add)
            dicionario_inicial[f"{add}"] = codigo
            saida_atual = add
            msg_decode.append(saida_atual)
            codigo+=1
            continue
        
        flag = 0
        saida_anterior = saida_atual
        if s != "":
            seq = [s, saida_atual]
            seq = ''.join(seq)
            dicionario_inicial[f"{seq}"] = codigo
            codigo +=1 

    msg_decode = ''.join(msg_decode)
    print(f"\nMessagem descodificada: \n\t{msg_decode}")
    print(f"\n{dicionario_inicial}")
   
message = read_message()
cod = dicionario_arranque(message)
cod_comprimido = codificacao_lzw(message, cod)
decodifica_lzw(dicionario_inicial, cod_comprimido, cod)