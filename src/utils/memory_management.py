"""
Memory management utilities for the archaeological discovery system.
Handles GPU and CPU memory cleanup to prevent out-of-memory errors.
"""

import gc
import logging

logger = logging.getLogger(__name__)

def cleanup_memory():
    """
    Enhanced memory cleanup with GPU support.
    Performs garbage collection and clears GPU memory pools.
    """
    # Standard Python garbage collection
    gc.collect()
    
    # GPU memory cleanup
    try:
        import cupy as cp
        cp.get_default_memory_pool().free_all_blocks()
        cp.get_default_pinned_memory_pool().free_all_blocks()
        logger.info("GPU memory cleaned successfully")
    except ImportError:
        logger.info("CuPy not available, skipping GPU memory cleanup")
    except Exception as e:
        logger.warning(f"GPU memory cleanup failed: {e}")
    
    logger.info("Memory cleanup completed")
