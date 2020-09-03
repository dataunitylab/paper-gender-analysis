import collections
import csv
import json
import glob
import sys

import genderComputer


def genders_for_pattern(pattern):
    """
    Construct a dictionary of first author counts by gender from
    DBLP JSON files which match a particular glob pattern
    """
    gc = genderComputer.GenderComputer()
    gender_counts = collections.defaultdict(lambda: 0)

    for json_file in glob.glob(pattern):
        data = json.load(open(json_file))['result']['hits']['hit']
        for paper in data:
            author_info = paper['info']['authors']['author']
            for (index, author) in enumerate(author_info):
                # Only consider first authors for now
                if index > 0:
                    break

                # Extract the author name
                if isinstance(author, dict):
                    author_name = author['text']
                elif isinstance(author, str):
                    author_name = author
                else:
                    raise TypeError('Invalid author name')

                # Remove numerical suffixes
                author_name = author_name.rstrip(' 0123456789')

                # Attempt to predict gender
                # TODO Include author country
                #      (perhaps from affiliation via DBLP, but not perfect)
                gender = gc.resolveGender(author_name, None)
                if gender is None:
                    gender = 'unknown'
                gender_counts[gender] += 1

    return dict(gender_counts)


def main():
    # Redirect stdout because the genderComputer library
    # prints things without a way to disable it
    orig_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')

    # Get info for SIGMOD and VLDB
    sigmod_genders = genders_for_pattern('data/SIGMOD*.json')
    sigmod_genders['conf'] = 'SIGMOD'

    vldb_genders = genders_for_pattern('data/VLDB*.json')
    vldb_genders['conf'] = 'VLDB'

    # Write a header row
    sys.stdout = orig_stdout
    csv_writer = csv.writer(sys.stdout)
    columns = ['conf', 'female', 'male', 'unisex', 'unknown']
    csv_writer.writerow(columns)

    # Write values for each conference
    for conf in [sigmod_genders, vldb_genders]:
        csv_writer.writerow([conf[key] for key in columns])


if __name__ == '__main__':
    main()
