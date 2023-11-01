from bpkio_api.consumer import BpkioSdkConsumer
from bpkio_api.models.BkYouSupportPackage import BkYouSupportPackage
from bpkio_api.response_handler import postprocess_response
from uplink import Query, get, response_handler, returns


@response_handler(postprocess_response)
class SupportApi(BpkioSdkConsumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

    @returns.json(BkYouSupportPackage)
    @get("admin/support/bkyou-support-package")
    def create_bkyou_support_package(
        self, session_id: Query("sessionId")
    ) -> BkYouSupportPackage | None:
        """Get a support package for a particular session"""
