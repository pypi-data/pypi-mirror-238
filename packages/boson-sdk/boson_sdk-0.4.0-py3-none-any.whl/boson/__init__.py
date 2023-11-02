import importlib.metadata

from boson.base import BaseProvider
from boson.boson_core_pb2 import (
    DatasetInfoRequest,
    DatasetInfoResponse,
    SearchRequest,
    SearchResponse,
    PixelsRequest,
    RasterResponse,
)
from boson.features_pb2 import CollectionMsg, FeatureMsg, FeatureCollectionMsg, LinkMsg


__version__ = importlib.metadata.version("boson-sdk")
__all__ = [
    "BaseProvider",
    "DatasetInfoRequest",
    "DatasetInfoResponse",
    "SearchRequest",
    "SearchResponse",
    "PixelsRequest",
    "RasterResponse",
    "CollectionMsg",
    "FeatureMsg",
    "FeatureCollectionMsg",
    "LinkMsg",
    "search_request_to_kwargs",
    "feature_collection_to_proto",
    "pixels_request_to_kwargs",
    "numpy_to_raster_response",
]
