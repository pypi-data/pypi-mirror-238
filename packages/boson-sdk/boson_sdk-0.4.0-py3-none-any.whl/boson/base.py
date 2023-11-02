from types import FunctionType
from typing import Optional, List
import datetime

from boson.boson_core_pb2 import (
    DatasetInfoRequest,
    DatasetInfoResponse,
    PixelsRequest,
    RasterResponse,
    SearchRequest,
    SearchResponse,
)
from google.protobuf.timestamp_pb2 import Timestamp
from boson.features_pb2 import CollectionMsg, ExtentMsg, SpatialExtentMsg, TemporalExtentMsg
from boson.conversion import (
    search_request_to_kwargs,
    pixels_request_to_kwargs,
    feature_collection_to_proto,
    numpy_to_raster_response,
    dict_to_pagination,
)


class BaseProvider:
    def __init__(
        self,
        name: str = "remote",
        alias: str = "Remote Boson Provider",
        description: str = "a remote Boson provider",
        license: str = "(unknown)",
        extent: Optional[dict] = None,
        search_func: Optional[FunctionType] = None,
        pixels_func: Optional[FunctionType] = None,
    ) -> None:
        self.name = name
        self.alias = alias
        self.description = description
        self.license = license
        self.extent = extent
        if self.extent is None:
            self.extent = {
                "spatial": {"bbox": [[-180.0, -90.0, 180.0, 90.0]]},
                "temporal": {"interval": [[None, None]]},
            }

        if search_func is not None and not callable(search_func):
            raise ValueError("search_func must be a callable or None")

        self.search_func = search_func

        if pixels_func is not None and not callable(pixels_func):
            raise ValueError("pixels_func must be a callable or None")
        self.pixels_func = pixels_func
        super().__init__()

    def dataset_info(self, _: DatasetInfoRequest) -> DatasetInfoResponse:
        return DatasetInfoResponse(
            name=self.name,
            alias=self.alias,
            links=[],
            conforms_to=[
                "https://api.stacspec.org/v1.0.0/core",
                "https://api.stacspec.org/v1.0.0/item-search",
                "https://api.stacspec.org/v1.0.0/ogcapi-features",
                "https://api.stacspec.org/v1.0.0/collections",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
            ],
            collections=[CollectionMsg(**self._collection())],
        )

    def _parse_interval(self, interval) -> List[Timestamp]:
        timestamps = []
        for x in interval:
            if x is None:
                timestamps.append(Timestamp())
            elif isinstance(x, datetime.datetime):
                t = Timestamp()
                t.FromDatetime(x)
                timestamps.append(t)
            else:
                timestamps.append(x)

        return timestamps

    def _extent_msg(self) -> ExtentMsg:
        bboxes = self.extent.get("bbox", [[-180, -90, 180, 90]])
        intervals = self.extent.get("interval", [[None, None]])

        bbox_msgs = [SpatialExtentMsg(bbox=bbox) for bbox in bboxes]
        interval_msgs = [
            TemporalExtentMsg(interval=self._parse_interval(interval)) for interval in intervals
        ]

        return ExtentMsg(spatial=bbox_msgs, temporal=interval_msgs)

    def _collection(self) -> dict:
        return {
            "version": "v1.0.0",
            "id": self.name,
            "title": self.alias,
            "description": self.description,
            "license": self.license,
            "extent": self._extent_msg(),
        }

    def pixels(self, request: PixelsRequest) -> RasterResponse:
        pixels_kwargs = pixels_request_to_kwargs(request)

        x = self.pixels_func(**pixels_kwargs)

        return numpy_to_raster_response(x)

    def search(self, request: SearchRequest) -> SearchResponse:
        search_kwargs = search_request_to_kwargs(request)
        res = self.search_func(**search_kwargs)
        pagination = {}

        if isinstance(res, dict):
            fc = res
        elif len(res) == 2:
            fc, pagination = res

        fc_proto = feature_collection_to_proto(fc)
        return SearchResponse(
            feature_collection=fc_proto, pagination=dict_to_pagination(pagination)
        )
