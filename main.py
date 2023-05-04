alfabeto_ascii = {}

def ascii_initialize(alfabeto_ascii):
    codigo = 0
    for x in range(32, 126):
        # alfabeto_ascii[f"{format(ord(chr(x)), 'b')}"] = x
        alfabeto_ascii[f"{chr(x)}"] = x
        codigo = x
    
    return codigo

def read_archive():
    messagem = []
    arq = open("arquivo.txt", "r")
    for linha in arq:
        for i in linha:
            # messagem.append(format(ord(i), 'b'))
            messagem.append(i)
    arq.close()

    return messagem

def lzw_enconder(messagem, alfabeto_ascii, codigo):
    msg_comprimida = []
    s = messagem[0]
    for caractere in range(len(messagem)):
        if (caractere+1) >= len(messagem):
            for i in alfabeto_ascii:
                if s == i:
                    msg_comprimida.append(alfabeto_ascii[i])
                    break
            
            alfabeto_ascii[f"{s}EOF"] = codigo
            codigo +=1
            break
        else:
            c = messagem[caractere+1]
        
        sequencia = [s,c]
        sequencia = ''.join(sequencia)

        if sequencia not in alfabeto_ascii:
            alfabeto_ascii[f"{sequencia}"] = codigo
            codigo += 1
        else:
            s = sequencia
            continue
            
        for i in alfabeto_ascii:
            if s == i:
                msg_comprimida.append(alfabeto_ascii[i])
                break

        s = c

    print(f"\n\n{alfabeto_ascii}\n\n")
    return msg_comprimida

def write_archive(msg_comprimida):
    with open('arq-compress', 'w') as arquivo:
        for i in msg_comprimida:
            arquivo.write(str(bin(i)))

codigo = ascii_initialize(alfabeto_ascii)
print(alfabeto_ascii)
messagem = read_archive()
print(messagem)

msg_comprimida = lzw_enconder(messagem, alfabeto_ascii, codigo)
print(msg_comprimida)

write_archive(msg_comprimida)

# with open('arq-2', 'w') as arquivo:
#     for i in messagem:
#         arquivo.write(format(ord(i), 'b'))
        





