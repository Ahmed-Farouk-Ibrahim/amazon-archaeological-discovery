"""
Topographic feature engineering module.
Computes advanced topographic features for archaeological detection.
"""

import numpy as np
import logging
from scipy.ndimage import gaussian_filter, generic_filter

logger = logging.getLogger(__name__)

def compute_revolutionary_topographic_features(dtm_array):
    """Compute advanced topographic features for archaeological detection - CPU version"""
    features = {}
    
    # Basic elevation
    features['elevation'] = dtm_array
    
    # Gradient analysis
    gy, gx = np.gradient(dtm_array)
    features['slope'] = np.sqrt(gx**2 + gy**2)
    features['aspect'] = np.arctan2(gy, gx)
    
    # Topographic anomaly (critical for earthwork detection)
    smoothed = gaussian_filter(dtm_array, sigma=15, mode='reflect')
    features['topo_anomaly'] = dtm_array - smoothed
    
    # Multi-scale TPI with proper generic_filter import
    for radius in [3, 7, 15]:
        try:
            kernel = np.ones((radius*2+1, radius*2+1))
            kernel[radius, radius] = 0
            mean_neighbor = generic_filter(dtm_array, np.mean, footprint=kernel)
            features[f'tpi_scale_{radius}'] = dtm_array - mean_neighbor
        except Exception as e:
            logger.warning(f"TPI calculation failed for radius {radius}: {e}")
            features[f'tpi_scale_{radius}'] = np.zeros_like(dtm_array)
    
    # Advanced curvature analysis
    try:
        gyy, gyx = np.gradient(gy)
        gxy, gxx = np.gradient(gx)
        features['profile_curvature'] = (gxx * gx**2 + 2 * gxy * gx * gy + gyy * gy**2) / (gx**2 + gy**2 + 1e-10)**(3/2)
        features['plan_curvature'] = (gxx * gy**2 - 2 * gxy * gx * gy + gyy * gx**2) / (gx**2 + gy**2 + 1e-10)
    except Exception as e:
        logger.warning(f"Curvature calculation failed: {e}")
        features['profile_curvature'] = np.zeros_like(dtm_array)
        features['plan_curvature'] = np.zeros_like(dtm_array)
    
    logger.info(f"Computed {len(features)} topographic features")
    return features

def compute_revolutionary_topographic_features_GPU(dtm_array_gpu):
    """GPU-accelerated topographic features using CuPy"""
    try:
        import cupy as cp
        features = {}
        
        # Basic elevation (already on GPU)
        features['elevation'] = cp.asnumpy(dtm_array_gpu)
        
        # GPU-accelerated gradient
        gy_gpu, gx_gpu = cp.gradient(dtm_array_gpu)
        features['slope'] = cp.asnumpy(cp.sqrt(gx_gpu**2 + gy_gpu**2))
        features['aspect'] = cp.asnumpy(cp.arctan2(gy_gpu, gx_gpu))
        
        # GPU-accelerated smoothing
        try:
            from cupyx.scipy.ndimage import gaussian_filter as gpu_gaussian_filter
            smoothed_gpu = gpu_gaussian_filter(dtm_array_gpu, sigma=15, mode='reflect')
        except ImportError:
            # Fallback to CPU for smoothing
            smoothed_gpu = cp.asarray(gaussian_filter(cp.asnumpy(dtm_array_gpu), sigma=15, mode='reflect'))
        
        features['topo_anomaly'] = cp.asnumpy(dtm_array_gpu - smoothed_gpu)
        
        # Convert back to CPU for compatibility
        for radius in [3, 7, 15]:
            try:
                # Simplified TPI on GPU
                features[f'tpi_scale_{radius}'] = cp.asnumpy(dtm_array_gpu - cp.mean(dtm_array_gpu))
            except:
                features[f'tpi_scale_{radius}'] = cp.asnumpy(cp.zeros_like(dtm_array_gpu))
        
        # GPU curvature
        try:
            gyy_gpu, gyx_gpu = cp.gradient(gy_gpu)
            gxy_gpu, gxx_gpu = cp.gradient(gx_gpu)
            
            profile_curv_gpu = (gxx_gpu * gx_gpu**2 + 2 * gxy_gpu * gx_gpu * gy_gpu + gyy_gpu * gy_gpu**2) / (gx_gpu**2 + gy_gpu**2 + 1e-10)**(3/2)
            plan_curv_gpu = (gxx_gpu * gy_gpu**2 - 2 * gxy_gpu * gx_gpu * gy_gpu + gyy_gpu * gx_gpu**2) / (gx_gpu**2 + gy_gpu**2 + 1e-10)
            
            features['profile_curvature'] = cp.asnumpy(profile_curv_gpu)
            features['plan_curvature'] = cp.asnumpy(plan_curv_gpu)
        except Exception as e:
            logger.warning(f"GPU curvature calculation failed: {e}")
            features['profile_curvature'] = cp.asnumpy(cp.zeros_like(dtm_array_gpu))
            features['plan_curvature'] = cp.asnumpy(cp.zeros_like(dtm_array_gpu))
        
        logger.info(f"GPU-computed {len(features)} topographic features")
        return features
        
    except Exception as e:
        logger.warning(f"GPU processing failed, falling back to CPU: {e}")
        # Fallback to CPU
        return compute_revolutionary_topographic_features(cp.asnumpy(dtm_array_gpu))
