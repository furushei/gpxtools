import os
import streamlit as st
import requests


API_URL = os.getenv('API_URL', 'http://localhost:41102')
REQUEST_TIMEOUT_SECONDS = 30

FORMAT_OPTIONS = [
    {
        'display_name': 'KML',
        'format': 'kml',
        'extension': 'kml',
    },
    {
        'display_name': 'GeoJSON',
        'format': 'geojson',
        'extension': 'geojson',
    }
]


def convert_gpx(uploaded_files, *, format='kml'):
    files = {}
    for idx, uploaded_file in enumerate(uploaded_files):
        if uploaded_file.name.lower().endswith('.gpx'):
            files[f'file{idx}'] = (uploaded_file.name, uploaded_file.getvalue(), 'application/gpx+xml')
    try:
        response = requests.post(
            f'{API_URL}/convert?format={format}',
            files=files,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        return None, f'API request failed: {exc}'

    if response.status_code != 200:
        try:
            error_message = response.json().get('error', 'Unknown error')
        except ValueError:
            error_message = response.text.strip() or 'Unknown error'
        return None, f'Failed to convert GPX to KML: {error_message}'

    return response.content, None


def get_default_filename(uploaded_files, *, format='kml'):
    extension = next(option['extension'] for option in FORMAT_OPTIONS if option['format'] == format)

    if not uploaded_files:
        return f'unnamed.{extension}'

    base_name = os.path.splitext(uploaded_files[0].name)[0]
    return f'{base_name}.{extension}'


def main():
    st.set_page_config(page_title='GPX Converter', page_icon='🗺️')

    st.title('GPX Converter')

    if 'converted_data' not in st.session_state:
        st.session_state['converted_data'] = None

    uploaded_files = st.file_uploader('Choose a GPX file', type='gpx', accept_multiple_files=True)

    if not uploaded_files:
        st.info('Please upload a GPX file to convert.')
        st.session_state['converted_data'] = None

    format_option = st.selectbox('Select output format', options=[option['display_name'] for option in FORMAT_OPTIONS])
    format_type = next(option['format'] for option in FORMAT_OPTIONS if option['display_name'] == format_option)

    if st.button('Convert', disabled=not uploaded_files):
        with st.spinner('Converting...'):
            converted_data, error = convert_gpx(uploaded_files, format=format_type)
        if error:
            st.error(error)
            st.session_state['converted_data'] = None
        else:
            st.session_state['converted_data'] = converted_data
            st.success('Conversion successful!')

    file_name = st.text_input('File Name', value=get_default_filename(uploaded_files, format=format_type))
    if st.session_state['converted_data'] is not None:
        st.download_button(
            label=f'Download {format_option}',
            data=st.session_state['converted_data'],
            file_name=file_name,
            mime='application/vnd.google-earth.kml+xml',
            on_click='ignore'
        )


if __name__ == '__main__':
    main()
