from iqrfpy.enums.message_types import MessageType


def generate_json_response(response_data: dict):
    json = {
        'mType': response_data['mtype'].value if issubclass(type(response_data['mtype']), MessageType) else response_data['mtype'],
        'data': {
            'msgId': response_data['msgid'],
            'rsp': {
                'nAdr': response_data['nadr'],
                'hwpId': response_data['hwpid'],
                'rCode': response_data['rcode'],
                'dpaVal': response_data['dpa_value']
            },
            'insId': 'iqrfgd2-1',
            'status': response_data['rcode']
        }
    }
    if 'pnum' in response_data:
        json['data']['rsp']['pnum'] = response_data['pnum']
    if 'pcmd' in response_data:
        json['data']['rsp']['pcmd'] = response_data['pcmd']
    if response_data['rcode'] == 0 and 'result' in response_data:
        json['data']['rsp']['result'] = response_data['result']
    return json
