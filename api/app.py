from flask import Flask, Response, request
import gpxpy
import xml.etree.ElementTree as ET
from typing import List, Tuple


class Track:
    def __init__(self, name: str, points: List[Tuple[float, float, float]]):
        self.name = name
        self.points = points


def parse_gpx(gpx_content: str) -> List[Track]:
    gpx = gpxpy.parse(gpx_content)
    tracks = []
    for track in gpx.tracks:
        for segment in track.segments:
            points = [(point.latitude, point.longitude, point.elevation) for point in segment.points]
            tracks.append(Track(track.name or 'Unnamed Track', points))
    return tracks


def make_kml(tracks: List[Track]) -> str:
    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')
    for track in tracks:
        placemark = ET.SubElement(document, 'Placemark')
        name = ET.SubElement(placemark, 'name')
        name.text = track.name
        line_string = ET.SubElement(placemark, 'LineString')
        coordinates = ' '.join(
            '{},{},{}'.format(lon, lat, ele)
            for lat, lon, ele in track.points
        )
        ET.SubElement(line_string, 'coordinates').text = coordinates
    return ET.tostring(kml, encoding='utf-8', xml_declaration=True)


def get_base_name(filename):
    return filename.rsplit('.', 1)[0] if '.' in filename else filename


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def root():
        return {"message": "Welcome to the GPX2KML API!"}

    @app.route('/convert', methods=['POST'])
    def convert():
        tracks = []
        for file_key in request.files:
            uploaded_file = request.files[file_key]
            if uploaded_file.filename.lower().endswith('.gpx'):
                gpx_content = uploaded_file.read().decode('utf-8')
                tmp_tracks = parse_gpx(gpx_content)
                if len(tmp_tracks) == 1:
                    tmp_tracks[0].name = get_base_name(uploaded_file.filename)
                else:
                    for idx, track in enumerate(tmp_tracks):
                        track.name = f'{get_base_name(uploaded_file.filename)} ({idx + 1}/{len(tmp_tracks)})'
                tracks.extend(tmp_tracks)
        if not tracks:
            return Response('No valid GPX files uploaded.', status=400)

        kml_content = make_kml(tracks)
        return Response(kml_content, mimetype='application/vnd.google-earth.kml+xml')

    return app


app = create_app()
