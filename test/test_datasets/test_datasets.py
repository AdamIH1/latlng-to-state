import pytest
import geopandas as gpd
from latlng_to_state.datasets import load_us_geometry
from latlng_to_state.datasets._base import load_parquet_file

def test_load_us_geometry_returns_geodataframe():
    gdf = load_us_geometry()
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert "geometry" in gdf.columns

def test_load_parquet_file_direct_returns_geodataframe():
    gdf = load_parquet_file("test_state.parquet")
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert not gdf.empty

def test_load_parquet_file_has_expected_columns():
    gdf = load_parquet_file("test_state.parquet")
    expected_cols = {"geometry", "NAME"}  # Adjust based on actual columns
    assert expected_cols.issubset(set(gdf.columns))

def test_load_parquet_file_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_parquet_file("nonexistent.parquet")

def test_load_parquet_file_invalid_module_raises():
    with pytest.raises(ModuleNotFoundError):
        load_parquet_file("test_state.parquet"
            , data_module="invalid.module.name")
