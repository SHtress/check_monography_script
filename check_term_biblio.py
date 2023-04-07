#!/usr/bin/env python3
"""Module to check if chapter terms in glossary and bibliographic links are in bibliography.tex
"""

import argparse
import os
import re

from termcolor import colored

KEY_CONCEPT = "ключевое понятие"
KEY_RELATION = "ключевое отношение"
KEY_SIGN = "ключевой знак"
KEY_KNOWLEDGE = "ключевое знание"
KEY_PARAMETR = "ключевой параметр"

BIBLIO_LINK = "библиографическая ссылка"

AUTHORS = "автор"

FILE_PATH = "file_path"
GLOSSARY_PATH = "glossary_path"
BIBLIO_PATH = "biblio_path"

KEY_ELEMENTS = [KEY_CONCEPT, KEY_RELATION,
                KEY_SIGN, KEY_PARAMETR]

BEGIN_LIST = "\\begin{scnrelfromlist}"
END_LIST = "\\end{scnrelfromlist}"
CHAPTER = "\\chapter"


def check_terms(file_path: str, glossary_path: str) -> list:
    """Check if key term in glossary.

    Args:
        file_path (str): path to file to check
        glossary_path (str): path to glossary file

    Returns:
        list: need to fix term list
    """
    in_list = False
    key_lists = []
    terms_to_fix = []

    key_list_begin_line = 0
    key_list_end_line = 0

    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

        for line_number, line in enumerate(lines):
            for key_element in KEY_ELEMENTS:
                if BEGIN_LIST + "{" + key_element + "}" in line:
                    key_list_begin_line = line_number
                    in_list = True
            if (in_list is True and END_LIST in line):
                key_list_end_line = line_number + 1
                in_list = False
                key_lists.append((key_list_begin_line, key_list_end_line))

    key_elements_to_check = []

    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for key_list in key_lists:
            for key_line_number in range(key_list[0] + 1, key_list[1] - 1):
                result = re.search(
                    r"\\scnitem{([А-яA-z0-9,.!?: *-]+)}", lines[key_line_number].strip())
                if result is not None:
                    key_elements_to_check.append(result.group(1))

    with open(glossary_path, 'r', encoding="utf-8") as file:
        content = file.read()
        # print("----------\nGloassary check:")
        for key_element in key_elements_to_check:
            status = True if key_element in content else False
            if status is False:
                terms_to_fix.append(key_element)
            # TODO: Change to logs
            # text_status = colored(
            #     "yes", "green") if status else colored("no", "red")
            # print(f"{key_element}: {text_status}")

    return terms_to_fix


def check_biblio(file_path: str, bibliography_path: str) -> list:
    """Check if bibliography links in bibliography .tex file

    Args:
        file_path (str): path to file to check
        bibliography_path (str): path to bibliography.tex file

    Returns:
        list: need to fix bibliography links list
    """

    line_number = 0
    in_list = False
    biblio_lists = []

    biblio_list_begin_line = 0
    biblio_list_end_line = 0

    biblio_links_to_fix = []

    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

        for line_number, line in enumerate(lines):
            if BEGIN_LIST + "{" + BIBLIO_LINK + "}" in line:
                biblio_list_begin_line = line_number
                in_list = True
            if (in_list is True and END_LIST in line):
                biblio_list_end_line = line_number + 1
                in_list = False
                biblio_lists.append(
                    (biblio_list_begin_line, biblio_list_end_line))

    biblio_links_to_check = []

    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for biblio_list in biblio_lists:
            for biblio_line_number in range(biblio_list[0] + 1, biblio_list[1] - 1):
                result = re.search(
                    r"\\scnitem{\\scncite{([A-z0-9]+)}}", lines[biblio_line_number].strip())
                if result is not None:
                    biblio_links_to_check.append(result.group(1))

    with open(bibliography_path, 'r', encoding="utf-8") as file:
        content = file.read()
        # print("----------\nBibliography check:")
        for biblio_link in biblio_links_to_check:
            status = True if biblio_link in content else False
            if status is False:
                biblio_links_to_fix.append(biblio_link)
            # TODO: Change to logs
            # text_status = colored(
            #     "yes", "green") if status else colored("no", "red")
            # print(f"{biblio_link}: {text_status}")

    return biblio_links_to_fix

def get_chapter_name(file_path:str) -> str:
    chapter_name = "No chapter name"

    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        result = re.search(r"\\chapter{([А-я ,:?!])}", content)
        if result is not None:
            chapter_name = result.group(1)

    return chapter_name
                


def get_authors(file_path: str) -> list:
    """Get chapter authors

    Args:
        file_path (str): path to chapter file

    Returns:
        list: list of chapter authors
    """

    line_number = 0
    in_list = False
    authors_lists = []

    authors_list_begin_line = 0
    authors_list_end_line = 0

    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

        for line_number, line in enumerate(lines):
            if BEGIN_LIST + "{" + AUTHORS + "}" in line:
                authors_list_begin_line = line_number
                in_list = True
            if (in_list is True and END_LIST in line):
                authors_list_end_line = line_number + 1
                in_list = False
                authors_lists.append(
                    (authors_list_begin_line, authors_list_end_line))

    authors_to_contact = []

    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for author_list in authors_lists:
            for author_line_number in range(author_list[0] + 1, author_list[1] - 1):
                result = re.search(
                    r"\\scnitem{([А-я.~ ]+)}", lines[author_line_number].strip())
                if result is not None:
                    authors_to_contact.append(result.group(1))

    return authors_to_contact


def main(args: dict):
    """Check if all key terms are in glossary file and
      all bibliographic links are in bibliography file

    Args:
        args (dict): dictionary of argument
    """

    for key, value in args.items():
        args[key] = os.path.abspath(value)  # Convert to absolute path

    file_path = args[FILE_PATH]
    glossary_path = args[GLOSSARY_PATH]
    biblio_path = args[BIBLIO_PATH]

    final_result = True

    print(f"\nCheck {file_path}")

    terms_to_fix = check_terms(file_path, glossary_path)
    final_result &= True if not terms_to_fix else False

    biblio_links_to_fix = check_biblio(file_path, biblio_path)
    final_result &= True if not biblio_links_to_fix else False

    authors_to_contact = get_authors(file_path)

    print("----------\nChecks result: " + (colored("Passed", "green")
          if final_result is True else colored("Error", "red")))

    if terms_to_fix:
        print("Need to add terms to glossary: ")
        for term in terms_to_fix:
            print("- " + term)

    if biblio_links_to_fix:
        print("Need to add biblio links to bibliography: ")
        for biblio_link in biblio_links_to_fix:
            print("- " + biblio_link)

    if (not final_result) and authors_to_contact:
        print("Please contact these authors to apply fixes: ")
        for author in authors_to_contact:
            print("- " + author)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(dest=FILE_PATH, type=str,
                        help="Chapter TeX file to check")
    parser.add_argument('-g', '--glossary_file', dest=GLOSSARY_PATH, type=str,
                        help="Glossary TeX file")
    parser.add_argument('-b', '--biblio_file', dest=BIBLIO_PATH, type=str,
                        help="Bibliography TeX file to check")

    PARSED_ARGS = parser.parse_args()

    main(vars(PARSED_ARGS))
