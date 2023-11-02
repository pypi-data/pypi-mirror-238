from __future__ import annotations
from collections import Counter
import numpy as np
__all__ = ['CLASS_LABELS', 'Counter', 'language_to_bboxes', 'np', 'z_rotation']
def _compute_counts(boxes):
    ...
def language_to_bboxes(entities):
    """
    
        Args:
            entities: List. List of (cmd,params) tuples that contain the entity command and its parameters
        
    """
def z_rotation(angle):
    """
    
        Helper function to convert angle around z-axis to rotation matrix
        Args:
            angle: Float. Angle around z-axis in radians
        Returns:
            rot_matrix: np.ndarray. 3x3 Rotation matrix
        
    """
CLASS_LABELS: dict = {'wall': 0, 'door': 1, 'window': 2}
