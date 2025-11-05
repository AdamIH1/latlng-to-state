import pytest
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from latlng_to_state.core.lookup import lookup_geometry_by_point


@pytest.fixture
def sample_gdf():
    """Returns a GeoDataFrame with two square polygons and a 'NAME' column."""
    data = {
        "NAME": ["A", "B"],
        "geometry": [
            Polygon([(0, 0), (0, 1), (1, 1), (1, 0)]),  # Square A
            Polygon([(2, 2), (2, 3), (3, 3), (3, 2)])   # Square B
        ]
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")


def test_lookup_contain_match(sample_gdf):
    """
    Tests that a point located inside a polygon correctly returns the
    matching NAME when using 'contain' mode.
    """
    lat, lng = 0.5, 0.5
    result = lookup_geometry_by_point(
        lat, lng, sample_gdf, check_type="contain", return_col="NAME"
    )
    assert result == "A"


def test_lookup_intersect_match(sample_gdf):
    """
    Tests that a point lying on a polygon boundary is matched when using
    'intersect' mode.
    """
    lat, lng = 0.0, 0.5  # On the edge of Square A
    result = lookup_geometry_by_point(
        lat, lng, sample_gdf, check_type="intersect", return_col="NAME"
    )
    assert result == "A"


def test_lookup_fallback_to_intersect(sample_gdf):
    """
    Tests that when no check_type is specified, the function falls back to
    'intersect' mode and returns a match.
    """
    lat, lng = 0.0, 0.5  # Not within, but intersects
    result = lookup_geometry_by_point(
        lat, lng, sample_gdf, check_type=None, return_col="NAME"
    )
    assert result == "A"


def test_lookup_no_match(sample_gdf):
    """
    Tests that when a point does not fall within or intersect any polygons,
    the function returns None.
    """
    lat, lng = 10.0, 10.0
    result = lookup_geometry_by_point(
        lat, lng, sample_gdf, check_type="contain", return_col="NAME"
    )
    assert result is None


def test_invalid_lat_raises(sample_gdf):
    """
    Tests that providing an invalid latitude (outside -90 to 90) raises a
    ValueError.
    """
    with pytest.raises(ValueError, match="Invalid latitude"):
        lookup_geometry_by_point(100.0, 0.0, sample_gdf)


def test_invalid_lng_raises(sample_gdf):
    """
    Tests that providing an invalid longitude (outside -180 to 180) raises
    a ValueError.
    """
    with pytest.raises(ValueError, match="Invalid longitude"):
        lookup_geometry_by_point(0.0, 200.0, sample_gdf)


def test_missing_return_col_raises(sample_gdf):
    """Tests that requesting a non-existent return column raises a
    ValueError.
    """
    lat, lng = 0.5, 0.5
    with pytest.raises(ValueError, match="Column 'MISSING' not found"):
        lookup_geometry_by_point(lat, lng, sample_gdf, return_col="MISSING")


def test_missing_geometry_column_raises():
    """Tests that passing a GeoDataFrame with no geometry column raises a
    ValueError."""
    df = pd.DataFrame({"NAME": ["A", "B"]})  # No geometry column
    gdf = gpd.GeoDataFrame(df)
    with pytest.raises(
        ValueError, match="must contain at least one geometry column"
    ):
        lookup_geometry_by_point(0.5, 0.5, gdf)


def test_none_geodataframe_raises():
    """Tests that passing None instead of a GeoDataFrame raises an
    AttributeError."""
    with pytest.raises(AttributeError):
        lookup_geometry_by_point(0.5, 0.5, None)
