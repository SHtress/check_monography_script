__author__ = "Viktor \"Vikort\" Markovets"


import re
import sys


def parse_from_file(path: str):
    result = []
    with open(path, "r") as file:
        for line in file:
            res = re.findall(r'\\scncite\{[\w\-\d]+\}', line)
            for i in res:
                if "\scnitem{" + i + "}" not in result:
                    result.append("\scnitem{" + i + "}")
    with open("parse_result.txt", 'w') as file:
        for line in result:
            file.write("\t" + line + '\n')
    print("bibliography parsed", bool(result))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        parse_from_file(sys.argv[1])
