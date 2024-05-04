# Separar una cadena por espacios en blanco y devolver una lista
def split(line):
    result = []
    word = ""
    for char in line:
        if char == " ":
            result.append(word)
            word = ""
        else:
            word += char
    result.append(word)
    return result

# Buscar un caracter en una cadena y retornar el indice
def find(string, char):
    for index, char_ in enumerate(string):
        if char_ == char:
            return index
    return -1

# Buscar un string en una cadena y retornar el indice
def find2(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return index
    return -1

# Buscar un string en una cadena y retornar True o False
def find3(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return True
    return False

# Borrar espacios en blanco
def delete_white_spaces(string):
    result = ""
    for char in string:
        if char != " ":
            result += char
    return result

# Borrar saltos de linea
def delete_jump_line(string):
    result = ""
    for char in string:
        if char != "\n":
            result += char
    return result

# Borrar espacio en blanco de una cadena excepto cuando este rodeado de comillas
def delete_white_spaces2(string):
    result = ""
    for index, char in enumerate(string):
        if char == " ":
            if index == 0 or index == len(string) - 1:
                continue
            elif string[index - 1] != "'" and string[index + 1] != "'" and string[index - 1] != '"' and string[index + 1] != '"':
                continue
        result += char
    return result


def yaparReader(archivo):
    with open(archivo, "r") as file:
        content = file.read()

    # Eliminar comentarios
    while find3(content, "/*"):
        index = find2(content, "/*")
        index2 = find2(content, "*/")
        content = content[:index] + content[index2 + 2:]

    token_list = []

    # Leer tokens
    while '%token' in content:
        index = find2(content, '%token')
        content = content[index + 7:]
        index2 = find(content, '\n')
        token = content[:index2]
        token_list.append(token)
        content = content[index2 + 1:]

    # Separar tokens si hay mas de un token en una linea
    for index, token in enumerate(token_list):
        if " " in token:
            x = split(token)
            token_list[index] = x[0]
            for i in range(1, len(x)):
                token_list.append(x[i])

    # Obtener producciones
    productions = {}
    while content != "":
        index = find2(content, ":\n")
        index2 = find(content, ";")
        head = content[:index]
        head = delete_jump_line(head)
        body = content[index + 2:index2]
        body = delete_jump_line(body)
        x = split(body)
        # Eliminar cadenas vacías
        while "" in x:
            x.remove("")
        res = []
        word = ""
        for element in x:
            if element == "|":
                word = word[:len(word) - 1]
                res.append(word)
                word = ""
            else:
                word += element + " "
        # Eliminar último espacio en blanco
        word = word[:len(word) - 1]
        res.append(word)
        productions[head] = res

        content = content[index2 + 1:]

    # Obtener no terminales obteniendo llaves de producciones
    no_terminals = list(productions.keys())
    return token_list, no_terminals, productions
