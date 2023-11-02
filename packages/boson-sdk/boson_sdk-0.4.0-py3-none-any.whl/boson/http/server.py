from typing import Optional, Any
from types import FunctionType
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException
from boson import (
    BaseProvider,
    DatasetInfoRequest,
    PixelsRequest,
    SearchRequest,
)

__all__ = ["serve"]


class BosonProvider(BaseProvider):
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
        super().__init__(
            name=name,
            alias=alias,
            description=description,
            license=license,
            extent=extent,
            search_func=search_func,
            pixels_func=pixels_func,
        )

        self.router = APIRouter()
        self.router.add_api_route("/dataset_info", self.dataset_info, methods=["POST"])
        self.router.add_api_route("/search", self.search, methods=["POST"])
        self.router.add_api_route("/pixels", self.pixels, methods=["POST"])
        # deprecated
        self.router.add_api_route("/warp", self.pixels, methods=["POST"])

    async def dataset_info(self, request: Request):
        body = await request.body()

        req = DatasetInfoRequest()
        req.ParseFromString(body)

        resp = super().dataset_info(req)
        return self.proto_response(resp)

    async def pixels(self, request: Request):
        body = await request.body()

        req = PixelsRequest()
        req.ParseFromString(body)

        try:
            resp = super().pixels(req)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"unable to run pixels function: {str(e)}")
        return self.proto_response(resp)

    async def search(self, request: Request):
        body = await request.body()

        req = SearchRequest()
        req.ParseFromString(body)

        try:
            resp = super().search(req)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"unable to run search function: {str(e)}")

        return self.proto_response(resp)

    def proto_response(self, resp: Any) -> Response:
        return Response(content=resp.SerializeToString(), media_type="application/x-protobuf")


def serve(
    search_func: Optional[FunctionType] = None, pixels_func: Optional[FunctionType] = None, **kwargs
):
    app = FastAPI()
    server = BosonProvider(pixels_func=pixels_func, search_func=search_func, **kwargs)
    app.include_router(server.router)
    return app
