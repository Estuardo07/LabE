import graphviz

EPSILON = 'ε'
CONCAT = "."
UNION = "|"
STAR = "*"
QUESTION = "?"
PLUS = "+"
LEFT_PARENTHESIS = "("
RIGHT_PARENTHESIS = ")"

OPERADORES = [EPSILON, CONCAT, UNION, STAR, QUESTION,
              PLUS, LEFT_PARENTHESIS, RIGHT_PARENTHESIS]


# Funcion para separar una linea en palabras
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

# Funcion para buscar un caracter en una cadena y retornar el indice
def find(string, char):
    for index, char_ in enumerate(string):
        if char_ == char:
            return index
    return -1

# Funcion para buscar un string en una cadena y retornar el indice
def find2(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return index
    return -1

# Funcion para buscar un string en una cadena y retornar True o False
def find3(string, string_):
    for index, char_ in enumerate(string):
        if string[index:index + len(string_)] == string_:
            return True
    return False

# Borrar espacios en blanco de una cadena
def delete_white_spaces(string):
    result = ""
    for char in string:
        if char != " ":
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

# Funcion para saber si un caracter es una letra
def is_letter(char):
    ascii_val = ord(char)  # Obtener el valor ASCII del caracter
    return (ascii_val >= 65 and ascii_val <= 90) or (ascii_val >= 97 and ascii_val <= 122)

# Funcion para saber si un caracter es un numero
def is_digit(char):
    ascii_val = ord(char)  # Obtener el valor ASCII del caracter
    return ascii_val >= 48 and ascii_val <= 57


# Funcion para buscar si existe una variable dentro de una cadena dado un indice y retornar el indice de la variable
def find4(string, index, string_to_find):
    for i in range(index, len(string)):
        if string[i:i + len(string_to_find)] == string_to_find:
            return i
    return -1


# Funcion para reemplazar una subcadena por otra en un string
def my_replace(original_str, old_substring, new_substring):
    result_str = ""  # Inicializar el string de resultado
    # Obtener la longitud de la subcadena a reemplazar
    sub_len = len(old_substring)
    i = 0  # Inicializar el índice del string original

    while i < len(original_str):
        # Buscar la siguiente ocurrencia de la subcadena a reemplazar
        j = find4(original_str, i, old_substring)

        # Si no se encontró ninguna ocurrencia más, agregar el resto del string original al resultado y salir del loop
        if j == -1:
            result_str += original_str[i:]
            break

        # Agregar el segmento del string original que está antes de la ocurrencia de la subcadena a reemplazar al resultado
        result_str += original_str[i:j]

        # Agregar la subcadena de reemplazo al resultado
        result_str += new_substring

        # Actualizar el índice para continuar la búsqueda después de la ocurrencia actual de la subcadena a reemplazar
        i = j + sub_len

    return result_str


def expand_range2(range_str):
    expanded_str = ""
    while find(range_str, "-") != -1:
        index = find(range_str, "-")
        for j in range(ord(range_str[index-2]), ord(range_str[index+2])+1):
            # Si j es final de linea, solo se agrega el caracter, sino agregar el caracter y |
            if j == ord(range_str[index+2]):
                expanded_str += chr(j)
            else:
                expanded_str += chr(j) + "|"
        if range_str[index+4] == "]":
            range_str = range_str[:index-3] + \
                expanded_str + range_str[index+4:]
        else:
            range_str = range_str[:index-3] + \
                expanded_str + '|' + range_str[index+4:]
        expanded_str = ""
    return range_str


def validate_range(range_str):
    for i in range(len(range_str)):
        if range_str[i] == "-":
            if is_letter(range_str[i-2]) and is_letter(range_str[i+2]):
                continue
            elif is_digit(range_str[i-2]) and is_digit(range_str[i+2]):
                continue
            else:
                return False
    return True

# Funcion para reemplazar una subcadena por otra en un string. Se utiliza para buscar dentro del valor de una variable si existe una variable y reemplazarla por su valor
def find_replace(string, string_to_replace, string_to_replace_with):
    # Dividir el string original en un array de strings
    words = []
    word = ""
    for char in string:
        if is_letter(char) or is_digit(char):
            word += char
        else:
            if word != "":
                words.append(word)
                word = ""
            words.append(char)
    if word != "":
        words.append(word)

    resultado = ""
    for word in words:
        if word == string_to_replace:
            resultado += string_to_replace_with
        else:
            resultado += word
    return resultado


OPERADORES2 = [EPSILON, CONCAT, UNION, STAR, QUESTION,
               PLUS, RIGHT_PARENTHESIS]

# Funcion para encontrar donde es necesario agregar el operador de concatenacion siguiendo ciertas reglas
def validate_concatenation(value):
    array = []
    for char in value:
        array.append(char)

    res = ""
    while array:
        char = array.pop(0)
        if char == ')':
            if array:
                if array[0] not in OPERADORES2:
                    res += char + CONCAT
                elif array[0] == '#':
                    res += char + CONCAT
                else:
                    res += char
            else:
                res += char
        elif char == "'":
            if array:
                if len(array) >= 3:
                    if array[1] == "'":
                        if array[2] not in OPERADORES2:
                            res += char + array.pop(0) + array.pop(0) + CONCAT
                        else:
                            res += char + array.pop(0) + array.pop(0)
                elif len(array) == 2:
                    if array[1] == "'":
                        res += char + array.pop(0) + array.pop(0)
        elif char == '"':
            if array:
                items = []
                items.append(char)
                for i in range(len(array)):
                    if array[i] == '"':
                        items.append(array[i])
                        break
                    else:
                        items.append(array[i])
                for i in range(len(items)-1):
                    array.pop(0)
                while items:
                    item = items.pop(0)
                    if item == '"':
                        res += item
                    elif item != '"' and items[0] != '"':
                        res += item + CONCAT
                    else:
                        res += item

        elif char == '*' or char == '?' or char == '+':
            if array:
                if array[0] not in OPERADORES2:
                    res += char + CONCAT
                else:
                    res += char
            else:
                res += char
        else:
            res += char
    return res


# Clase Simbolo para representar cada simbolo de la cadena y saber si es un operador o no
class Simbolo:
    def __init__(self, simbolo, is_operator=False):
        self.val = simbolo
        self.id = ord(simbolo)
        self.is_operator = is_operator


# Funcion para convertir la cadena a un arreglo de simbolos
def convert_to_Simbolo(string):
    array = []
    for char in string:
        array.append(char)

    res = []
    while array:
        char = array.pop(0)
        if char == "'":
            res.append(Simbolo(array.pop(0)))
            array.pop(0)
        elif char in OPERADORES:
            res.append(Simbolo(char, True))
        else:
            res.append(Simbolo(char))
    return res

# Funcion para convertir la cadena a un arreglo de simbolos tomando en cuenta los simbolos de dos caracteres
def convert_to_Simbolo2(string):
    array = []
    for char in string:
        array.append(char)

    res = []
    while array:
        char = array.pop(0)
        if char == "'":
            res.append(Simbolo(array.pop(0)))
            array.pop(0)
        elif char == '"':
            items = []
            for i in range(len(array)):
                if array[i] == '"':
                    items.append(array[i])
                    break
                else:
                    items.append(array[i])
            for i in range(len(items)):
                array.pop(0)
            while items:
                item = items.pop(0)
                if item == '.':
                    res.append(Simbolo(item, True))
                elif item != '"':
                    res.append(Simbolo(item))

        elif char in OPERADORES:
            res.append(Simbolo(char, True))
        else:
            res.append(Simbolo(char))
    return res


# Funcion para ordenar el arreglo de objetos Simbolo a notacion postfix
def shunting_yard(infix):
    # Precedencia de los operadores
    precedence = {'|': 1, '.': 2, '?': 3, '*': 3, '+': 3}
    # Pila de operadores
    stack = []
    # Cola de salida
    postfix = []
    for c in infix:
        # Si se encuentra un ( se agrega a la pila
        if c.val == '(' and c.is_operator == True:
            stack.append(c)
        # Si se encuentra un ) se sacan los operadores de la pila hasta encontrar un (
        elif c.val == ')' and c.is_operator == True:
            while stack[-1].val != '(' and stack[-1].is_operator == True:
                postfix.append(stack.pop())
            stack.pop()
        # Si se encuentra un operador se sacan los operadores de la pila hasta encontrar un operador de menor precedencia
        elif c.val in precedence and c.is_operator == True:
            while stack and stack[-1].val != '(' and stack[-1].is_operator == True and precedence[c.val] <= precedence[stack[-1].val]:
                postfix.append(stack.pop())
            stack.append(c)
        # Si se encuentra un simbolo se agrega a la cola de salida
        else:
            postfix.append(c)
    # Se sacan los operadores restantes de la pila y se agregan a la cola de salida
    while stack:
        postfix.append(stack.pop())

    return postfix


# clase nodo para crear el arbol de expresiones regulares
class Node:
    def __init__(self, data):
        self.id = id(self)
        self.data = data
        self.left = None
        self.right = None

# La función build_tree crea el árbol de expresiones regulares a partir de una expresión regular en notación postfix


def build_tree(postfix):
    # Se crea una pila vacía
    stack = []
    # Se recorre la expresión regular
    for c in postfix:
        # Si se encuentra un simbolo alfanumerico se crea un nodo con el simbolo y se agrega a la pila
        if not c.is_operator:
            stack.append(Node(c))
        # Si se encuentra un operador unario se crea un nodo con el operador y se saca un nodo de la pila y se agrega como hijo del nodo creado
        elif c.val == '*' or c.val == '?' or c.val == '+':
            node = Node(c)
            node.left = stack.pop()
            stack.append(node)
        # Si se encuentra un operador se crea un nodo con el operador y se sacan los dos nodos de la pila y se agregan como hijos del nodo creado
        else:
            node = Node(c)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack.pop()


# La función draw_tree crea un arbol a partir de un nodo raiz de una expresión regular en notación postfija

def draw_tree(root):
    # Se crea un grafo dirigido
    dot = graphviz.Digraph()
    # Se recorre el árbol de expresiones regulares

    def traverse(node):
        # Si el nodo no es nulo se crea un nodo con el id del nodo y el dato del nodo y se agregan las aristas correspondientes
        if node:
            dot.node(str(id(node)), node.data.val)
            # Si el nodo tiene un hijo izquierdo se crea una arista entre el nodo y el hijo izquierdo
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)))
            # Si el nodo tiene un hijo derecho se crea una arista entre el nodo y el hijo derecho
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)))
            # Se recorre el hijo izquierdo y el hijo derecho utilizando recursividad
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    return dot

