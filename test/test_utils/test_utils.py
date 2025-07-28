import pytest
import geopandas as gpd
from shapely.geometry import Polygon

from latlng_to_state.utils.utils_core import (
    _point_within_geometry
    , _point_intersects_geometry
)

@pytest.fixture
def sample_gdf():
    """Creates a GeoDataFrame with two square polygons and names."""
    data = {
        "NAME": ["SquareOne", "SquareTwo"],
        "geometry": [
            Polygon([(0, 0), (0, 1), (1, 1), (1, 0)]),        # SquareOne
            Polygon([(2, 2), (2, 3), (3, 3), (3, 2)])         # SquareTwo
        ]
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")

def test_point_within_geometry_match(sample_gdf):
    # Point inside SquareOne
    lat, lng = 0.5, 0.5
    result = _point_within_geometry(lat, lng, sample_gdf)
    assert result is not None
    assert result["NAME"] == "SquareOne"

def test_point_within_geometry_none(sample_gdf):
    # Point outside all geometries
    lat, lng = 10.0, 10.0
    result = _point_within_geometry(lat, lng, sample_gdf)
    assert result is None

def test_point_intersects_geometry_match(sample_gdf):
    # Point on the edge of SquareOne — should not be 'within'
    # but will 'intersect'
    lat, lng = 0.0, 0.5
    result = _point_intersects_geometry(lat, lng, sample_gdf)
    assert result is not None
    assert result["NAME"] == "SquareOne"

def test_point_intersects_geometry_none(sample_gdf):
    # Point completely outside both squares
    lat, lng = -5.0, -5.0
    result = _point_intersects_geometry(lat, lng, sample_gdf)
    assert result is None
