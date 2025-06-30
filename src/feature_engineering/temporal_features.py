"""
Temporal feature engineering module.
Computes temporal vegetation patterns for archaeological detection.
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

def perform_advanced_temporal_analysis(ndvi_time_series):
    """
    Perform advanced temporal analysis on NDVI time series.
    
    Args:
        ndvi_time_series: Dictionary of NDVI arrays by time period
        
    Returns:
        Dict containing temporal features
    """
    logger.info("Performing advanced temporal analysis...")
    
    if not ndvi_time_series or len(ndvi_time_series) < 2:
        logger.warning("Insufficient temporal data for analysis")
        # Return dummy features with zeros
        dummy_shape = (100, 100)  # Default shape
        return {
            'temporal_mean': np.zeros(dummy_shape),
            'temporal_std': np.zeros(dummy_shape),
            'temporal_min': np.zeros(dummy_shape),
            'temporal_max': np.zeros(dummy_shape),
            'stability_index': np.ones(dummy_shape),
            'trend_slope': np.zeros(dummy_shape)
        }
    
    # Stack NDVI arrays
    ndvi_stack = np.stack(list(ndvi_time_series.values()))
    
    # Calculate temporal statistics
    temporal_features = {
        'temporal_mean': np.nanmean(ndvi_stack, axis=0),
        'temporal_std': np.nanstd(ndvi_stack, axis=0),
        'temporal_min': np.nanmin(ndvi_stack, axis=0),
        'temporal_max': np.nanmax(ndvi_stack, axis=0),
        'stability_index': 1.0 / (np.nanstd(ndvi_stack, axis=0) + 0.001),
        'trend_slope': calculate_temporal_trend(ndvi_stack)
    }
    
    logger.info(f"Generated {len(temporal_features)} temporal features")
    return temporal_features

def calculate_temporal_trend(ndvi_stack):
    """Calculate temporal trend using linear regression."""
    n_times, height, width = ndvi_stack.shape
    time_points = np.arange(n_times)
    
    # Initialize trend array
    trend_slope = np.zeros((height, width))
    
    # Calculate trend for each pixel
    for i in range(height):
        for j in range(width):
            pixel_series = ndvi_stack[:, i, j]
            if not np.isnan(pixel_series).all():
                # Simple linear trend calculation
                valid_mask = ~np.isnan(pixel_series)
                if np.sum(valid_mask) > 1:
                    x = time_points[valid_mask]
                    y = pixel_series[valid_mask]
                    trend_slope[i, j] = np.polyfit(x, y, 1)[0]
    
    return trend_slope
