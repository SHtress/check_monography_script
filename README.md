# Check script for monography

Python script for checking glossary and bibliography for [monography](https://github.com/ostis-ai/monography2022).

It checks if key terms in your chapter are in `glossary.tex` and biblio links are in `bibliography.tex`.

## Quick start

To check all monography run in your monogrpahy directory with command line:

```sh
git clone https://github.com/SHtress/check_monography_script
cd check_monography_script
./check_monography
```

## Usage

From your command line:

```sh
./check_term_biblio.py 'PATH_TO_CHAPTER' -g 'PATH_TO_GLOSSARY' -b 'PATH_TO_BIBLIOGRAPHY'
```

`PATH_TO_YOUR_FILE` - path to your chapter .tex file;

`PATH_TO_GLOSSARY` - path to glossary.tex;

`PATH_TO_BIBLIOGRAPHY_FILE` - path to bibliography.tex;

## Output example

Check passed:
```
Check /home/shtr3s/monography2022/author/part2/chapter_lang.tex
----------
Checks result: Passed
```

Check didn't pass:
```
Check /home/shtr3s/monography2022/author/part2/chapter_top_ontologies.tex
----------
Checks result: Error
Need to add terms to glossary: 
- Ядро базы знаний ostis-системы
Need to add biblio links to bibliography: 
- Dobrov2006
- Gorshkov2016
- Iqbal2013
Please contact these authors to apply fixes: 
- Бутрин С.В.
- Шункевич Д.В.
```

If check didn't pass in log you will see:
- what terms should be added to glossary;
- what biblio links should be added to bibliography;
- who to contact about applying fixes.
