import geopandas as gpd
import pandas as pd 
from shapely.geometry import Point
from typing import Optional

def _point_within_geometry(
    lat: float, lng: float, gdf: gpd.GeoDataFrame
) -> Optional[pd.Series]:
    """Returns the first row where the point is strictly within a geometry.

    Args:
        lat: Latitude of the point.
        lng: Longitude of the point.
        gdf: GeoDataFrame containing polygon geometries.

    Returns:
        The first matching row as a Series, or None if no match is found.
    """
    point = Point(lng, lat)
    result = gdf[gdf.contains(point)]
    if not result.empty:
        return result.iloc[0]
    return None


def _point_intersects_geometry(
    lat: float, lng: float, gdf: gpd.GeoDataFrame
) -> Optional[pd.Series]:
    """Returns the first row where the point intersects a geometry.

    Args:
        lat: Latitude of the point.
        lng: Longitude of the point.
        gdf: GeoDataFrame containing polygon geometries.

    Returns:
        The first matching row as a Series, or None if no match is found.
    """
    point = Point(lng, lat)
    result = gdf[gdf.intersects(point)]
    if not result.empty:
        return result.iloc[0]
    return None
