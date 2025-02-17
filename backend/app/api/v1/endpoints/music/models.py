from backend.app.common.models import StrictBaseModel
from fastapi import Form

class DownloadBody(StrictBaseModel):
    url: str = Form(...)
    output_path : str = '/tmp/'
    resolution : str = "360p"