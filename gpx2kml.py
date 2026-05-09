import argparse
import gpxpy
import xml.etree.ElementTree as ET


def main():
    args = get_args()
    gpx = read_gpx(args.input)
    kml = convert_gpx_to_kml(gpx)
    write_kml(args.output, kml)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    return args


def read_gpx(path):
    with open(path, 'r', encoding='utf-8') as f:
        gpx = gpxpy.parse(f)
    return gpx


def convert_gpx_to_kml(gpx):
    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')
    for track in gpx.tracks:
        for segment in track.segments:
            placemark = ET.SubElement(document, 'Placemark')
            line_string = ET.SubElement(placemark, 'LineString')
            coordinates = ' '.join(
                '{},{},{}'.format(
                    point.longitude,
                    point.latitude,
                    point.elevation
                )
                for point in segment.points
            )
            ET.SubElement(line_string, 'coordinates').text = coordinates
    return kml


def write_kml(path, kml):
    with open(path, 'wb') as f:
        f.write(ET.tostring(kml))


if __name__ == '__main__':
    main()
