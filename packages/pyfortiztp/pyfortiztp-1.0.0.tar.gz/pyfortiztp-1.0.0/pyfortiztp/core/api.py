from pyfortiztp.models.devices import Devices


class Api(object):
    """Base API class.
    """

    def __init__(self, userid: str, password: str, client_id: str="fortiztp", forticloud_host: str="https://customerapiauth.fortinet.com", fortiztp_host: str="https://fortiztp.forticloud.com", verify: bool=True, **kwargs):
        self.userid = userid
        self.password = password
        self.client_id = client_id
        self.forticloud_host = forticloud_host + "/api/v1"
        self.fortiztp_host = fortiztp_host + "/public/api/v1"
        self.verify = verify
        self.access_token = None
        self.expires_in = None
        self.refresh_token = None
        self.timestamp = None

    @property
    def devices(self):
        """Endpoints related to device management.
        """
        return Devices(api=self)