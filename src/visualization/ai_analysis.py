"""
AI-powered archaeological analysis using OpenAI.
"""

import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

def generate_ai_archaeological_analysis(hotspots_gdf, model_performance):
    """
    Generate AI-powered archaeological interpretation using OpenAI.
    
    Args:
        hotspots_gdf: GeoDataFrame containing discovered hotspots
        model_performance: Model AUC score for analysis
        
    Returns:
        str: AI-generated archaeological analysis
    """
    if hotspots_gdf.empty:
        return "No hotspots identified for analysis"
    
    # Initialize OpenAI client
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OpenAI API key not found in environment variables")
            return "OpenAI API key not configured. Please check your .env file."
        
        client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        return f"OpenAI client initialization failed: {e}"
    
    # Get top hotspot for analysis
    top_hotspot = hotspots_gdf.iloc[0]
    
    # Create detailed archaeological prompt
    prompt = f"""
You are Dr. Maria Santos, a world-renowned archaeologist specializing in pre-Columbian Amazonian civilizations with 25 years of field experience.

An advanced AI system has identified a high-probability archaeological site using multi-sensor remote sensing analysis:

**DISCOVERY DETAILS:**
- Location: {top_hotspot.geometry.y:.6f}°N, {top_hotspot.geometry.x:.6f}°W
- AI Confidence: {top_hotspot.mean_prob:.1%}
- Model Performance: ROC AUC {model_performance:.3f}
- Analysis Method: FABDEM DTM + NASA HLS temporal analysis + Copernicus validation

**DATA FUSION EVIDENCE:**
- Topographic anomaly detected in bare-earth elevation model
- Temporal vegetation stability suggests altered soil composition
- Multi-spectral indices indicate subsurface archaeological features
- Location validated against known settlement patterns

**EXPERT INTERPRETATION NEEDED:**
Based on this multi-sensor evidence, provide a 2-paragraph archaeological assessment:

1. **Site Significance**: How compelling is this evidence for a genuine pre-Columbian earthwork? What type of structure might this represent?

2. **Research Priority**: Should this site receive immediate field investigation? What specific archaeological methods would you recommend?

Provide your expert opinion as if briefing a research expedition team.
"""
    
    try:
        # Generate AI analysis
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are Dr. Maria Santos, a distinguished archaeologist specializing in pre-Columbian Amazonian civilizations with 25 years of field experience."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        ai_analysis = response.choices[0].message.content
        logger.info("AI archaeological analysis generated successfully")
        return ai_analysis
        
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        
        # Fallback analysis if OpenAI fails
        fallback_analysis = f"""
AI ARCHAEOLOGICAL INTERPRETATION

**DISCOVERY ANALYSIS:**
Location: {top_hotspot.geometry.y:.6f}°N, {top_hotspot.geometry.x:.6f}°W
AI Confidence: {top_hotspot.mean_prob:.1%}
Model Performance: ROC AUC {model_performance:.3f}

**SITE SIGNIFICANCE:**
This multi-sensor analysis has identified a high-probability archaeological anomaly using advanced 
remote sensing techniques. The combination of topographic irregularities, temporal vegetation 
stability patterns, and spectral signatures suggests potential pre-Columbian earthwork construction.

**RESEARCH PRIORITY:**
Based on the AI confidence score of {top_hotspot.mean_prob:.1%}, this site merits immediate field 
investigation. The detected patterns are consistent with known geoglyph characteristics in the 
Amazon basin, including geometric earthwork formations and altered soil composition signatures.

**RECOMMENDED METHODS:**
- Ground-penetrating radar survey
- High-resolution drone mapping
- Soil composition analysis
- Archaeological excavation planning

Note: OpenAI API error: {e}
"""
        return fallback_analysis
