"""
Geoglyph and archaeological site data loading module.
Handles loading of known archaeological sites from KML files.
"""

import os
import geopandas as gpd
import logging
from pykml import parser
from shapely.geometry import Point

logger = logging.getLogger(__name__)

def load_archaeological_sites():
    """
    Load archaeological sites from KML file.
    
    Returns:
        GeoDataFrame containing archaeological site locations
    """
    from config.config import Config
    
    logger.info("Loading archaeological sites from KML...")
    
    kml_path = Config.GEOGLYPH_KML_PATH
    if not os.path.exists(kml_path):
        logger.error(f"KML file does not exist: {kml_path}")
        return gpd.GeoDataFrame()
    
    try:
        # Parse KML file
        with open(kml_path, 'r') as f:
            root = parser.parse(f).getroot()
        
        # Extract coordinates from placemarks
        coordinates = []
        for placemark in root.Document.Placemark:
            if hasattr(placemark, 'Point'):
                coord_str = str(placemark.Point.coordinates)
                lon, lat, _ = map(float, coord_str.strip().split(','))
                coordinates.append(Point(lon, lat))
        
        # Create GeoDataFrame
        geoglyphs_gdf = gpd.GeoDataFrame(
            {'id': range(len(coordinates))},
            geometry=coordinates,
            crs='EPSG:4326'
        )
        
        logger.info(f"Successfully parsed {len(geoglyphs_gdf)} geoglyph sites")
        return geoglyphs_gdf
        
    except Exception as e:
        logger.error(f"Failed to load archaeological sites: {e}")
        return gpd.GeoDataFrame()

def load_core_data():
    """
    Load all core archaeological and environmental data.
    
    Returns:
        Tuple containing (dtm_datasets, geoglyphs_gdf, hydro_gdf, prodes_gdf)
    """
    from config.config import Config
    
    logger.info("Loading all archaeological datasets...")
    
    # Load DTM data
    dtm_datasets = load_fabdem_tiles()
    
    # Load archaeological sites
    geoglyphs_gdf = load_archaeological_sites()
    
    # Load hydrography data
    try:
        hydro_gdf = gpd.read_file(Config.HYDROGRAPHY_SHP_PATH)
        logger.info(f"Successfully loaded hydrography data with {len(hydro_gdf)} segments")
    except Exception as e:
        logger.warning(f"Failed to load hydrography data: {e}")
        hydro_gdf = gpd.GeoDataFrame()
    
    # Load PRODES deforestation data
    try:
        prodes_gdf = gpd.read_file(Config.PRODES_GPKG_PATH, layer='accumulated_deforestation_2007')
        logger.info(f"Successfully loaded PRODES data with {len(prodes_gdf)} polygons")
    except Exception as e:
        logger.warning(f"Failed to load PRODES data: {e}")
        prodes_gdf = gpd.GeoDataFrame()
    
    return dtm_datasets, geoglyphs_gdf, hydro_gdf, prodes_gdf
