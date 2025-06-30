"""
Satellite data loading module for NASA HLS and Copernicus Sentinel-2 data.
Handles systematic loading and processing of multi-temporal satellite imagery.
"""

import os
import numpy as np
import rasterio
import logging
from typing import Dict, Tuple, List

logger = logging.getLogger(__name__)

def process_nasa_hls_collection_systematically(nasa_folders: List[str], nasa_hls_folder: str) -> Tuple[Dict, Dict, Dict]:
    """
    Load and process NASA HLS collection with systematic temporal coverage.
    
    Args:
        nasa_folders: List of NASA HLS folder names to process
        nasa_hls_folder: Base path to NASA HLS data
        
    Returns:
        Tuple containing nasa_scene_data, ndvi_temporal_series, enhanced_vegetation_indices
    """
    logger.info(f"Loading NASA HLS collection with {len(nasa_folders)} scenes")
    
    # Prioritize tiles by geographic coverage
    prioritized_nasa = []
    for tile in ['T20LKP', 'T20LKR', 'T20LLQ']:
        tile_scenes = [f for f in nasa_folders if tile.lower() in f.lower()]
        prioritized_nasa.extend(tile_scenes)
    
    nasa_scene_data = {}
    ndvi_temporal_series = {}
    enhanced_vegetation_indices = {}
    successful_scene_loads = 0
    
    for folder in prioritized_nasa:
        logger.info(f"Processing NASA HLS scene: {folder}")
        
        # Convert folder name to HLS identifier format
        hls_identifier = folder.replace('nasa-hls-', 'HLS.').replace('-', '.').upper()
        folder_lower = folder.lower()
        spectral_bands = {}
        
        # Load standard HLS bands
        band_list = ['B04', 'B08', 'B05', 'B06', 'B07', 'B8A', 'B11', 'B12']
        for band in band_list:
            file_name = f"{hls_identifier}.v2.0.{band}.tif"
            file_path = os.path.join(nasa_hls_folder, folder_lower, file_name)
            
            try:
                with rasterio.open(file_path) as src:
                    spectral_bands[band] = src.read(1)
                logger.debug(f"Loaded {band} - shape: {spectral_bands[band].shape}")
            except Exception as e:
                logger.warning(f"Failed to load {band} from {folder}: {e}")
                spectral_bands[band] = None
        
        # Calculate vegetation indices if required bands are available
        if spectral_bands.get('B04') is not None and spectral_bands.get('B08') is not None:
            nasa_scene_data[folder] = spectral_bands
            successful_scene_loads += 1
            
            # Calculate NDVI
            red_band = spectral_bands['B04'].astype(np.float32)
            nir_band = spectral_bands['B08'].astype(np.float32)
            ndvi_array = (nir_band - red_band) / (nir_band + red_band + 1e-10)
            
            temporal_identifier = folder.split('-')[-1][:7]
            ndvi_temporal_series[temporal_identifier] = ndvi_array
            
            # Calculate additional vegetation indices
            if spectral_bands.get('B05') is not None:
                red_edge_band = spectral_bands['B05'].astype(np.float32)
                ndre_array = (nir_band - red_edge_band) / (nir_band + red_edge_band + 1e-10)
                enhanced_vegetation_indices[f"{folder}_NDRE"] = ndre_array
            
            logger.debug(f"Vegetation indices calculated for {temporal_identifier}")
    
    logger.info(f"NASA HLS processing complete: {successful_scene_loads}/{len(nasa_folders)} scenes loaded")
    return nasa_scene_data, ndvi_temporal_series, enhanced_vegetation_indices

