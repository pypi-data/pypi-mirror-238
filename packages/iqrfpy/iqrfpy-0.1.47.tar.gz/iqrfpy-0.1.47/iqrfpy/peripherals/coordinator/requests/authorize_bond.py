"""Coordinator Authorize Bond parameters."""

from typing import List, Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['AuthorizeBondRequest', 'AuthorizeBondParams']


class AuthorizeBondParams:
    """AuthorizeBondParams class.

    Parameters for AuthorizeBond request. Each object represents a single
    pair of device address and MID.
    """

    __slots__ = '_req_addr', '_mid'

    def __init__(self, req_addr: int, mid: int):
        """AuthorizeBondParams constructor.

        Args:
            req_addr (int): Device address
            mid (int): Module ID
        """
        self._validate(req_addr=req_addr, mid=mid)
        self._req_addr = req_addr
        self._mid = mid

    def _validate(self, req_addr: int, mid: int):
        """Validates pair parameters.

        Args:
            req_addr (int): Requested node address.
            mid (int): Module ID.
        """
        self._validate_req_addr(req_addr=req_addr)
        self._validate_mid(mid=mid)

    @staticmethod
    def _validate_req_addr(req_addr: int):
        """Validates requested node address.

        Args:
            req_addr (int): Requested node address.
        Raises:
            RequestParameterInvalidValueError: If req_addr is less than 0 or greater than 255.
        """
        if not dpa_constants.BYTE_MIN <= req_addr <= dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Requested address value should be between 1 and 239.')

    @property
    def req_addr(self) -> int:
        """:obj:`int`: Requested node address.

        Getter and setter.
        """
        return self._req_addr

    @req_addr.setter
    def req_addr(self, value: int):
        self._validate_req_addr(req_addr=value)
        self._req_addr = value

    @staticmethod
    def _validate_mid(mid: int):
        """Validates module ID.

        Args:
            mid (int): Module ID.
        Raises:
            RequestParameterInvalidValueError: If mid is less than 0 or greater than 4294967295.
        """
        if not dpa_constants.MID_MIN <= mid <= dpa_constants.MID_MAX:
            raise RequestParameterInvalidValueError('MID value should be an unsigned 32bit integer.')

    @property
    def mid(self) -> int:
        """:obj:`int`: Module ID.

        Getter and setter.
        """
        return self._mid

    @mid.setter
    def mid(self, value: int):
        self._validate_mid(mid=value)
        self._mid = value


class AuthorizeBondRequest(IRequest):
    """Coordinator AuthorizeBond request class."""

    __slots__ = ('_nodes',)

    def __init__(self, nodes: List[AuthorizeBondParams], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        """AuthorizeBond request constructor.

        Args:
            nodes (List[AuthorizeBondParams]): List of address-mid pairs.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535 (Ignore HWPID check).
            dpa_rsp_time (float, optional): DPA request timeout in seconds. Defaults to None.
            dev_process_time (float, optional): Device processing time. Defaults to None.
            msgid (str, optional): JSON API message ID. Defaults to None. If the parameter is not specified, a random
                UUIDv4 string is generated and used.
        """
        self._validate_nodes(nodes)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.AUTHORIZE_BOND,
            m_type=CoordinatorMessages.AUTHORIZE_BOND,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._nodes: List[AuthorizeBondParams] = nodes

    @staticmethod
    def _validate_nodes(nodes: List[AuthorizeBondParams]) -> None:
        """Validates request parameters.

        Args:
            nodes (List[AuthorizeBondParams]): List of address-mid pairs.
        Raises:
            RequestParameterInvalidValueError: If length of nodes is 0 or greater than 11.
        """
        if len(nodes) == 0:
            raise RequestParameterInvalidValueError('At least one pair of requested address and MID is required.')
        if len(nodes) > 11:
            raise RequestParameterInvalidValueError('Request can carry at most 11 pairs of address and MID.')

    @property
    def nodes(self) -> List[AuthorizeBondParams]:
        """:obj:`list` of :obj:`AuthorizeBondParams`: Address-mid pairs.

        Getter and setter.
        """
        return self._nodes

    @nodes.setter
    def nodes(self, value: List[AuthorizeBondParams]):
        self._validate_nodes(value)
        self._nodes = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        """DPA request serialization method.

        Args:
            mutable (bool, optional): Serialize into mutable byte representation of DPA request packet.
                Defaults to False.

        Returns:
            :obj:`bytes`: Immutable byte representation of DPA request packet.\n
            :obj:`bytearray`: Mutable byte representation of DPA request packet (if argument mutable is True).
        """
        pdata = []
        for node in self._nodes:
            pdata.append(node.req_addr)
            pdata.append(node.mid & 0xFF)
            pdata.append((node.mid >> 8) & 0xFF)
            pdata.append((node.mid >> 16) & 0xFF)
            pdata.append((node.mid >> 24) & 0xFF)
        self._pdata = pdata
        return Common.serialize_to_dpa(nadr=self._nadr, pnum=self._pnum, pcmd=self._pcmd, hwpid=self._hwpid,
                                       pdata=self._pdata, mutable=mutable)

    def to_json(self) -> dict:
        """JSON API request serialization method.

        Returns:
            :obj:`dict`: JSON API request object.
        """
        self._params = {'nodes': [{'reqAddr': node.req_addr, 'mid': node.mid} for node in self._nodes]}
        return Common.serialize_to_json(mtype=self._mtype, msgid=self._msgid, nadr=self._nadr, hwpid=self._hwpid,
                                        params=self._params, dpa_rsp_time=self._dpa_rsp_time)
