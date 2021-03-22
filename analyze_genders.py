import codecs
import collections
import csv
import io
import itertools
import json
import glob
import os
import random
import re
import sys

from bs4 import BeautifulSoup
import genderComputer
import matplotlib
import matplotlib.ticker as ticker
import pandas as pd
import tabulator


def load_data_file(fh, header_row=1, header_map=None):
    """
    Read data from a file for analysis
    """
    gender_counts = []
    with tabulator.Stream(fh, scheme='stream', format='csv', headers=header_row) as stream:
        if not stream.headers and not header_map:
            sys.stderr.write('If no headers are available, a map from column names to indices is required.')
            sys.exit(1)

        if header_map is None:
            header_map = {
                'authors': 'authors',
            }

            # Add optional mappings if they exist
            if stream.headers:
                if 'paper_id' in stream.headers:
                    header_map['paper_id'] = 'paper_id'
                if 'field' in stream.headers:
                    header_map['field'] = 'field'
                if 'conf' in stream.headers:
                    header_map['conf'] = 'conf'
                if 'year' in stream.headers:
                    header_map['year'] = 'year'

                if 'author_position' in stream.headers and 'author_name' in stream.headers:
                    header_map['author_position'] = 'author_position'
                    header_map['author_name'] = 'author_name'
                    del header_map['authors']

        for (paper_id, row) in enumerate(stream.iter(keyed=header_row is not None)):
            datum = collections.OrderedDict(
                field=None,
                paper_id=paper_id,
                conf=None,
                year=None,
                author_position=None,
                author_id=None,
                author_name=None,
                male=0,
                female=0,
                unisex=0,
                unknown=0,
            )

            if 'authors' in header_map:
                # Read multiple authors assuming they are comma or "and" separated
                skipped = 0
                for (author_position, author_name) in enumerate(re.split(',|\Wand\W', row[header_map['authors']])):
                    author_name = author_name.strip()
                    if author_name == 'and':
                        skipped += 1
                    else:
                        datum = datum.copy()
                        datum['author_position'] = author_position - skipped
                        datum['author_name'] = author_name
                        datum['author_id'] = author_name

                        gender_counts.append(datum)
            else:
                # Read everything using the given header mapping
                for (orig, this) in header_map.items():
                    datum[orig] = row[this]

                if datum['author_id'] is None:
                    datum['author_id'] = datum['author_name']

                gender_counts.append(datum)

    return gender_counts


