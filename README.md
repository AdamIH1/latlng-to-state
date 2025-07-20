# latlng-to-state

**latlng-to-state** is a lightweight Python package that maps latitude/longitude points to U.S. state geometries using geospatial containment and intersection checks. It comes with built-in U.S. state polygon data (census), us zipcode centroid data (census), and works seamlessly with `GeoPandas` and `shapely`.

---

## 🔧 Features 

- 🗺️ **Spatial Lookup**: Determine if a lat/lng point is contained within or intersects with a polygon (e.g., a U.S. state).
- 📦 **Built-in Data**: Includes preloaded U.S. state geometries (as a `.parquet` file).
- 🧪 **Clean API**: Simple utility functions for integrating geospatial logic into your own workflows.
- 🧱 **Modular Design**: Organized into utilities and core logic for easy extension.

---

## 📦 Installation

```bash
pip install latlng-to-state
```

> Note: Requires Python ≥ 3.9

---

## 🚀 Quickstart

```python
import geopandas as gpd
from latlng_to_state.datasets import load_us_geometry
from latlng_to_state.core.lookup import lookup_geometry_by_point

# Load built-in U.S. state geometries
gdf = load_us_geometry()

# Sample lat/lng in Texas
lat, lng = 31.9686, -99.9018

# Lookup state name
state_name = lookup_geometry_by_point(lat, lng, gdf, check_type="contain", return_col="NAME")

print(state_name)  # Output: Texas
```

---

## 🧠 API

### `lookup_geometry_by_point`

```python
lookup_geometry_by_point(
    lat: float,
    lng: float,
    gdf: geopandas.GeoDataFrame,
    check_type: Optional[str] = None,
    return_col: str = "NAME"
) -> Optional[Union[str, int, float]]
```

Check whether a given lat/lng point falls inside or intersects with any geometry in a GeoDataFrame.

- `lat`, `lng`: Coordinates of the point.
- `gdf`: A `GeoDataFrame` containing geometries (e.g., U.S. states).
- `check_type`: `"contain"`, `"intersect"`, or `None` (tries contain then intersect).
- `return_col`: Column to return (e.g., `"NAME"` for state name).

Returns the matched value from the `return_col` column, or `None` if no match.

---

### `load_us_geometry`

```python
from latlng_to_state.datasets import load_us_geometry

gdf = load_us_geometry()
```

Loads the built-in U.S. state geometry data as a `GeoDataFrame`.

---

## 📁 Included Data

The package includes:
- A U.S. state geometry dataset (in `parquet` format) bundled under `latlng_to_state/datasets/data`.

---

## 📦 Dependencies

- `geopandas`
- `shapely`
- `pandas`

Install automatically via pip, or add them manually if needed:

```bash
pip install geopandas shapely pandas
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🧑‍💻 Contributing

Contributions welcome! Feel free to open issues or submit PRs on [GitHub](https://github.com/AdamIH1/latlng-to-state/tree/main).

