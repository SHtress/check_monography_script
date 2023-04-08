__author__ = "Viktor \"Vikort\" Markovets"


import re
import sys
from string import Template

from termcolor import colored


def parse_from_file(path: str) -> list:

    biblio_template = Template('''
    \\scnciteheader{$link}
    \\scnfullcite{$link}
    \\begin{scnreltolist}{библиографическая ссылка}
        $ref
    \\end{scnreltolist}
    ''')

    ref_template = Template("\\scnitem{$chapter\\ref{$ref} \\nameref{$ref}}")

    result = []
    biblio_links_to_tex = []
    biblio_links = dict()
    current_label = ""
    not_check = False

    with open(path, "r", encoding="utf8") as file:
        for line in file:

            current_label_search_result = re.search(
                r'\\label{([a-z_]+)}', line)

            if current_label_search_result is not None:
                current_label = current_label_search_result.group(1)

            # To skip bibliography in head. Need to optimize.
            if "\\begin{scnrelfromlist}{библиографическая ссылка}" in line:
                not_check = True

            if "\\end{scnrelfromlist}" in line and not_check is True:
                not_check = False
            elif not_check is True:
                continue

            res = re.findall(r'\\scncite\{[\w\-\d]+\}', line)
            for i in res:
                if "\\scnitem{" + i + "}" not in result:
                    result.append("\\scnitem{" + i + "}")

                chapter_flag = "Глава " if "chapter" in current_label else ""

                if not any(i in biblio_link for biblio_link in biblio_links):
                        biblio_links[i] = [ref_template.substitute(chapter=chapter_flag,ref=current_label)]
                else:
                    new_ref = ref_template.substitute(chapter=chapter_flag,ref=current_label)
                    if new_ref not in biblio_links[i]:
                        biblio_links[i].append(new_ref)                

    for key in biblio_links:
        refs = []
        for ref in biblio_links.get(key):
            refs.append(ref)
        biblio_link_to_tex = biblio_template.substitute(link=key, ref="\n\t\t".join(refs))
        biblio_links_to_tex.append(biblio_link_to_tex)

    with open("biblio_list_for_chapter.tex", 'w', encoding="utf8") as file:
        for line in result:
            file.write("\t" + line + '\n')

    with open("biblio_list_for_bibliography.tex", 'w', encoding="utf8") as file:
        for line in biblio_links_to_tex:
            file.write(line)

    print("bibliography parsed", bool(result))

    return biblio_links_to_tex


if __name__ == "__main__":
    if len(sys.argv) == 2:
        parse_from_file(sys.argv[1])