def load_data_dblp(field=None):
    """
    Construct a dictionary of first author counts by gender from
    DBLP JSON files which match a particular glob pattern
    """
    gender_counts = []

    # If no field is specified, use them all
    if field is None:
        field = '**'
    glob_path = os.path.join('data', field, '*.json')

    for json_file in glob.glob(glob_path):
        field = json_file.split('-')[0].split('/')[1].replace('_', ' ')
        conf = json_file.split('-')[0].split('/')[-1].upper()

        data = json.load(open(json_file))['result']['hits'].get('hit', [])
        for paper in data:
            # Skip papers which are for some reason missing author info
            if 'authors' not in paper['info']:
                continue

            author_info = paper['info']['authors']['author']

            # Handle single author papers which do not
            # wrap the single author in list
            if not isinstance(author_info, list):
                author_info = [author_info]

            year = int(paper['info']['year'])

            for (index, author) in enumerate(author_info):
                # Start author indexes at 1
                index += 1

                # Initialize a new data point
                datum = collections.OrderedDict(
                    field=field,
                    paper_id=paper['@id'],
                    conf=conf,
                    year=year,
                    author_position=None,
                    author_id=None,
                    author_name=None,
                    male=0,
                    female=0,
                    unisex=0,
                    unknown=0
                )

                # Track which number this author is
                datum['author_position'] = index

                # Extract the author name and ID
                if isinstance(author, dict):
                    author_name = author['text']
                    author_id = author['@pid']
                elif isinstance(author, str):
                    author_name = author_id = author
                else:
                    raise TypeError('Invalid author name')

                # Remove numerical suffixes
                author_name = author_name.rstrip(' 0123456789')
                datum['author_name'] = author_name
                datum['author_id'] = author_id

                gender_counts.append(datum)

    # XXX Temporarily also parse HTML
    glob_path = os.path.join('data', field, '*.html')
    for html_file in glob.glob(glob_path):
        field = html_file.split('-')[0].split('/')[1].replace('_', ' ')
        conf = html_file.split('-')[0].split('/')[-1].upper()

        soup = BeautifulSoup(open(html_file).read(), 'lxml')
        for (paper_index, paper) in enumerate(soup.select('cite.data')):
            # Year is either the content property of a meta element
            # or contained within the text of a span element
            date = paper.select_one('[itemprop="datePublished"]')
            if date.name == 'meta':
                year = int(date.attrs['content'])
            elif date.name == 'span':
                year = int(date.get_text())
            else:
                raise ValueError('Could not find publication year')

            for (index, author) in enumerate(paper.select('[itemprop="author"] [itemprop="name"]')):
                # Start author indexes at 1
                index += 1

                # Initialize a new data point
                datum = collections.OrderedDict(
                    field=field,
                    paper_id=html_file + str(paper_index),
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

                # Remove numerical suffixes
                author_name = author_id = author.attrs['title'].rstrip(' 0123456789')
                datum['author_name'] = author_name
                datum['author_id'] = author_id

                gender_counts.append(datum)

    return gender_counts

def populate_genders(data):
    """
    Attempt to infer a gender for each row in the dataset.

    For many reasons, not limited to the following,
    this is a highly imperfect analysis:

    1. Many names are commonly used by people of different gender identities.
    2. An individual may not have a name traditionally used
       by someone of their gender identity.
    3. Only binary gender identities are considered.
    """
    # Redirect stdout because the genderComputer library
    # prints things without a way to disable it
    orig_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')

    gc = genderComputer.GenderComputer()
    for datum in data:
        # Attempt to predict gender
        # TODO Include author country
        #      (perhaps from affiliation via DBLP, but not perfect)
        gender = gc.resolveGender(datum['author_name'], None)
        if gender is None:
            gender = 'unknown'
        datum[gender] += 1

    sys.stdout = orig_stdout

def _assume_gender_weighted(df):
    """
    Assume the gender of unknown/unisex names to be proportional
    to the ratio of known male/female names in the remainder
    """

    # Calculate gender ratio
    known = df[~df['unisex'] & ~df['unknown']]
    female_authors = known[known['female']]['author_id'].nunique()
    male_authors = known[known['male']]['author_id'].nunique()
    female_ratio = female_authors / (female_authors + male_authors)

    # Assume a gender for each author with unknown
    # gender based on the observed distribution
    author_genders = {}
    for author in df[df['unknown'] | df['unisex']]['author_id'].unique():
        if random.random() <= female_ratio:
            author_genders[author] = 'female'
        else:
            author_genders[author] = 'male'

    # Set the assumed gender on the original dataframe
    for index in df.index:
        if df.loc[index, 'unknown'] or df.loc[index, 'unisex']:
            gender = author_genders[df.loc[index, 'author_id']]
            df.loc[index, gender] = True


def _assume_gender_static(df, gender='female'):
    """
    Use a single static value for genders which could not be inferred
    """
    unknown = df['unknown'] | df['unisex']
    if gender == 'female':
        df.loc[unknown, 'female'] = True
        df.loc[unknown, 'male'] = False
    elif gender == 'male':
        df.loc[unknown, 'male'] = True
        df.loc[unknown, 'female'] = False


def dataframe(genders=None, field=None, exclude=None, assume=_assume_gender_weighted):
    """
    Return the data as a Pandas DataFrame
    """
    # Infer genders for data files in the data/ directory
    if genders is None:
        genders = load_data_dblp(field)
        populate_genders(genders)
    elif field is not None:
        raise ValueError("Can't specify both data and field")

    df = pd.DataFrame(genders)

    # Optionally exclude some conferences
    if exclude:
        df = df[~df['conf'].isin(exclude)]

    # Convert gender columns to booleans
    df['male'] = df['male'] == 1
    df['female'] = df['female'] == 1
    df['unisex'] = df['unisex'] == 1
    df['unknown'] = df['unknown'] == 1

    # Assume the gender of those authors who could not automatically inferred
    if assume:
        assume(df)

    # Relabel VLDB to VLDB/PVLDB
    df.loc[df.conf == 'vldb', 'conf'] = 'vldb/pvldb'

    # Find the index of the last author of each
    # paper and add to the original data frame
    last_author_index = df.groupby(['paper_id'], sort=False)['author_position'].max().to_frame()
    first_paper = df.groupby(['author_id'], sort=False)['year'] \
                    .min().to_frame()
    df = df.join(last_author_index, on='paper_id', rsuffix='_last')
    df = df.join(first_paper, on='author_id', rsuffix='_first_paper') \
           .sort_values(['paper_id', 'author_position'])

    return df


def _first_female_author(group):
    # Check for the first author of a paper being female
    return group['female'].iloc[0]


def _last_female_author(group):
    # Check for the last author of a paper being female
    return group['female'].iloc[group['author_position_last'].iloc[0] - 1]


def _any_female_author(group):
    # Check for any author of a paper being female
    return group['female'].any()


def _all_female_author(group):
    # Check for all authors of a paper being female
    return group['female'].all()


def aggregate_authorship(df, group_attrs=['conf', 'year'], funcs=None):
    aggregates = {}
    if funcs is None:
        funcs = {
            'first': _first_female_author,
            'last': _last_female_author,
            'any': _any_female_author,
            'all': _all_female_author
        }
    for (name, fn) in funcs.items():
        # First group by paper ID to calculate values per paper
        grouped = df.groupby(['paper_id'] + group_attrs).apply(fn)

        if not grouped.empty:
            # Then group by conference and year and calculate the percentage
            df_agg = grouped.to_frame('female')
            aggregates[name] = df_agg.groupby(group_attrs).mean().multiply(100)

    return aggregates


def plot_authors(df, plot_label, save=None, header=True):
    # Calculate the rolling mean across three years
    rolling_mean = df.unstack(level=0).sort_values(['year']).ffill() \
                     .rolling(window=3).mean()

    # Generate a simple line plot
    if header:
        plot_title = 'Female authors by year (%s)' % plot_label
    else:
        plot_title = None
    fig = rolling_mean.plot(figsize=(15, 8), title=plot_title)

    # Set the markers
    markers = itertools.cycle((',', '+', '.', 'o', '*', 'x', '^', 'P'))
    for line in fig.get_lines():
        line.set_marker(next(markers))

    # Add x-axis labels every other year
    fig.xaxis.set_major_locator(ticker.MultipleLocator(5))

    # y-axis is always a percentage of all papers
    fig.set_ylabel('% of papers')

    # Strip the extra group part from legends
    fig.legend([c.split(', ')[1].rstrip(')')
                for c in fig.get_legend_handles_labels()[1]])

    # Optionally save to file
    if save:
        # Set matplotlib parameters
        matplotlib.use('pgf')
        matplotlib.rcParams.update({
            'pgf.texsystem': 'pdflatex',
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
            'font.size': 20,
        })

        # Calculate the filename
        if save is True:
            filename = plot_label.replace(' ', '_')
        else:
            filename = save
        filename += '.pgf'

        fig.figure.set_tight_layout(True)
        fig.figure.savefig(os.path.join('output', filename))


def main():
    pd.set_option('display.max_columns', None)
    if sys.stdin.isatty():
        # Load data for DBLP files in the data/ directory
        genders = load_data_dblp(field='DB')
        dblp = True
    else:
        # Load data provided on standard input
        genders = load_data_file(sys.stdin.buffer)
        dblp = False

    # Add the predicted genders to the data
    populate_genders(genders)

    # Write a header row
    csv_writer = csv.writer(open(os.path.join('output', 'gender.csv'), 'w'))
    columns = genders[0].keys()
    csv_writer.writerow(columns)

    # Write values for each conference
    for row in genders:
        csv_writer.writerow(row.values())

    # Save plots to file
    if dblp:
        exclude = ['PODS']
    else:
        exclude = None
    df = dataframe(genders, exclude=exclude)
    aggregates = aggregate_authorship(df)
    if aggregates:
        plot_authors(aggregates['all'], 'all positions', save=True, header=False)
        plot_authors(aggregates['any'], 'any position', save=True, header=False)
        plot_authors(aggregates['first'], 'first author', save=True, header=False)
        plot_authors(aggregates['last'], 'last author', save=True, header=False)


    # Perform additional analysis only for the DBLP dataset
    if dblp:
        # Get all fields without conferences not in CS Rankings
        df = dataframe(exclude=['CIDR', 'DASFAA', 'DKE', 'EDBT'])

        aggregates = aggregate_authorship(df, group_attrs=['field', 'year'], funcs={'first': _first_female_author})
        plot_authors(aggregates['first'], 'first author', save='fields', header=False)


if __name__ == '__main__':
    main()
