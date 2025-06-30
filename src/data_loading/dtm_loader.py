"""
DTM (Digital Terrain Model) data loading module for FABDEM elevation data.
Handles loading and processing of forest-corrected elevation models.
"""

import os
import glob
import rasterio
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def load_fabdem_tiles() -> Dict:
    """
    Load FABDEM DTM tiles from the configured directory.
    
    Returns:
        Dict mapping tile names to rasterio dataset objects
    """
    from config.config import Config
    
    logger.info("Loading FABDEM DTM tiles...")
    
    fabdem_folder = Config.FABDEM_DTM_FOLDER
    if not os.path.exists(fabdem_folder):
        logger.error(f"FABDEM folder does not exist: {fabdem_folder}")
        return {}
    
    # Find all TIFF files in the FABDEM folder
    tif_files = glob.glob(os.path.join(fabdem_folder, '*.tif'))
    
    dtm_datasets = {}
    successful_loads = 0
    
    for tif_file in tif_files:
        tile_name = os.path.basename(tif_file)
        
        try:
            dtm_raster = rasterio.open(tif_file)
            dtm_datasets[tile_name] = dtm_raster
            successful_loads += 1
            logger.debug(f"Loaded DTM tile: {tile_name}")
        except Exception as e:
            logger.warning(f"Failed to load DTM tile {tile_name}: {e}")
    
    logger.info(f"Successfully loaded {successful_loads} FABDEM DTM tiles")
    return dtm_datasets
