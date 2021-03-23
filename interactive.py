import base64
import io

import streamlit as st
import tabulator

import analyze_genders


FIELDS = ['field', 'paper_id', 'conf', 'year', 'authors']


def get_table_download_link(df):
    """
    Generates a link allowing the data in a panda dataframe to be downloaded
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'

uploaded_file = st.file_uploader('Input file for analysis', type='csv')
has_header = st.checkbox('CSV file has header', value=True)

if uploaded_file is not None:
    file_like = io.BytesIO(uploaded_file.getvalue())

    # Set the header row if needed
    if has_header:
        header_row = 1
    else:
        header_row = None

    # Get the column headers parsed from the file
    stream = tabulator.Stream(file_like, scheme='stream', format='csv', headers=header_row)
    stream.open()
    if stream.headers:
        file_headers = stream.headers
    else:
        file_headers = list(range(len(stream.sample[0])))

    # Set up the field mapping
    header_map = {}
    for field in FIELDS:
        # Check if there is a match already by name
        try:
            index = file_headers.index(field)
        except ValueError:
            index = len(file_headers)

        value = st.selectbox(label=field, options=file_headers + [None], index=index)
        if value is not None:
            header_map[field] = value

    genders = analyze_genders.load_data_file(file_like, header_row=header_row, header_map=header_map)
    analyze_genders.populate_genders(genders)
    df = analyze_genders.dataframe(genders)

    st.write(df)
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
