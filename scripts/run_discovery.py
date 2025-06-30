#!/usr/bin/env python3
"""
Main execution script for Amazon Archaeological Discovery System.
This script orchestrates the complete archaeological discovery workflow.
"""

import sys
import os
import logging
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.config import Config
from utils.memory_management import cleanup_memory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('archaeological_discovery.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Execute the complete archaeological discovery pipeline."""
    logger.info("Starting Amazon Archaeological Discovery System")
    
    try:
        # Validate configuration
        Config.validate_config()
        logger.info("Configuration validated successfully")
        
        # Import main pipeline after config validation
        from main_pipeline import main_ultimate_pipeline
        
        # Execute the discovery pipeline
        trained_model, feature_names, discovered_hotspots = main_ultimate_pipeline()
        
        if trained_model is not None:
            logger.info("Archaeological discovery pipeline completed successfully")
            logger.info(f"Discovered {len(discovered_hotspots)} potential archaeological sites")
        else:
            logger.error("Pipeline execution failed")
            return 1
            
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        return 1
    
    finally:
        cleanup_memory()
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
