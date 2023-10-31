import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.coordinator.requests.authorize_bond import AuthorizeBondParams, AuthorizeBondRequest


class AuthorizeBondRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x00\x00\x00\x0d\xff\xff\x01\x00\x00\x00\x00'
        self.json = {
            'mType': 'iqrfEmbedCoordinator_AuthorizeBond',
            'data': {
                'msgId': 'authorizeBondTest',
                'req': {
                    'nAdr': 0,
                    'hwpId': 65535,
                    'param': {
                        'nodes': [
                            {
                                'reqAddr': 1,
                                'mid': 0
                            }
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'single_pair',
            [AuthorizeBondParams(req_addr=1, mid=2164554855)],
            b'\x00\x00\x00\x0d\xff\xff\x01\x67\x7c\x04\x81'
        ],
        [
            'three_pairs',
            [
                AuthorizeBondParams(req_addr=1, mid=0),
                AuthorizeBondParams(req_addr=2, mid=2164554855),
                AuthorizeBondParams(req_addr=3, mid=2164554771),
            ],
            b'\x00\x00\x00\x0d\xff\xff\x01\x00\x00\x00\x00\x02\x67\x7c\x04\x81\x03\x13\x7c\x04\x81'
        ]
    ])
    def test_to_dpa(self, _, params, expected):
        request = AuthorizeBondRequest(nodes=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_pair',
            [AuthorizeBondParams(req_addr=1, mid=2164554855)],
        ],
        [
            'three_pairs',
            [
                AuthorizeBondParams(req_addr=1, mid=0),
                AuthorizeBondParams(req_addr=2, mid=2164554855),
                AuthorizeBondParams(req_addr=3, mid=2164554771),
            ],
        ]
    ])
    def test_to_json(self, _, params: List[AuthorizeBondParams]):
        request = AuthorizeBondRequest(nodes=params, msgid='authorizeBondTest')
        self.json['data']['req']['param']['nodes'] = [{'reqAddr': node.req_addr, 'mid': node.mid} for node in params]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            'single_pair',
            [AuthorizeBondParams(req_addr=1, mid=2164554855)],
            b'\x00\x00\x00\x0d\xff\xff\x01\x67\x7c\x04\x81'
        ],
        [
            'three_pairs',
            [
                AuthorizeBondParams(req_addr=1, mid=0),
                AuthorizeBondParams(req_addr=2, mid=2164554855),
                AuthorizeBondParams(req_addr=3, mid=2164554771),
            ],
            b'\x00\x00\x00\x0d\xff\xff\x01\x00\x00\x00\x00\x02\x67\x7c\x04\x81\x03\x13\x7c\x04\x81'
        ]
    ])
    def test_set_nodes(self, _, params: List[AuthorizeBondParams], dpa):
        nodes = [AuthorizeBondParams(req_addr=1, mid=0)]
        request = AuthorizeBondRequest(nodes=nodes, msgid='authorizeBondTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.nodes = params
        self.json['data']['req']['param']['nodes'] = [{'reqAddr': node.req_addr, 'mid': node.mid} for node in params]
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [1, -1],
        [256, 10],
        [2, 4294967297],
    ])
    def test_invalid_param_members_constructor(self, req_addr, mid):
        with self.assertRaises(RequestParameterInvalidValueError):
            AuthorizeBondParams(req_addr=req_addr, mid=mid)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_req_addr(self, req_addr: int):
        params = AuthorizeBondParams(req_addr=0, mid=1)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.req_addr = req_addr

    @parameterized.expand([
        [-1],
        [4294967297]
    ])
    def test_invalid_mid(self, mid: int):
        params = AuthorizeBondParams(req_addr=0, mid=1)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.mid = mid

    @parameterized.expand([
        [[]],
        [[AuthorizeBondParams(req_addr=random.randint(0, 255), mid=random.randint(0, 0xFFFFFFFF))] * 12]
    ])
    def test_invalid_pair_count(self, params: List[AuthorizeBondParams]):
        with self.assertRaises(RequestParameterInvalidValueError):
            AuthorizeBondRequest(nodes=params)
