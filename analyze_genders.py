import collections
import csv
import json
import glob
import sys

import genderComputer
import pandas as pd


def infer_genders():
    """
    Construct a dictionary of first author counts by gender from
    DBLP JSON files which match a particular glob pattern
    """
    # Redirect stdout because the genderComputer library
    # prints things without a way to disable it
    orig_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')

    gc = genderComputer.GenderComputer()
    gender_counts = []

    for json_file in glob.glob('data/*.json'):
        conf = json_file.split('-')[0].split('/')[1]
        year = int(json_file.split('-')[1].split('.')[0])

        data = json.load(open(json_file))['result']['hits']['hit']
        for paper in data:
            # Skip papers which are for some reason missing author info
            if 'authors' not in paper['info']:
                continue

            author_info = paper['info']['authors']['author']

            # Handle single author papers which do not
            # wrap the single author in list
            if not isinstance(author_info, list):
                author_info = [author_info]

            for (index, author) in enumerate(author_info):
                # Initialize a new data point
                datum = collections.OrderedDict(
                    conf=conf,
                    year=year,
                    author_position=None,
                    author_name=None,
                    male=0,
                    female=0,
                    unisex=0,
                    unknown=0
                )

                # Track which number this author is
                datum['author_position'] = index

                # Extract the author name
                if isinstance(author, dict):
                    author_name = author['text']
                elif isinstance(author, str):
                    author_name = author
                else:
                    raise TypeError('Invalid author name')

                # Remove numerical suffixes
                author_name = author_name.rstrip(' 0123456789')
                datum['author_name'] = author_name

                # Attempt to predict gender
                # TODO Include author country
                #      (perhaps from affiliation via DBLP, but not perfect)
                gender = gc.resolveGender(author_name, None)
                if gender is None:
                    gender = 'unknown'
                datum[gender] += 1

                gender_counts.append(datum)

    sys.stdout = orig_stdout
    return gender_counts


def dataframe():
    """
    Return the data as a Pandas DataFrame
    """
    # Infer genders for data files in the data/ directory
    genders = infer_genders()
    return pd.DataFrame(genders)


def main():
    # Infer genders for data files in the data/ directory
    genders = infer_genders()

    # Write a header row
    csv_writer = csv.writer(sys.stdout)
    columns = genders[0].keys()
    csv_writer.writerow(columns)

    # Write values for each conference
    for row in genders:
        csv_writer.writerow(row.values())


if __name__ == '__main__':
    main()
