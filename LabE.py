from yaparReader import yaparReader
from SLR import build_slr
from yalex.scanner import get_tokens


def main():
    file = 'yapars/slr-4.yalp'
    terminals, no_terminals, gramatica = yaparReader(file)
    tokens = get_tokens()
    for val in terminals:
        if val in tokens.values():
            pass
        else:
            print("Tokens no definidos", val)
            exit(1)
    print('Todos los tokens estan definidos')
    slr = build_slr(gramatica, terminals, no_terminals)
    slr.draw_afd()


if __name__ == '__main__':
    main()
