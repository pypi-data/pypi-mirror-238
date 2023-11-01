import json
import os
import socket
import struct
from dataclasses import asdict, is_dataclass
from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class CloudResource:
    class Type(Enum):
        AwsS3Bucket = "AwsS3Bucket"
        AwsSqsQueue = "AwsSqsQueue"

    type: Type
    value: str


@dataclass
class CloudCredential:
    class Type(Enum):
        AwsAccessKeyId = "AwsAccessKeyId"
        AwsSecretAccessKey = "AwsSecretAccessKey"
        AwsSessionToken = "AwsSessionToken"
        AwsRoleArn = "AwsRoleArn"
        AwsTrustedAccountArn = "AwsTrustedAccountArn"

        GcpAutoDetect = "GcpAutoDetect"
        GcpTrustedServiceAccountEmail = "GcpTrustedServiceAccount"
        GcpKeyJson = "GcpKeyJson"
        GcpKeyFile = "GcpKeyFile"

    type: Type
    value: str


@dataclass
class MappedCloudResource:
    resource: CloudResource
    credentials: List[CloudCredential]


class AgentProtocol:
    class MsgType(Enum):
        Err = "Err"
        GetHttpProxy = "GetHttpProxy"
        HttpProxy = "HttpProxy"
        GetAppliance = "GetAppliance"
        Appliance = "Appliance"
        MapResource = "MapResource"
        MappedResource = "MappedResource"
        GetCredentials = "GetCredentials"
        Credentials = "Credentials"

    @dataclass
    class MapResource:
        type: CloudResource.Type
        rawResource: str

    @dataclass
    class GetCredentials:
        type: CloudResource.Type

    @dataclass
    class MappedResource:
        type: CloudResource.Type
        rawOriginal: str
        rawMapped: str

    @dataclass
    class Credentials:
        credentials: List[CloudCredential]


class Tensor9:
    agentHost: str

    def __init__(self):
        self.agentHost = "t9agent.internal"
        if self.is_enabled():
            appliance = self.get_appliance()
            print(f"Tensor9 enabled.  Appliance configuration: {appliance}")

    def i_am_running_on_prem(self):
        """Determine if the current software environment is on-premises, in a customer appliance.

        Returns:
            bool: True if running on-premises, False otherwise.
        """
        return self.is_enabled()

    def is_enabled(self):
        """Determine if the current software environment is on-premises, in a customer appliance.

        Returns:
            bool: True if running on-premises, False otherwise.
        """
        if os.environ.get('TENSOR9_ENABLED', '').lower() == "true":
            return True
        elif os.environ.get('ON_PREM', '').lower() == "true":
            return True
        return False

    def get_appliance(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.connect((self.agentHost, 7782))
            self._send_msg(skt, AgentProtocol.MsgType.GetAppliance, {})
            msgType = self._recv_hdr(skt)

            if msgType == AgentProtocol.MsgType.Appliance:
                appliance = self._recv_json(skt)
                return appliance
            elif msgType == AgentProtocol.MsgType.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msgType}")

    def get_http_proxy(self) -> str:
        """Fetch the Tensor9 HTTP proxy endpoint that can be used to safely communicate with the outside world.

        Returns:
            str: The Tensor9 HTTP proxy endpoint.

        Raises:
            ValueError: If there's an error in the response or an unexpected message type is received.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.connect((self.agentHost, 7782))
            self._send_msg(skt, AgentProtocol.MsgType.GetHttpProxy, {})
            msgType = self._recv_hdr(skt)

            if msgType == AgentProtocol.MsgType.HttpProxy:
                httpProxy = self._recv_json(skt)
                return httpProxy['endpoint']
            elif msgType == AgentProtocol.MsgType.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msgType}")

    def map_resource(self, resource: CloudResource) -> MappedCloudResource:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.connect((self.agentHost, 7782))
            self._send_msg(skt, AgentProtocol.MsgType.MapResource, self._dictify(AgentProtocol.MapResource(resource.type, resource.value.encode("utf-8").hex())))
            msgType = self._recv_hdr(skt)

            if msgType == AgentProtocol.MsgType.MappedResource:
                raw = AgentProtocol.MappedResource(**self._recv_json(skt))
                resource = CloudResource(raw.type, bytes.fromhex(raw.rawMapped).decode("utf-8"))
                credentials = self.get_credentials(resource)
                return MappedCloudResource(resource, credentials)
            elif msgType == AgentProtocol.MsgType.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msgType}")

    def get_credentials(self, resource: CloudResource) -> List[CloudCredential]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.connect((self.agentHost, 7782))
            self._send_msg(skt, AgentProtocol.MsgType.GetCredentials, self._dictify(AgentProtocol.GetCredentials(resource.type)))
            msgType = self._recv_hdr(skt)

            if msgType == AgentProtocol.MsgType.Credentials:
                rawCredentials = AgentProtocol.Credentials(**self._recv_json(skt))
                credentials = []
                for rawCredential in rawCredentials.credentials:
                    credentials.append(CloudCredential(rawCredential['type'], bytes.fromhex(rawCredential['value']).decode("utf-8")))
                return credentials
            elif msgType == AgentProtocol.MsgType.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msgType}")

    def _mk_hdr(self, msgType):
        return {"v": "V2023_08_22", "type": msgType.name}

    def _send_msg(self, skt, msgType, msgPayload):
        self._send_json(skt, self._mk_hdr(msgType))
        self._send_json(skt, msgPayload)

    def _send_json(self, skt, obj):
        encoded = json.dumps(obj).encode('utf-8')
        return self._send(skt, encoded)

    def _send(self, skt, data):
        # Calculate the frame size as a big endian int32
        frameSz = struct.pack('>I', len(data))

        skt.sendall(frameSz)
        skt.sendall(data)

    def _recv_hdr(self, skt) -> AgentProtocol.MsgType:
        hdr = self._recv_json(skt)

        if hdr.get('v') != "V2023_08_22":
            raise ValueError(f"Unexpected protocol version: {hdr}")

        # Raise an error if hdr.type doesn't exist
        if 'type' not in hdr:
            raise ValueError(f"Missing 'type' in header: {hdr}")

        # Parse hdr.type as a MsgType string and parse the string into a MsgType
        try:
            msgType = AgentProtocol.MsgType(hdr['type'])
        except ValueError:
            raise ValueError(f"Invalid MsgType value in header: {hdr['type']}")

        # Return the MsgType to the caller
        return msgType

    def _recv_json(self, skt):
        data = self._recv(skt)
        try:
            # Parse the received data as JSON and return it
            return json.loads(data.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode received data as JSON: {e}")

    def _recv(self, skt):
        reader = skt.makefile('rb')
        try:
            frameSzBuf = reader.read(4)  # Read exactly 4 bytes
            if len(frameSzBuf) < 4:
                raise ConnectionError("Socket connection broken or insufficient data")

            frameSz = struct.unpack('>I', frameSzBuf)[0]
            data = reader.read(frameSz)  # Read exactly frameSz bytes

            if len(data) < frameSz:
                raise ConnectionError("Socket connection broken or insufficient data")

            return data
        finally:
            reader.close()

    def _dictify(self, obj):
        if is_dataclass(obj):
            return {k: self._dictify(v) for k, v in asdict(obj).items()}
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj
