#!/usr/bin/env python

import pathlib

import analyze_genders


def main():
    # Infer genders for data files in the data/ directory
    df = analyze_genders.dataframe()

    # Add a new column of first names
    df['first_name'] = df['author_name'].str.split(' ', expand=True)[0]

    # Find only the first authors
    first_authors = df[df['author_position'] == 0]

    # Get first authors with an unknown gender
    unknown_gender = first_authors[first_authors['unknown'] | first_authors['unisex']]

    # Output some data needed by the paper
    pathlib.Path('paper/').mkdir(exist_ok=True)
    with open('paper/DA_vars.tex', 'w') as vars_file:
        vars_file.write('\\newcommand{\\DAUnknownGender}{%d}\n' % unknown_gender['first_name'].nunique())


if __name__ == '__main__':
    main()
