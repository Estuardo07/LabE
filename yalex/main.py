from yalexReader import yalexReader
from directAFD import regex_to_afd
from jinja2 import Template
import pickle


def main():
    file = 'YALex2.txt'
    rule_token, token_dic = yalexReader(file)
    with open('template.j2', 'r') as f:
        template = f.read()

    template = Template(template)
    rendered = template.render(tokens=token_dic)
    with open('scanner.py', 'w') as f:
        f.write(rendered)
    afd = regex_to_afd(rule_token, token_dic)

    print("afd generado")
    with open('afd.pickle', 'wb') as f:
        pickle.dump(afd, f)


if __name__ == '__main__':
    main()