# Funcion para crear el arbol, armarlo con graphviz y dibujarlo/guardarlo en la carpeta arboles
def show_tree(postfix, nombre):
    tree = build_tree(postfix)
    dot = draw_tree(tree)
    dot.format = 'png'
    dot.render('arboles/' + nombre, view=False)


TOKENS = {}


def Yalex_reader(archivo):
    # Abrir el archivo y guardar el contenido en una variable
    with open(archivo, "r") as file:
        content = file.read()

    # Eliminar comentarios de una cadena

    while '(*' in content:
        content = content[:find2(content, '(*')] + \
            content[find2(content, "*)") + 2:]

    # Eliminar saltos de linea de una cadena
    while '\n' in content:
        content = content[:find(content, '\n')] + \
            " " + content[find(content, '\n') + 1:]

    variables = {}
    tokens = {}

    # Guardar cada expresion regular dentro de la seccion de definicion regular
    while 'let' in content:
        index = find2(content, 'let ')
        content = content[index + 3:]
        name = content[:find(content, '=')]
        name = delete_white_spaces(name)
        if find2(content, 'let ') == -1:
            value = content[find2(content, '=') +
                            1: find2(content, 'rule tokens')]
            value = delete_white_spaces2(value)
            variables[name] = value
            content = content[find2(content, 'rule tokens'):]
        else:
            value = content[find2(content, '=') + 1:find2(content, 'let ')]
            value = delete_white_spaces2(value)
            variables[name] = value
            content = content[find2(content, 'let '):]

    rule_tokens = []
    while content != '':
        if find3(content, 'rule tokens'):
            index = find2(content, 'rule tokens')
            content = content[index + 11:]
            rule = content[find(content, '=') + 1:find(content, '|')]
            rule_tokens.append(rule)
            content = content[find(content, '|') + 1:]
        elif find3(content, '|'):
            rule = content[:find(content, '|')]
            rule_tokens.append(rule)
            content = content[find(content, '|') + 1:]
        else:
            rule = content
            rule_tokens.append(rule)
            content = ''

    tuples = []
    for rule in rule_tokens:
        if '{' in rule:
            tuples.append(
                (rule[:find(rule, '{')], rule[find(rule, '{') + 1:find(rule, '}')]))
        else:
            tuples.append((rule, ''))

    # Guardar en una lista los tokens de la tupla sin el {return}
    rule_tokens = []
    for rule in tuples:
        rule_tokens.append(delete_white_spaces(rule[0]))

    i = 0
    for rule in tuples:
        TOKENS[i] = rule[1]
        i += 1

    newVariables = {}
    keys_array = list(variables.keys())

    for key, value in variables.items():
        if validate_range(value):
            value = expand_range2(value)
            variables[key] = value

    # Reemplazar parte del valor de un item en el diccionario por el valor otro item si existe como llave
    for key, value in variables.items():
        for key2 in keys_array:
            value = find_replace(value, key2, variables[key2])
        variables[key] = value
        newVariables[key] = value

    # Reemplazar los rangos de los valores por la lista que representa ese rango
    for key, value in newVariables.items():
        if find3(value, "' ''\\t''\\n'"):
            value = value.replace("' ''\\t''\\n'", ' ' +
                                  '|' + '\t' + '|' + '\n')
        if find3(value, '"\\s\\t\\n"'):
            value = value.replace('"\\s\\t\\n"', ' ' + '|' + '\t' + '|' + '\n')
        if find3(value, "'+''-'"):
            value = value.replace("'+''-'", "'+'" + '|' + "'-'")
        newVariables[key] = value

    # Reemplazar los corchetes por parentesis
    for key, value in newVariables.items():
        if find3(value, '['):
            value = my_replace(value, '[', '(')
        if find3(value, ']'):
            value = my_replace(value, ']', ')')
        newVariables[key] = value

    # Para cada variable aplicarle la funcion de concatenacion
    for key, value in newVariables.items():
        newVariables[key] = validate_concatenation(value)

    # Para cada token en la lista, validar si existe una variable que tenga el mismo nombre y reemplazarla por su valor
    new_rule_tokens = []
    for rule in rule_tokens:
        for key, value in newVariables.items():
            if rule == key:
                rule = value
        new_rule_tokens.append(rule)

    for rule in new_rule_tokens:
        if rule[0] != "'" and rule[0] != '(' and rule[0] != '"':
            print(key, 'Error: ' + rule +
                  ' no es un token valido\nTermiando programa')
            exit()

    # Pasar todos los tokens a una sola cadena
    rule_token_regex = ""
    for rule in new_rule_tokens:
        # Revisar si es el ultimo elemento
        if rule == new_rule_tokens[-1]:
            rule_token_regex += '(' + '(' + rule + ')' + '#' + ')'
        else:
            rule_token_regex += '(' + '(' + rule + ')' + '#' + ')' + '|'

    rule_token_regex = validate_concatenation(rule_token_regex)

    definicion_regular = {}

    # Convertir la cadena a un arreglo de simbolos
    rule_token_regex = convert_to_Simbolo2(rule_token_regex)

    # Convertir cada variable a un arreglo de simbolos
    for key, value in newVariables.items():
        definicion_regular[key] = convert_to_Simbolo(value)

    # Aplicar la funcion shunting_yard a cada variable
    definicion_regular_postfix = {}
    for key, value in definicion_regular.items():
        definicion_regular_postfix[key] = shunting_yard(value)

    # Aplicar la funcion shunting_yard a los tokens
    rule_token_regex_postfix = shunting_yard(rule_token_regex)

    return rule_token_regex_postfix, TOKENS
