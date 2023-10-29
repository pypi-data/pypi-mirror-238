from pyfortiztp.core.fortiztp import FortiZTP
import requests


class Devices(FortiZTP):
    """API class for devices.
    """

    def __init__(self, **kwargs):
        super(Devices, self).__init__(**kwargs)

    def all(self, deviceSN: str=None):
        """Retrieves the status of a device.

        Args:
            deviceSN (str): Serial number of a specific device.
        """

        self.login_check()

        # API endpoint
        url = self.api.fortiztp_host + f"/devices"

        # Get a specific device
        if deviceSN:
            url += f"/{deviceSN}"

        # Send our request to the API
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api.access_token}"}, verify=self.api.verify)
        
        # HTTP 200 OK
        if response.status_code == 200:
            return response.json()

    def update(self, deviceSN: list, deviceType: str, provisionStatus: str, provisionTarget: str, region: str=None, externalControllerIp: str=None, externalControllerSn: str=None):
        """Provisions or unprovisions a device.

        Args:
            deviceSN (list): A list of device serial numbers.
            deviceType (str): FortiGate, FortiAP, FortiSwitch or FortiExtender.
            provisionStatus (str): To provision device, set to 'provisioned'. To unprovision device, set to 'unprovisioned'.
            provisionTarget (str): FortiManager, FortiGateCloud, FortiLANCloud, FortiSwitchCloud, ExternalAC, FortiExtenderCloud.
            region (str): Only needed for FortiGateCloud, FortiLANCloud and FortiManagerCloud. For FortiLAN Cloud, please choose one available region for that device return from GET request. For FortiManager Cloud, region is the account region: US-WEST-1, EU-CENTRAL-1, CA-WEST-1 and AP-NORTHEAST-1 etc.
            externalControllerSn (str): Only needed for FortiManager provision.
            externalControllerIp (str): FQDN/IP. Needed for FortiManager or External AC provision.
        """

        self.login_check()

        # Convert deviceSN to a list, if its a str.
        if type(deviceSN) == str:
            deviceSN = [deviceSN]

        # Create a device list
        devices = []

        # Add each device to our devices list
        for serial in deviceSN:

            # Payload
            device = {
                "deviceSN": serial,
                "deviceType": deviceType,
                "provisionStatus": provisionStatus,
                "provisionTarget": provisionTarget
            }

            # Optional fields
            if provisionTarget == "FortiGateCloud" or provisionTarget == "FortiManagerCloud" or provisionTarget == "FortiLANCoud":
                device['region'] = region

            if provisionTarget == "FortiManager" or provisionTarget == "ExternalAC":
                device['externalControllerIp'] = externalControllerIp

            if provisionTarget == "FortiManager":
                device['externalControllerSn'] = externalControllerSn

            # Add device to list
            devices.append(device)

        # Send our request to the API
        response = requests.put(self.api.fortiztp_host + f"/devices", headers={"Authorization": f"Bearer {self.api.access_token}"}, json=devices, verify=self.api.verify)

        # API returns 204 No Content on successful request        
        if response.status_code == 204:
            return response.status_code
        else:
            return response.json()