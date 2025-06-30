"""
Spectral feature engineering module.
Computes spectral indices for archaeological detection.
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

def compute_advanced_spectral_indices(spectral_bands):
    """Advanced spectral indices for archaeological detection"""
    indices = {}
    
    def safe_extract(band_key):
        if band_key in spectral_bands and spectral_bands[band_key] is not None:
            return spectral_bands[band_key].astype(np.float32)
        return None
    
    red = safe_extract('B04')
    green = safe_extract('B03')
    blue = safe_extract('B02') 
    red_edge1 = safe_extract('B05')
    nir = safe_extract('B08')
    swir1 = safe_extract('B11')
    swir2 = safe_extract('B12')
    
    # Only calculate indices if required bands exist
    if red is not None and nir is not None:
        indices['NDVI'] = (nir - red) / (nir + red + 1e-10)
        indices['EVI2'] = 2.5 * (nir - red) / (nir + 2.4 * red + 1.0)
        L = 0.5
        indices['SAVI'] = ((nir - red) / (nir + red + L)) * (1 + L)
    
    if red_edge1 is not None and nir is not None:
        indices['NDRE1'] = (nir - red_edge1) / (nir + red_edge1 + 1e-10)
    
    # Check all required bands before calculation
    if red is not None and nir is not None and swir1 is not None and blue is not None:
        indices['BSI'] = ((swir1 + red) - (nir + blue)) / ((swir1 + red) + (nir + blue) + 1e-10)
    
    if swir1 is not None and nir is not None:
        indices['SCI'] = (swir1 - nir) / (swir1 + nir + 1e-10)
    
    # Only calculate if all required bands exist
    if red is not None and swir1 is not None and nir is not None:
        indices['AAI'] = (swir1 - red) / (nir + 1e-10)
        # Only calculate EDI if BSI was successfully calculated
        if 'BSI' in indices and 'NDVI' in indices:
            indices['EDI'] = (indices['BSI'] - indices['NDVI']) / 2.0
    
    logger.info(f"Computed {len(indices)} spectral indices")
    return indices

def extract_features_at_points(points_gdf, feature_rasters, dtm_raster, rivers_gdf):
    """
    Extract feature values at specific point locations.
    
    Args:
        points_gdf: GeoDataFrame containing point locations
        feature_rasters: Dictionary of feature arrays
        dtm_raster: DTM rasterio dataset for coordinate transformation
        rivers_gdf: Rivers GeoDataFrame for distance calculation
        
    Returns:
        DataFrame with extracted feature values
    """
    import pandas as pd
    
    logger.info(f"Extracting features at {len(points_gdf)} points")
    
    feature_data = []
    
    for idx, point in points_gdf.iterrows():
        try:
            # Convert point to pixel coordinates
            row, col = dtm_raster.index(point.geometry.x, point.geometry.y)
            
            # Extract features
            point_features = {}
            for feature_name, feature_array in feature_rasters.items():
                if 0 <= row < feature_array.shape[0] and 0 <= col < feature_array.shape[1]:
                    point_features[feature_name] = feature_array[row, col]
                else:
                    point_features[feature_name] = 0.0
            
            # Calculate distance to nearest river
            if not rivers_gdf.empty:
                try:
                    distances = rivers_gdf.distance(point.geometry)
                    point_features['distance_to_river'] = distances.min()
                except:
                    point_features['distance_to_river'] = 1000.0  # Default distance
            else:
                point_features['distance_to_river'] = 1000.0
            
            feature_data.append(point_features)
            
        except Exception as e:
            logger.warning(f"Failed to extract features for point {idx}: {e}")
            # Add default values
            default_features = {name: 0.0 for name in feature_rasters.keys()}
            default_features['distance_to_river'] = 1000.0
            feature_data.append(default_features)
    
    return pd.DataFrame(feature_data)