def process_copernicus_validation_collection_systematically(copernicus_folders: List[str], copernicus_folder: str) -> Tuple[Dict, Dict]:
    """
    Load and process Copernicus Sentinel-2 collection for high-resolution validation.
    
    Args:
        copernicus_folders: List of Copernicus folder names to process
        copernicus_folder: Base path to Copernicus data
        
    Returns:
        Tuple containing copernicus_scene_data, copernicus_ndvi_collection
    """
    logger.info("Loading Copernicus collection for high-resolution validation")
    
    # Prioritize tiles by geographic coverage
    prioritized_copernicus = []
    for tile in ['T20LKP', 'T20LKR', 'T20LLQ']:
        tile_scenes = [f for f in copernicus_folders if tile.lower() in f.lower()]
        prioritized_copernicus.extend(tile_scenes)
    
    copernicus_scene_data = {}
    copernicus_ndvi_collection = {}
    successful_copernicus_loads = 0
    
    for folder in prioritized_copernicus:
        logger.info(f"Processing Copernicus scene: {folder}")
        
        # Convert folder name to tile identifier
        tile_identifier = folder.replace('copernicus-', '').replace('-', '_').upper()
        folder_lower = folder.lower()
        spectral_bands = {}
        
        # Load Copernicus bands at different resolutions
        copernicus_bands = ['B04_10m', 'B08_10m', 'B05_20m', 'B06_20m', 'B07_20m', 'B8A_20m', 'B11_20m', 'B12_20m']
        for band in copernicus_bands:
            file_name = f"{tile_identifier}_{band}.jp2"
            file_path = os.path.join(copernicus_folder, folder_lower, file_name)
            
            try:
                with rasterio.open(file_path) as src:
                    spectral_bands[band] = src.read(1)
                logger.debug(f"Loaded {band}")
            except Exception as e:
                logger.warning(f"Failed to load {band} from {folder}: {e}")
                spectral_bands[band] = None
        
        # Calculate high-resolution NDVI
        if spectral_bands.get('B04_10m') is not None and spectral_bands.get('B08_10m') is not None:
            copernicus_scene_data[folder] = spectral_bands
            successful_copernicus_loads += 1
            
            red_10m = spectral_bands['B04_10m'].astype(np.float32)
            nir_10m = spectral_bands['B08_10m'].astype(np.float32)
            ndvi_10m = (nir_10m - red_10m) / (nir_10m + red_10m + 1e-10)
            copernicus_ndvi_collection[folder] = ndvi_10m
            logger.debug("High-resolution NDVI calculated")
    
    logger.info(f"Copernicus processing complete: {successful_copernicus_loads}/{len(copernicus_folders)} scenes loaded")
    return copernicus_scene_data, copernicus_ndvi_collection

def create_comprehensive_satellite_dataset(nasa_folders: List[str], copernicus_folders: List[str]) -> Dict:
    """
    Create comprehensive satellite dataset from NASA and Copernicus data.
    
    Args:
        nasa_folders: List of NASA folder names
        copernicus_folders: List of Copernicus folder names
        
    Returns:
        Dict containing comprehensive satellite data
    """
    from config.config import Config
    
    logger.info("Creating comprehensive multi-source satellite dataset...")
    
    nasa_scenes, ndvi_time_series, enhanced_indices = process_nasa_hls_collection_systematically(
        nasa_folders, Config.NASA_HLS_FOLDER)
    copernicus_scenes, copernicus_ndvi = process_copernicus_validation_collection_systematically(
        copernicus_folders, Config.COPERNICUS_FOLDER)
    
    # Temporal analysis statistics
    temporal_analysis_statistics = {}
    if len(ndvi_time_series) > 1:
        ndvi_stack = np.stack(list(ndvi_time_series.values()))
        temporal_analysis_statistics = {
            'temporal_mean': np.nanmean(ndvi_stack, axis=0),
            'temporal_std': np.nanstd(ndvi_stack, axis=0),
            'temporal_min': np.nanmin(ndvi_stack, axis=0),
            'temporal_max': np.nanmax(ndvi_stack, axis=0),
            'stability_index': 1.0 / (np.nanstd(ndvi_stack, axis=0) + 0.001)
        }
    
    comprehensive_satellite_data = {
        'nasa_scenes': nasa_scenes,
        'copernicus_scenes': copernicus_scenes,
        'temporal_coverage': sorted(ndvi_time_series.keys()),
        'ndvi_time_series': ndvi_time_series,
        'copernicus_ndvi': copernicus_ndvi,
        'enhanced_indices': enhanced_indices,
        'temporal_statistics': temporal_analysis_statistics
    }
    
    logger.info(f"Satellite integration success: {len(nasa_scenes)} NASA + {len(copernicus_scenes)} Copernicus scenes")
    logger.info(f"Temporal coverage: {len(ndvi_time_series)} NDVI time series")
    logger.info(f"Enhanced indices: {len(enhanced_indices)} calculated")
    
    return comprehensive_satellite_data
