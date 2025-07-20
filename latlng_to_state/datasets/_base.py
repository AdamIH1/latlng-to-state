from importlib import resources
import geopandas as gpd 

DATA_MODULE = "latlng_to_state.datasets.data"


def load_parquet_file(
    data_file_name,
    data_module=DATA_MODULE):

    data_path = resources.files(data_module) / data_file_name
    data_df = gpd.read_parquet(data_path)

    return data_df


def load_us_geometry():
  
    data_file_name = "test_state.parquet"
    data = load_parquet_file(data_file_name=data_file_name) 

    return data