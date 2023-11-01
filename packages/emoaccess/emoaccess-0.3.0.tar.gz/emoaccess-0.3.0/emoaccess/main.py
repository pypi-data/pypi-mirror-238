import pandas as pd
import numpy as np
from typing import Optional, Union
import emoaccess.version as v


def run_base_object_queries(acquisition_id: Optional[str] = None,
                            biomarkers: Optional[list] = None,
                            annotations: Optional[list] = None,
                            segmentation_version: int = None,
                            biomarker_version: int = None,
                            config_mode: Optional[bool] = False):
    """
    Runs the database queries for the base object.
    """
    pass


def run_image_queries(acquisition_id: str = None,
                      channels: Optional[Union[list, np.array]] = None,
                      resolution: Optional[int] = None):

    """
    Fetches the image data
    """
    pass


def run_hne_queries(acquisition_id: str = None):
    """
    Fetches the H&E image data
    """
    pass


def run_mask_queries(acquisition_id: str = None,
                     ):
    """
    Fetches the mask data
    """
    pass


def run_segmentation_mask_queries(acquisition_id: str = None,
                                  study_id: Optional[int] = None,
                                  seg_mask_type: Optional[str] = None,
                                  segmentation_version: Optional[int] = None,
                                  biomarker_version: Optional[int] = None
                                  ):

    pass


def run_metadata_queries(acquisition_id: str = None) -> pd.DataFrame:
    '''
    Run metadata queries
    '''
    pass


def version():
    return v.__version__
