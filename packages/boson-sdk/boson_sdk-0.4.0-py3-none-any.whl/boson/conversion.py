import uuid

from typing import Union
import numpy as np
import geodesic
import shapely.wkb as wkb
from google.protobuf.struct_pb2 import Struct
import boson.boson_core_pb2 as pb
from boson.features_pb2 import FeatureMsg, FeatureCollectionMsg, LinkMsg, AssetMsg


def feature_collection_to_proto(fc: geodesic.FeatureCollection) -> FeatureCollectionMsg:
    features = []
    for feature in fc.features:
        features.append(feature_to_proto(feature))

    links = []
    for link in fc.links:
        links.append(link_to_proto(link))

    return FeatureCollectionMsg(features=features, links=links)


def feature_to_proto(feature: geodesic.Feature) -> FeatureMsg:
    geom_wkb = feature.geometry.wkb

    assets = feature.get("assets")

    if assets is not None:
        assetsMsg = {}
        for asset_name, asset in assets.items():
            assetsMsg[asset_name] = AssetMsg(
                title=asset.title,
                description=asset.description,
                type=asset.type,
                href=asset.href,
                roles=asset.roles,
            )
    else:
        assetsMsg = None

    fid = feature.get("id", str(uuid.uuid4()))

    properties = Struct()
    properties.update(feature.properties)

    return FeatureMsg(
        id=fid,
        geometry=geom_wkb,
        properties=properties,
        links=feature.links,
        assets=assetsMsg,
    )


def link_to_proto(link: dict) -> LinkMsg:
    return LinkMsg(
        href=link.get("href"), rel=link.get("rel"), type=link.get("type"), title=link.get("title")
    )


def search_request_to_kwargs(request: pb.SearchRequest) -> dict:
    bbox = request.bbox
    datetime = request.datetime
    filter = request.filter
    collections = [convert_id(c) for c in request.collections]
    feature_ids = [convert_id(c) for c in request.feature_ids]
    fields = None
    if request.fields is not None:
        fields = {
            "include": request.fields.include,
            "exclude": request.fields.exclude,
        }

    intersects = None
    if request.intersects:
        intersects = wkb.loads(request.intersects)

    return {
        "bbox": tuple(bbox) if bbox else None,
        "datetime": datetime,
        "filter": filter,
        "collections": collections,
        "feature_ids": feature_ids,
        "fields": fields,
        "intersects": intersects,
        "count_only": request.count_only,
        "limit": request.limit,
        "pagination": convert_pagination(request.pagination.current),
    }


def numpy_to_raster_response(x: np.ndarray) -> pb.RasterResponse:
    return pb.RasterResponse(
        data=x.tobytes(), content_type=pb.RAW, pixel_type=convert_dtype(x.dtype), shape=x.shape
    )


def pixels_request_to_kwargs(request: pb.PixelsRequest) -> dict:
    bbox = request.bbox
    bbox84 = request.bbox_wgs84
    pixel_size = request.pixel_size
    shape = request.shape

    asset_bands = []
    if request.asset_bands is not None:
        asset_bands = [
            {"asset": ab.asset, "bands": tuple([convert_id(band_id) for band_id in ab.bands])}
            for ab in request.asset_bands
        ]

    return dict(
        bbox=bbox,
        bbox84=bbox84,
        pixel_size=tuple(pixel_size),
        shape=tuple(shape),
        pixel_type=convert_pixel_type(request.pixel_type),
        output_crs=convert_crs(request.output_crs),
        bbox_crs=convert_crs(request.bbox_crs),
        datetime=request.datetime,
        asset_bands=asset_bands,
        filepaths=request.filepaths,
        filter=request.filter,
    )


def convert_crs(crs: pb.CRS) -> str:
    kind = crs.WhichOneof("crs_type")
    if kind == "EPSG":
        return f"EPSG:{crs.EPSG}"
    elif kind == "PROJJSON":
        return crs.PROJJSON


def convert_pixel_type(pt: pb.PixelType) -> str:
    if pt == pb.BYTE:
        return "|u1"
    elif pt == pb.UINT16:
        return "<u2"
    elif pt == pb.UINT32:
        return "<u4"
    elif pt == pb.UINT64:
        return "<u8"
    elif pt == pb.INT16:
        return "<i2"
    elif pt == pb.INT32:
        return "<i4"
    elif pt == pb.INT64:
        return "<i8"
    elif pt == pb.FLOAT32:
        return "<f4"
    elif pt == pb.FLOAT64:
        return "<f8"
    elif pt == pb.CFLOAT32:
        return "<c8"
    elif pt == pb.CFLOAT64:
        return "<c16"
    raise ValueError(f"unknown pixel type {pt}")


def convert_dtype(dt: np.dtype):
    dt = np.dtype(dt)
    if dt == np.uint8:
        return pb.BYTE
    elif dt == np.uint16:
        return pb.UINT16
    elif dt == np.uint32:
        return pb.UINT32
    elif dt == np.uint64:
        return pb.UINT64
    elif dt == np.int16:
        return pb.INT16
    elif dt == np.int32:
        return pb.INT32
    elif dt == np.int64:
        return pb.INT64
    elif dt == np.float32:
        return pb.FLOAT32
    elif dt == np.float64:
        return pb.FLOAT64
    elif dt == np.complex64:
        return pb.CFLOAT32
    elif dt == np.complex128:
        return pb.CFLOAT64
    raise ValueError(f"unknown pixel type {dt}")


def convert_id(id: Union[pb.BandID, pb.FeatureID, pb.CollectionID]) -> Union[str, int]:
    if id.name is not None:
        return id.name
    return id.id


def convert_pagination(p: pb.PageInfo) -> dict:
    if p is None:
        return {}
    kind = p.WhichOneof("method")
    if kind == "page_page_size":
        pps = p.page_page_size
        return {"page": pps.page, "page_size": pps.page_size}
    elif kind == "token":
        return {"token": p.token}
    elif kind == "link":
        method = "GET"
        if p.link.method == pb.POST:
            method = "POST"
        return {
            "link": {"href": p.link.href, "method": method},
        }

    return {}


def dict_to_pagination(p: dict) -> pb.Pagination:
    if "page_size" in p and "page" in p:
        return pb.Pagination(
            next=pb.PageInfo(
                page_page_size=pb.PagePageSize(page=p["page"], page_size=p["page_size"])
            )
        )
    elif "token" in p:
        return pb.Pagination(next=pb.PageInfo(token=p["token"]))
    elif "href" in p:
        return pb.Pagination(
            next=pb.PageInfo(link=pb.Link(href=p["href"], method=p.get("method", "GET")))
        )
