# GPX Tools

GPX ファイルを扱うための Web ツール集です。GPX を KML / GeoJSON へ変換したり、地図上に軌跡を表示したりできます。

## 機能

- **Converter** — GPX ファイルを KML または GeoJSON 形式へ変換し、ダウンロードできます。複数ファイルの同時アップロードに対応しています。
- **Map** — GPX の軌跡を Leaflet ベースの地図上に表示します。新しい GPX をアップロードすると、既存の軌跡を消してから描画します。

## 構成

3 つのサービスを Docker Compose で起動します。

| サービス | 技術 | 役割 |
| --- | --- | --- |
| `nginx` | nginx | リバースプロキシ。静的なトップページと Map ページの配信、`api` / `converter` への振り分けを行います。 |
| `converter` | Streamlit | GPX 変換用の UI。アップロードされたファイルを `api` に送り、変換結果を返します。 |
| `api` | Flask + gpxpy | GPX をパースして KML / GeoJSON を生成する変換 API。 |

### ルーティング

`nginx` は `41100` 番ポートで待ち受け、以下のように振り分けます。

- `/` — トップページ（リンク集）
- `/map/` — 地図表示ページ
- `/converter/` — 変換 UI（Streamlit）
- `/api/` — 変換 API（Flask）

## 起動方法

[Docker](https://www.docker.com/) と Docker Compose が必要です。

```bash
docker compose up --build
```

起動後、ブラウザで以下にアクセスします。

```
http://localhost:41100/
```

## API

### `POST /convert`

アップロードされた GPX ファイルを変換します。

- **リクエスト** — `multipart/form-data` で 1 つ以上の `.gpx` ファイルを送信します。
- **クエリパラメータ**
  - `format` — `kml`（デフォルト）または `geojson`
- **レスポンス** — 変換後の KML または GeoJSON。

#### 例

```bash
curl -X POST "http://localhost:41100/api/convert?format=geojson" \
  -F "file=@track.gpx" \
  -o track.geojson
```

## ライセンス

[LICENSE](LICENSE) を参照してください。
