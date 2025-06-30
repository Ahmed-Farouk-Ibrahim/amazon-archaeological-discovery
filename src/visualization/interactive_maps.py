"""
Interactive map creation for archaeological discoveries.
"""

import folium
from folium.plugins import HeatMap, Fullscreen, MeasureControl
import geopandas as gpd
from shapely.geometry import Point
import logging
from pyproj import Transformer

logger = logging.getLogger(__name__)

def create_ultimate_interactive_map(pred_gdf, hotspots_gdf, known_sites_gdf, dtm_raster, save_path):
    """Create an interactive map showing archaeological hotspots and known sites."""
    logger.info("Creating ultimate interactive map...")
    
    # Convert to lat/lon for Folium
    sites_latlon = known_sites_gdf.to_crs("EPSG:4326") if not known_sites_gdf.empty else gpd.GeoDataFrame()
    
    # Robust map center calculation
    try:
        if dtm_raster is not None:
            transformer = Transformer.from_crs(dtm_raster.crs, "EPSG:4326", always_xy=True)
            min_lon, min_lat = transformer.transform(dtm_raster.bounds.left, dtm_raster.bounds.bottom)
            max_lon, max_lat = transformer.transform(dtm_raster.bounds.right, dtm_raster.bounds.top)
            map_center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
        else:
            map_center = [-10.0, -67.0]  # Default Amazon center
    except Exception as e:
        logger.warning(f"Map center calculation failed: {e}")
        map_center = [-10.0, -67.0]  # Default Amazon center

    # Create base map
    m = folium.Map(location=map_center, zoom_start=12)
    
    # Add satellite imagery with error handling
    try:
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google Satellite',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)
    except Exception as e:
        logger.warning(f"Satellite layer failed: {e}")

    # Add probability heatmap
    if pred_gdf is not None and not pred_gdf.empty:
        try:
            heat_data = [[row.geometry.y, row.geometry.x, row.probability] 
                         for _, row in pred_gdf.to_crs("EPSG:4326").iterrows()]
            HeatMap(heat_data, name='Archaeological Probability', radius=15, blur=10).add_to(m)
        except Exception as e:
            logger.warning(f"Heatmap creation failed: {e}")

    # Add known sites
    if not sites_latlon.empty:
        try:
            known_sites_layer = folium.FeatureGroup(name='Known Geoglyphs', show=False).add_to(m)
            for _, row in sites_latlon.iterrows():
                folium.CircleMarker(
                    [row.geometry.y, row.geometry.x], 
                    radius=4, 
                    color='cyan', 
                    fill=True,
                    popup='Known Geoglyph Site'
                ).add_to(known_sites_layer)
        except Exception as e:
            logger.warning(f"Known sites layer failed: {e}")

    # Add candidate hotspots
    if hotspots_gdf is not None and not hotspots_gdf.empty:
        try:
            hotspots_latlon = hotspots_gdf.to_crs("EPSG:4326")
            hotspots_layer = folium.FeatureGroup(name='New Discoveries').add_to(m)
            
            for idx, row in hotspots_latlon.iterrows():
                popup_html = f"""
                <div style="width: 300px;">
                    <h4>Discovery #{idx+1}</h4>
                    <p><b>Coordinates:</b> {row.geometry.y:.6f}, {row.geometry.x:.6f}</p>
                    <p><b>Confidence:</b> {row.mean_prob:.2%}</p>
                </div>
                """
                
                color = 'red' if row.mean_prob > 0.7 else 'orange' if row.mean_prob > 0.5 else 'yellow'
                
                folium.Marker(
                    [row.geometry.y, row.geometry.x], 
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color=color, icon='star')
                ).add_to(hotspots_layer)
        except Exception as e:
            logger.warning(f"Hotspots layer failed: {e}")

    # Add controls
    try:
        folium.LayerControl().add_to(m)
        Fullscreen().add_to(m)
        MeasureControl().add_to(m)
    except Exception as e:
        logger.warning(f"Map controls failed: {e}")

    # Save map
    try:
        m.save(save_path)
        logger.info(f"Map saved: {save_path}")
    except Exception as e:
        logger.error(f"Map save failed: {e}")
    
    return m
