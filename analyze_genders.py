import collections
import csv
import json
import glob
import sys

import genderComputer


def infer_genders():
    """
    Construct a dictionary of first author counts by gender from
    DBLP JSON files which match a particular glob pattern
    """
    gc = genderComputer.GenderComputer()
    gender_counts = collections.defaultdict(lambda: {})

    for json_file in glob.glob('data/*.json'):
        conf = json_file.split('-')[0].split('/')[1]
        year = int(json_file.split('-')[1].split('.')[0])
        if year not in gender_counts[conf]:
            gender_counts[conf][year] = collections.defaultdict(lambda: 0)
            gender_counts[conf][year]['conf'] = conf
            gender_counts[conf][year]['year'] = year

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
                gender_counts[conf][year][gender] += 1

    return gender_counts.values()


def main():
    # Redirect stdout because the genderComputer library
    # prints things without a way to disable it
    orig_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')

    # Infer genders for data files in the data/ directory
    genders = infer_genders()

    # Write a header row
    sys.stdout = orig_stdout
    csv_writer = csv.writer(sys.stdout)
    columns = ['conf', 'year', 'female', 'male', 'unisex', 'unknown', 'm/f']
    csv_writer.writerow(columns)

    # Write values for each conference
    for years in genders:
        for conf in years.values():
            csv_writer.writerow([conf[key] for key in columns])


if __name__ == '__main__':
    main()
