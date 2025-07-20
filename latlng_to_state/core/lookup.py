
import geopandas as gpd
from typing import Optional, Union
from latlng_to_state.utils.utils_core import (
    _point_within_geometry
    , _point_intersects_geometry
)


def lookup_geometry_by_point(
    lat: float,
    lng: float,
    gdf: Optional[gpd.GeoDataFrame],
    check_type: Optional[str] = None,
    return_col: str = "NAME",
) -> Optional[Union[str, int, float]]:
    """Looks up a value from a GeoDataFrame based on a lat/lng point.

    Args:
        lat: Latitude of the point.
        lng: Longitude of the point.
        check_type: 'contain' or 'intersect'. If None, try 'contain' then
            'intersect'.
        gdf: GeoDataFrame to use for lookup. Must be provided.
        return_col: Column name to return from the matched row.

    Returns:
        The value from the specified column in the matching row, or None if no
            match.

    Raises:
        ValueError: If `gdf` is not provided or `return_col` is missing in the
            match.
        ValueError: If lat or lng are outside valid ranges.
    """
    geometry_cols = gdf.select_dtypes(include=["geometry"]).columns
    if not geometry_cols:
        raise ValueError(
            "GeoDataFrame must contain at least one geometry column."
        )

    if abs(lat) > 90:
        raise ValueError(
            f"Invalid latitude {lat}. Must be between -90 and 90."
        )
    if abs(lng) > 180:
        raise ValueError(
            f"Invalid longitude {lng}. Must be between -180 and 180."
        )

    if check_type == "contain":
        match = _point_within_geometry(lat, lng, gdf)
    elif check_type == "intersect":
        match = _point_intersects_geometry(lat, lng, gdf)
    else:
        match = _point_within_geometry(lat, lng, gdf)
        if match is None:
            match = _point_intersects_geometry(lat, lng, gdf)

    if match is not None:
        if return_col in match:
            return match[return_col]
        else:
            raise ValueError(
                f"Column '{return_col}' not found in matched geometry row."
                )


    return None
