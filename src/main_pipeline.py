"""
Main execution pipeline for Amazon archaeological discovery system.
Submitted for OpenAI to Z Challenge competition.

This module orchestrates the complete archaeological discovery workflow
from data loading through final site identification and analysis.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime
from shapely.geometry import Point, box
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.utils import resample
import psutil
import json
import re

# Add source directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
from config.config import Config
from data_loading.satellite_loader import create_comprehensive_satellite_dataset
from data_loading.dtm_loader import load_fabdem_tiles
from data_loading.geoglyph_loader import load_core_data
from feature_engineering.topographic_features import compute_revolutionary_topographic_features, compute_revolutionary_topographic_features_GPU
from feature_engineering.temporal_features import perform_advanced_temporal_analysis
from feature_engineering.spectral_features import compute_advanced_spectral_indices, extract_features_at_points
from models.archaeological_ensemble import UltimateArchaeologicalEnsemble
from visualization.interactive_maps import create_ultimate_interactive_map
from visualization.ai_analysis import generate_ai_archaeological_analysis
from utils.memory_management import cleanup_memory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_bounds_from_filename_CORRECT(filename):
    """Parse bounds from FABDEM filename format: S01W061_FABDEM_V1-2.tif"""
    match = re.match(r'S(\d+)W(\d+)_FABDEM_V1-2\.tif', filename)
    if not match:
        return None
    
    south_lat = -int(match.group(1))  # S01 = -1°
    west_lon = -int(match.group(2))   # W061 = -61°
    
    # Each tile covers 1 degree
    minx = west_lon      # Western edge
    maxx = west_lon + 1  # Eastern edge
    miny = south_lat     # Southern edge
    maxy = south_lat + 1 # Northern edge
    
    return [minx, miny, maxx, maxy]

def check_overlap_CORRECT(tile_bounds, geoglyph_bounds):
    """Check if two bounding boxes overlap"""
    if tile_bounds is None:
        return False
    
    # No overlap if:
    no_overlap = (tile_bounds[0] > geoglyph_bounds[2] or  # tile minx > geoglyph maxx
                  tile_bounds[2] < geoglyph_bounds[0] or  # tile maxx < geoglyph minx
                  tile_bounds[1] > geoglyph_bounds[3] or  # tile miny > geoglyph maxy
                  tile_bounds[3] < geoglyph_bounds[1])    # tile maxy < geoglyph miny
    
    return not no_overlap

def find_overlapping_dtm_tiles_FIXED(dtm_datasets, geoglyphs_gdf):
    """FIXED version for your S01W061_FABDEM_V1-2.tif format"""
    logger.info("Finding Overlapping DTM Tiles (FIXED for your format)")
    geoglyph_bounds = geoglyphs_gdf.total_bounds
    logger.info(f"Geoglyph bounds: {geoglyph_bounds}")
    
    overlapping_dtm_tiles = {}
    
    for dtm_name, dtm_raster in dtm_datasets.items():
        # FIXED: Parse bounds from your actual filename format
        tile_bounds = parse_bounds_from_filename_CORRECT(dtm_name)
        
        if tile_bounds and check_overlap_CORRECT(tile_bounds, geoglyph_bounds):
            # Double-check with actual spatial join
            dtm_poly = box(*tile_bounds)
            dtm_gdf = gpd.GeoDataFrame([1], geometry=[dtm_poly], crs='EPSG:4326')
            sites_in_tile = gpd.sjoin(geoglyphs_gdf.to_crs('EPSG:4326'), dtm_gdf, how="inner", predicate='intersects')
            
            if not sites_in_tile.empty:
                overlapping_dtm_tiles[dtm_name] = {
                    'raster': dtm_raster,
                    'sites': sites_in_tile,
                    'bounds': tile_bounds
                }
                logger.info(f"Found {dtm_name}: {len(sites_in_tile)} sites - Bounds: {tile_bounds}")
    
    logger.info(f"Found {len(overlapping_dtm_tiles)} overlapping DTM tiles")
    return overlapping_dtm_tiles

def sort_tiles_by_priority(overlapping_dtm_tiles):
    """Sort DTM tiles by number of overlapping sites with enhanced coverage strategy"""
    logger.info("Sorting tiles by archaeological site density...")
    
    # Create list of (tile_name, site_count, tile_info)
    tiles_with_counts = []
    for tile_name, tile_info in overlapping_dtm_tiles.items():
        site_count = len(tile_info['sites'])
        tiles_with_counts.append((tile_name, site_count, tile_info))
    
    # Sort by site count (descending - most sites first)
    sorted_tiles = sorted(tiles_with_counts, key=lambda x: x[1], reverse=True)
    
    # Calculate cumulative coverage and find optimal strategies
    total_sites = sum([count for _, count, _ in sorted_tiles])
    cumulative_sites = 0
    optimal_count_80 = 0
    optimal_count_90 = 0
    optimal_count_95 = 0
    tiles_with_10plus = 0
    
    logger.info(f"Total sites across all tiles: {total_sites}")
    logger.info(f"Top tiles by site density:")
    
    for i, (tile_name, site_count, _) in enumerate(sorted_tiles):
        cumulative_sites += site_count
        coverage = cumulative_sites / total_sites
        
        # Track coverage milestones
        if coverage >= 0.8 and optimal_count_80 == 0:
            optimal_count_80 = i + 1
        if coverage >= 0.9 and optimal_count_90 == 0:
            optimal_count_90 = i + 1
        if coverage >= 0.95 and optimal_count_95 == 0:
            optimal_count_95 = i + 1
        
        # Track tiles with significant sites (10+)
        if site_count >= 10:
            tiles_with_10plus = i + 1
        
        # Print top 15 tiles
        if i < 15:
            logger.info(f"   #{i+1}: {tile_name} - {site_count} sites ({coverage*100:.1f}% cumulative)")
    
    # Enhanced strategy: Choose the best approach
    logger.info(f"Coverage Analysis:")
    logger.info(f"   80% coverage: {optimal_count_80} tiles")
    logger.info(f"   90% coverage: {optimal_count_90} tiles")
    logger.info(f"   95% coverage: {optimal_count_95} tiles")
    logger.info(f"   Tiles with 10+ sites: {tiles_with_10plus} tiles")
    
    # Strategy: Use 90% coverage OR all tiles with 10+ sites, whichever is MORE
    optimal_count = max(optimal_count_90, tiles_with_10plus)
    
    final_coverage = sum([count for _, count, _ in sorted_tiles[:optimal_count]]) / total_sites
    
    logger.info(f"Selected strategy: {optimal_count} tiles")
    logger.info(f"   Final coverage: {final_coverage*100:.1f}% of all sites")
    logger.info(f"   Rationale: {'90% coverage achieved' if optimal_count == optimal_count_90 else 'Including all high-value tiles (10+ sites)'}")
    
    # Return sorted dictionary
    sorted_dict = {tile_name: tile_info for tile_name, _, tile_info in sorted_tiles}
    return sorted_dict, optimal_count

def generate_realistic_negatives(sites_in_tile, dtm_raster):
    """Generate challenging negative samples near positive sites"""
    
    # Calculate number of negatives needed
    n_negative = min(len(sites_in_tile) * 2, 100)
    
    negative_points = []
    bounds = dtm_raster.bounds
    
    # 70% of negatives: Near positive sites (within 1-5km) - HARDER NEGATIVES
    near_negatives_needed = int(n_negative * 0.7)
    sites_to_sample = min(len(sites_in_tile), near_negatives_needed)
    
    if sites_to_sample > 0:
        sampled_sites = sites_in_tile.sample(sites_to_sample) if len(sites_in_tile) > sites_to_sample else sites_in_tile
        
        for _, site in sampled_sites.iterrows():
            for _ in range(max(1, near_negatives_needed // sites_to_sample)):
                # Sample within 1-5km of positive site
                offset_x = np.random.uniform(-0.05, 0.05)  # ~5km
                offset_y = np.random.uniform(-0.05, 0.05)
                
                neg_x = site.geometry.x + offset_x
                neg_y = site.geometry.y + offset_y
                
                # Ensure within bounds
                if (bounds.left <= neg_x <= bounds.right and 
                    bounds.bottom <= neg_y <= bounds.top):
                    negative_points.append(Point(neg_x, neg_y))
                
                if len(negative_points) >= near_negatives_needed:
                    break
            if len(negative_points) >= near_negatives_needed:
                break
    
    # 30% of negatives: Random locations - EASIER NEGATIVES
    random_negatives_needed = n_negative - len(negative_points)
    for _ in range(random_negatives_needed):
        x = np.random.uniform(bounds.left, bounds.right)
        y = np.random.uniform(bounds.bottom, bounds.top)
        negative_points.append(Point(x, y))
    
    logger.info(f"   Generated {len(negative_points)} negative samples ({int(n_negative * 0.7)} near sites, {random_negatives_needed} random)")
    return negative_points

def save_model_and_checkpoints(model, model_path, checkpoint_data, checkpoint_path):
    """Save model and checkpoint data"""
    import joblib
    
    # Save model
    joblib.dump(model, model_path)
    
    # Save checkpoint data
    with open(checkpoint_path, 'w') as f:
        json.dump(checkpoint_data, f, indent=2)
    
    logger.info(f"Model saved to {model_path}")
    logger.info(f"Checkpoint saved to {checkpoint_path}")

def main_ultimate_pipeline():
    """Execute the complete archaeological discovery pipeline - FIXED VERSION"""
    logger.info("ULTIMATE ARCHAEOLOGICAL DISCOVERY SYSTEM")
    logger.info("=" * 60)
    
    # Create output directories
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dirs = {
        'models': f'/workspace/models_{timestamp}',
        'results': f'/workspace/results_{timestamp}',
        'maps': f'/workspace/maps_{timestamp}'
    }
    
    for dir_path in output_dirs.values():
        os.
