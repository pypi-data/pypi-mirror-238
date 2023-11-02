import pandas as pd
import numpy as np
from typing import Optional


def _yesterday():
    pass


def get_annotation_ids_for_acquisition_id(acquisition_id: str = None,
                                          conn=None):

    """
    Gets the annotation ids for an acquisition id.

    Args:
        acquisition_id: acquisition id
        conn: database connection

    Returns:
        annotation ids
    """
    pass


def get_cell_coordinates_for_acquisition_id(acquisition_id: str = None,
                                            segmentation_version: int = None,
                                            conn=None) -> pd.DataFrame:

    """
    Gets the cell coordinates for an acquisition id.

    Args:
        acquisition_id: acquisition id
        segmentation_version: segmentation version
        conn: database connection

    Returns:
        cell coordinates
    """
    pass


def get_story_masks_for_acquisition_id(acquisition_id):
    pass


def get_segmentation_masks_for_acquisition_id(acquisition_id: str = None,
                                              study_id: Optional[int] = None,
                                              seg_version: int = None
                                              ) -> np.ndarray:

    """
    Returns the segmentation mask for a given acquisition_id.

    Args:
        acquisition_id: str representing unique acquisition id.
        study_id: int representing unique study id.

    Returns:
        A numpy array of the segmentation mask.
    """
    pass


def get_cell_anno_df(acquisition_id: str = None) -> pd.DataFrame:
    pass


def get_biomarker_and_segmentation_versions_for_study_acquisitions(study_id: int = None,
                                                                   conn=None) -> pd.DataFrame:
    pass


def get_all_metadata_for_acquisition_id(acq_ids, conn=None):
    pass


def get_all_acquisition_ids_for_study_id(study_id, conn=None):
    pass


def get_all_biomarkers_for_acquisition_id(acquisition_id, conn=None):
    pass
