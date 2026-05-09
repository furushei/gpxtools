import os
import streamlit as st
import requests


API_URL = os.getenv('API_URL', 'http://localhost:41102')
REQUEST_TIMEOUT_SECONDS = 30


def convert_gpx(uploaded_files):
    files = {}
    for idx, uploaded_file in enumerate(uploaded_files):
        if uploaded_file.name.lower().endswith('.gpx'):
            files[f'file{idx}'] = (uploaded_file.name, uploaded_file.getvalue(), 'application/gpx+xml')
    try:
        response = requests.post(
            f'{API_URL}/convert',
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


def get_default_kml_filename(uploaded_files):
    if not uploaded_files:
        return 'unnamed.kml'

    base_name = os.path.splitext(uploaded_files[0].name)[0]
    return f'{base_name}.kml'


def main():
    st.title('GPX to KML Converter')
    st.write('Upload a GPX file and download the converted KML file.')

    if 'kml_data' not in st.session_state:
        st.session_state['kml_data'] = None

    uploaded_files = st.file_uploader('Choose a GPX file', type='gpx', accept_multiple_files=True)

    if not uploaded_files:
        st.info('Please upload a GPX file to convert.')
        st.session_state['kml_data'] = None

    if st.button('Convert to KML', disabled=not uploaded_files):
        with st.spinner('Converting...'):
            kml, error = convert_gpx(uploaded_files)
        if error:
            st.error(error)
            st.session_state['kml_data'] = None
        else:
            st.session_state['kml_data'] = kml
            st.success('Conversion successful!')

    file_name = st.text_input('KML File Name', value=get_default_kml_filename(uploaded_files))
    if st.session_state['kml_data'] is not None:
        st.download_button(
            label='Download KML',
            data=st.session_state['kml_data'],
            file_name=file_name,
            mime='application/vnd.google-earth.kml+xml',
            on_click='ignore'
        )


if __name__ == '__main__':
    main()
