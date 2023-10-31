import json
import socket
import struct
import os

from enum import Enum


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


class Tensor9:

    def __init__(self):
        if self.isEnabled():
            appliance = self.getAppliance()
            print(f"Tensor9 enabled.  Appliance configuration: {appliance}")

    def iAmRunningOnPrem(self):
        """Determine if the current software environment is on-premises, in a customer appliance.

        Returns:
            bool: True if running on-premises, False otherwise.
        """
        return self.isEnabled()

    def isEnabled(self):
        """Determine if the current software environment is on-premises, in a customer appliance.

        Returns:
            bool: True if running on-premises, False otherwise.
        """
        if os.environ.get('TENSOR9_ENABLED', '').lower() == "true":
            return True
        elif os.environ.get('ON_PREM', '').lower() == "true":
            return True
        return False

    def getHttpProxy(self):
        """Fetch the Tensor9 HTTP proxy endpoint that can be used to safely communicate with the outside world.

        Returns:
            str: The Tensor9 HTTP proxy endpoint.

        Raises:
            ValueError: If there's an error in the response or an unexpected message type is received.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.connect(("localhost", 7782))
            self._sendMsg(skt, MsgType.GetHttpProxy, {})
            msgType = self._recvHdr(skt)

            if msgType == MsgType.HttpProxy:
                httpProxy = self._recvJson(skt)
                return httpProxy['endpoint']
            elif msgType == MsgType.Err:
                err = self._recvJson(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msgType}")

    def getAppliance(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.connect(("localhost", 7782))
            self._sendMsg(skt, MsgType.GetAppliance, {})
            msgType = self._recvHdr(skt)

            if msgType == MsgType.Appliance:
                appliance = self._recvJson(skt)
                return appliance
            elif msgType == MsgType.Err:
                err = self._recvJson(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msgType}")

    def _mkHdr(self, msgType):
        return {"v": "V2023_08_22", "type": msgType.name}

    def _sendMsg(self, skt, msgType, msgPayload):
        self._sendJson(skt, self._mkHdr(msgType))
        self._sendJson(skt, msgPayload)

    def _sendJson(self, skt, obj):
        return self._send(skt, json.dumps(obj).encode('utf-8'))

    def _send(self, skt, data):
        # Calculate the frame size as a big endian int32
        frameSz = struct.pack('>I', len(data))

        skt.sendall(frameSz)
        skt.sendall(data)

    def _recvHdr(self, skt):
        hdr = self._recvJson(skt)

        if hdr.get('v') != "V2023_08_22":
            raise ValueError(f"Unexpected protocol version: {hdr}")

        # Raise an error if hdr.type doesn't exist
        if 'type' not in hdr:
            raise ValueError(f"Missing 'type' in header: {hdr}")

        # Parse hdr.type as a MsgType string and parse the string into a MsgType
        try:
            msgType = MsgType(hdr['type'])
        except ValueError:
            raise ValueError(f"Invalid MsgType value in header: {hdr['type']}")

        # Return the MsgType to the caller
        return msgType

    def _recvJson(self, skt):
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
