#!/usr/bin/python3
# Gabriel Fernandes <gabrielfernndss@gmail.com>

import re
import os
import sys
import zipfile
import requests

from . import retrievedata


USAGE = '''Specify the folder to looking for pom.xml and the 'roteiro number' 
            like this: python3 autoit.py /path/to/pom/ 5'''

MATRICULA_PATTERN = re.compile('INSIRA SEU NUMERO DE MATRICULA')
ROTEIRO_PATTERN = re.compile('R0.-0.')


def valida_turma(turma):
    if not isinstance(turma, str):
        raise TypeError('turma precisa ser um caractere("str")')
    turmas = ('1', '2', '3')
    if turma not in turmas:
        raise ValueError('turma precisa ser uma das: (1,2,3)')


def valida_matricula(matricula):
    if not isinstance(matricula, str):
        raise TypeError('matricula precisa ser uma "str"')
    regex = re.compile('\d{1,9}')
    if not regex.fullmatch(matricula):
        raise ValueError('matricula precisa ser do tipo xxxxxxxxx, onde x é um digito(1-9)')


def valida_path(path):
    if not isinstance(path, str):
        raise TypeError('path precisa ser passado como uma "str"')
    if not os.path.isdir(path):
        raise TypeError('insira um caminho("path") de diretorio valido')


def write_pom(path, matricula, roteiro):
    valida_path(path)
    valida_matricula(matricula)
    retrievedata.valida_roteiro(roteiro)

    data = None
    with open(path + '/pom.xml', 'r') as pom:
        data = pom.read()
        data = MATRICULA_PATTERN.sub(matricula, data)
        data = ROTEIRO_PATTERN.sub(roteiro, data)

    if data != None:
        with open(path + '/pom.xml', 'w') as pom:
            pom.write(data)


def extract_zip(zip, folder):
    with zipfile.ZipFile(zip) as zp:
        zp.extractall(folder)


def main():
    args = sys.argv
    try:
        write_pom(args[1], args[2], args[3])
    except IndexError:
        print('''Uso: passar caminho ate a pasta em que se encontra o pom.xml, 
            matricula e roteiro na qual deseja-se preencher automaticamento no pom
            Exemplo: python3 autoit.py /home/fernandes/leda-roteiros 111110234 R03-03''')
        sys.exit(1)


if __name__ == '__main__':
    main()