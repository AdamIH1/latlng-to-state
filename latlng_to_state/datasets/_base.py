from importlib import resources
import geopandas as gpd

DATA_MODULE = "latlng_to_state.datasets.data"


def load_parquet_file(data_file_name, data_module=DATA_MODULE):
    """Loads a GeoParquet file as a GeoDataFrame.

    Args:
        data_file_name (str): Name of the Parquet file to load.
        data_module (str): Python module path where the file is stored.

    Returns:
        geopandas.GeoDataFrame: The loaded GeoDataFrame.
    """
    data_path = resources.files(data_module) / data_file_name
    data_df = gpd.read_parquet(data_path)
    return data_df


def load_us_state_geometry():
    """Loads US state boundary geometry as a GeoDataFrame.

    Returns:
        geopandas.GeoDataFrame: US state boundary geometry.
    """
    data_file_name = "us_state_boundary.parquet"
    data = load_parquet_file(data_file_name=data_file_name)
    return data


def load_us_zipcode_centroid():
    """Loads ZIP code centroid data as a GeoDataFrame.

    Returns:
        geopandas.GeoDataFrame: ZIP code centroid data.
    """
    data_file_name = "us_zipcode_centroid.parquet"
    data = load_parquet_file(data_file_name=data_file_name)
    return data
