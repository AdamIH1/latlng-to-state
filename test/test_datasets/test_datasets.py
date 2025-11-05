import pytest
import geopandas as gpd
from latlng_to_state.datasets import (
    load_us_state_geometry,
    load_us_zipcode_centroid,
)
from latlng_to_state.datasets._base import load_parquet_file


def test_load_us_state_geometry_returns_geodataframe():
    """Tests that load_us_state_geometry returns a GeoDataFrame
    containing a geometry column."""
    gdf = load_us_state_geometry()
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert "geometry" in gdf.columns


def test_load_parquet_file_direct_returns_geodataframe():
    """Tests that load_parquet_file loads a valid GeoDataFrame when a
    correct parquet filename is given."""
    gdf = load_parquet_file("us_state_boundary.parquet")
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert not gdf.empty


def test_load_parquet_file_has_expected_columns():
    """Tests that the loaded state boundary GeoDataFrame includes the
    expected 'geometry' and 'state' columns."""
    gdf = load_parquet_file("us_state_boundary.parquet")
    expected_cols = {"geometry", "state"}
    assert expected_cols.issubset(set(gdf.columns))


def test_load_parquet_file_missing_file_raises():
    """Tests that loading a parquet file that does not exist raises a
    FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_parquet_file("nonexistent.parquet")


def test_load_parquet_file_invalid_module_raises():
    """Tests that loading from an invalid data module raises a
    ModuleNotFoundError."""
    with pytest.raises(ModuleNotFoundError):
        load_parquet_file(
            "us_state_boundary.parquet",
            data_module="invalid.module.name",
        )


def test_load_us_zipcode_centroid_returns_geodataframe():
    """Tests that load_us_zipcode_centroid returns a GeoDataFrame
    containing a geometry column."""
    gdf = load_us_zipcode_centroid()
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert "geometry" in gdf.columns


def test_load_zipcode_centroid_returns_geodataframe():
    """Tests that loading the zipcode centroid parquet file returns a
    non-empty GeoDataFrame with a geometry column."""
    gdf = load_parquet_file("us_zipcode_centroid.parquet")
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert not gdf.empty
    assert "geometry" in gdf.columns


def test_load_zipcode_centroids_has_expected_columns():
    """Tests that the loaded zipcode centroid GeoDataFrame includes the
    expected 'geometry' and 'zipcode' columns."""
    gdf = load_parquet_file("us_zipcode_centroid.parquet")
    expected_cols = {"geometry", "zipcode"}
    assert expected_cols.issubset(set(gdf.columns))


def test_load_zipcode_centroids_missing_file_raises():
    """Tests that attempting to load a missing zipcode centroid parquet
    file raises a FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_parquet_file("nonexistent_zipcode_file.parquet")
