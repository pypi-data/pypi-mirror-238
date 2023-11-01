import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.node.requests.validate_bonds import ValidateBondsRequest, NodeValidateBondsParams


class ValidateBondsRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x01\x08\xff\xff\x0a\x00\x00\x00\x00\x0b\x01\x00\x00\x00'
        self.json = {
            'mType': 'iqrfEmbedNode_ValidateBonds',
            'data': {
                'msgId': 'validateBondsTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'nodes': [
                            {
                                'bondAddr': 10,
                                'mid': 0
                            },
                            {
                                'bondAddr': 11,
                                'mid': 1
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
            [NodeValidateBondsParams(bond_addr=1, mid=2164554855)],
            b'\x01\x00\x01\x08\xff\xff\x01\x67\x7c\x04\x81'
        ],
        [
            'three_pairs',
            [
                NodeValidateBondsParams(bond_addr=1, mid=0),
                NodeValidateBondsParams(bond_addr=2, mid=2164554855),
                NodeValidateBondsParams(bond_addr=3, mid=2164554771),
            ],
            b'\x01\x00\x01\x08\xff\xff\x01\x00\x00\x00\x00\x02\x67\x7c\x04\x81\x03\x13\x7c\x04\x81'
        ]
    ])
    def test_to_dpa(self, _, params, expected):
        request = ValidateBondsRequest(nadr=1, nodes=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_pair',
            [NodeValidateBondsParams(bond_addr=1, mid=2164554855)],
        ],
        [
            'three_pairs',
            [
                NodeValidateBondsParams(bond_addr=1, mid=0),
                NodeValidateBondsParams(bond_addr=2, mid=2164554855),
                NodeValidateBondsParams(bond_addr=3, mid=2164554771),
            ],
        ]
    ])
    def test_to_json(self, _, params):
        request = ValidateBondsRequest(nadr=1, nodes=params, msgid='validateBondsTest')
        self.json['data']['req']['param']['nodes'] = [{'bondAddr': node.bond_addr, 'mid': node.mid} for node in params]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            'single_pair',
            [NodeValidateBondsParams(bond_addr=1, mid=2164554855)],
            b'\x01\x00\x01\x08\xff\xff\x01\x67\x7c\x04\x81'
        ],
        [
            'three_pairs',
            [
                NodeValidateBondsParams(bond_addr=1, mid=0),
                NodeValidateBondsParams(bond_addr=2, mid=2164554855),
                NodeValidateBondsParams(bond_addr=3, mid=2164554771),
            ],
            b'\x01\x00\x01\x08\xff\xff\x01\x00\x00\x00\x00\x02\x67\x7c\x04\x81\x03\x13\x7c\x04\x81'
        ]
    ])
    def test_set_nodes(self, _, params, dpa):
        nodes = [NodeValidateBondsParams(bond_addr=10, mid=0), NodeValidateBondsParams(bond_addr=11, mid=1)]
        request = ValidateBondsRequest(nadr=1, nodes=nodes, msgid='validateBondsTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.nodes = params
        self.json['data']['req']['param']['nodes'] = [{'bondAddr': node.bond_addr, 'mid': node.mid} for node in params]
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
    def test_invalid_param_members(self, bond_addr, mid):
        with self.assertRaises(RequestParameterInvalidValueError):
            NodeValidateBondsParams(bond_addr=bond_addr, mid=mid)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_bond_addr(self, bond_addr: int):
        params = NodeValidateBondsParams(bond_addr=1, mid=0)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.bond_addr = bond_addr

    @parameterized.expand([
        [-1],
        [4294967297]
    ])
    def test_invalid_mid(self, mid: int):
        params = NodeValidateBondsParams(bond_addr=1, mid=0)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.mid = mid

    @parameterized.expand([
        [[NodeValidateBondsParams(bond_addr=random.randint(0, 255), mid=random.randint(0, 0xFFFFFFFF))] * 12]
    ])
    def test_invalid_pair_count(self, params: List[NodeValidateBondsParams]):
        with self.assertRaises(RequestParameterInvalidValueError):
            ValidateBondsRequest(nadr=1, nodes=params)
