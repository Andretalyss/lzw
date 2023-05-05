import bitarray

def compress(data):
    dictionary = {chr(i): i for i in range(256)}
    result = bitarray.bitarray()
    sequence = ""
    
    for char in data:
        temp = sequence + char
        if temp in dictionary:
            sequence = temp
        else:
            result.extend(bin(dictionary[sequence])[2:].zfill(9))
            dictionary[temp] = len(dictionary)
            sequence = char
    
    if sequence:
        result.extend(bin(dictionary[sequence])[2:].zfill(9))
    
    print(dictionary)
    return result


def decompress(data):
    dictionary = {i: chr(i) for i in range(256)}
    result = ""
    sequence = ""
    code_size = 9
    index = 0
    
    while index < len(data):
        code = int(data[index:index+code_size].to01(), 2)
        index += code_size
        
        if code in dictionary:
            entry = dictionary[code]
        elif code == len(dictionary):
            entry = sequence + sequence[0]
        else:
            raise ValueError("Bad compression code")
        
        result += entry
        if sequence:
            dictionary[len(dictionary)] = sequence + entry[0]
            if len(dictionary) == 2**code_size:
                code_size += 1
        sequence = entry
    
    return result

original_data = "ABRACADABRA"
compressed_data = compress(original_data)
decompressed_data = decompress(compressed_data)

print("Messagem:", original_data)
print("Msg_comprimida:", compressed_data)
print("Msg_descomprimida:", decompressed_data)