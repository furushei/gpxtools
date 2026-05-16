# GPX Tools

A collection of web tools for working with GPX files. Convert GPX to KML / GeoJSON, or visualize tracks on a map.

## Features

- **Converter** — Convert GPX files to KML or GeoJSON and download the result. Multiple files can be uploaded at once.
- **Map** — Display GPX tracks on a Leaflet-based map. Uploading a new GPX clears the existing tracks before drawing.

## Architecture

Three services are orchestrated with Docker Compose.

| Service | Stack | Role |
| --- | --- | --- |
| `nginx` | nginx | Reverse proxy. Serves the static landing page and the Map page, and routes requests to `api` / `converter`. |
| `converter` | Streamlit | UI for GPX conversion. Sends uploaded files to `api` and returns the converted output. |
| `api` | Flask + gpxpy | Conversion API that parses GPX and generates KML / GeoJSON. |

### Routing

`nginx` listens on port `41100` and routes as follows.

- `/` — Landing page (links)
- `/map/` — Map view
- `/converter/` — Conversion UI (Streamlit)
- `/api/` — Conversion API (Flask)

## Getting Started

[Docker](https://www.docker.com/) and Docker Compose are required.

```bash
docker compose up -d --build
```

Once running, open the following in your browser.

```
http://localhost:41100/
```

## API

### `POST /convert`

Converts the uploaded GPX files.

- **Request** — Send one or more `.gpx` files as `multipart/form-data`.
- **Query parameters**
  - `format` — `kml` (default) or `geojson`
- **Response** — The converted KML or GeoJSON.

#### Example

```bash
curl -X POST "http://localhost:41100/api/convert?format=geojson" \
  -F "file=@track.gpx" \
  -o track.geojson
```

## License

See [LICENSE](LICENSE).
