#  """
#    Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """

import numpy as np

ADVA_LENGTH = 12
ADI_LENGTH = 4
HEADER_LENGTH = 4
PACKET_DATA_INFO = 4  # 1E16
SERVICE_UUID_LENGTH = 4  # AFFD
EXTENDED_HEADER_LENGTH = 4
PACKET_DECRYPT_MASK = 0xc
BRG_SERVICE_UUID = 'C6FC'

BLE5_SHIFT = EXTENDED_HEADER_LENGTH + ADI_LENGTH

STAT_PARAM_LENGTH = 4
RSSI_LENGTH = 2
GW_DATA_LENGTH = STAT_PARAM_LENGTH + RSSI_LENGTH
ADI_LOCATION = EXTENDED_HEADER_LENGTH + ADVA_LENGTH
PAYLOAD_LENGTH = 16

packet_data_dict = {'raw_packet': '',
                    'adv_address': (0, 12),
                    'decrypted_packet_type': (24, 1),
                    'group_id': (20, 6),
                    'raw_group_id': '',
                    'test_mode': 0,
                    'header': '',
                    'external_header': '',
                    'adi': '',
                    'en': (12, 2),
                    'type': (14, 2),
                    'data_uid': (16, 4),
                    'nonce': (26, 8),
                    'enc_uid': (34, 12),
                    'mic': (46, 12),
                    'enc_payload': (58, 16),
                    'packet_length': None}

gw_result_dict = {'gw_packet': 'gw_packet',
                  'rssi': 'rssi',
                  'stat_param': 'stat_param',
                  'time_from_start': 'time_from_start',
                  'counter_tag': 'counter_tag',
                  'is_valid_tag_packet': 'is_valid_tag_packet',
                  'is_packet_from_bridge': 'is_packet_from_bridge'}

packet_length_types = {
    '4225': {'name': 'LEGACY', 'packet_tag_length': 78, 'bytes_shift': 0, 'length_modifier': None},
    '4729': {'name': 'BLE5-EXT', 'packet_tag_length': 86, 'bytes_shift': BLE5_SHIFT, 'length_modifier': None},
    '4731': {'name': 'BLE5-DBL-EXT', 'packet_tag_length': 102, 'bytes_shift': BLE5_SHIFT,
             'length_modifier': {'enc_payload': (PAYLOAD_LENGTH * 2)}}
}


def parse_packet(packet_data_input, is_full_packet):
    pixie_result = {}
    gw_result = {}

    # check packet type:
    if is_full_packet is None:
        packet_data_input, expected_length = check_packet_length_with_no_indication(packet_data_input)
        if expected_length is None:
            raise Exception(f'invalid packet length for packet {packet_data_input}, '
                            f'these are the valid tag packet length: {packet_length_types}')
    elif is_full_packet:
        expected_length = packet_length_types[packet_data_input[:HEADER_LENGTH]]
    else:
        packet_data_input = '4225' + packet_data_input
        expected_length = packet_length_types[packet_data_input[:HEADER_LENGTH]]

    # check if packet from bridge
    from_bridge = is_packet_from_bridge(packet_data_input)

    # check if packet length is valid
    received_len = len(packet_data_input)

    if received_len == expected_length['packet_tag_length'] + GW_DATA_LENGTH:
        pass  # valid length
    elif received_len == expected_length['packet_tag_length']:
        packet_data_input += '0' * GW_DATA_LENGTH
    else:
        gw_result['is_valid_tag_packet'] = np.array(False)
        raise Exception(f'invalid packet length for packet {packet_data_input}, '
                        f'expected tag packet length: {expected_length["packet_tag_length"]}')

    try:
        # Parse pixie data
        pixie_result.update(parse_pixie(packet_data_input, expected_length, from_bridge))

        # Parse GW
        gw_result.update(parse_gw(packet_data_input, from_bridge))
        gw_result['is_valid_tag_packet'] = np.array(True)

    except Exception as e:
        print('Packet string cannot be parsed due to {}'.format(e))
        gw_result['is_valid_tag_packet'] = np.array(False)

    return pixie_result, gw_result


def parse_gw(packet_data, is_from_bridge):
    result = {}
    gw_data = packet_data[-GW_DATA_LENGTH:]
    try:
        result['gw_packet'] = np.array(gw_data, dtype='<U6')
        result['rssi'] = np.array(int(gw_data[:RSSI_LENGTH], 16))
        result['stat_param'] = np.array(int(gw_data[RSSI_LENGTH:RSSI_LENGTH+STAT_PARAM_LENGTH], 16))
        result['time_from_start'] = np.array(float('nan'))
        result['counter_tag'] = np.array(float('nan'))
        result['is_packet_from_bridge'] = np.array(is_from_bridge)

        return result

    except Exception as e:
        print('Issue parsing GW data: {}'.format(e))
        return


def parse_pixie(packet_data, packet_len_dict, is_from_bridge):
    try:
        result = {'raw_packet': packet_data}
        valid_length = packet_len_dict['packet_tag_length'] + GW_DATA_LENGTH
        result['header'] = packet_data[:HEADER_LENGTH]
        result['raw_packet'] = packet_data[HEADER_LENGTH:-GW_DATA_LENGTH]
        result['packet_length'] = valid_length
        result.update(parser(result['raw_packet'], packet_len_dict))
        result['flow_ver'] = hex(int(result['adv_address'][:2] + result['adv_address'][-2:], 16)) \
            if not is_from_bridge else hex(0)
        result['decrypted_packet_type'] = (int(result['decrypted_packet_type'], 16) & PACKET_DECRYPT_MASK) >> 2

    except Exception as e:
        raise Exception(f'packet_map: parse_packet: could not parse packet: {packet_data} due to {e}')

    return result


def extract_fields(packet_data, shift=0, length_modifier=None):
    result = {}
    for key, value in packet_data_dict.items():
        if isinstance(value, tuple):
            start, length = value
            if length_modifier and key in length_modifier:
                length = length_modifier[key]
            if shift == BLE5_SHIFT and key == 'adv_address':
                result[key] = packet_data[start + shift - ADI_LENGTH:start + shift - ADI_LENGTH + length]
                continue
            result[key] = packet_data[start + shift:start + shift + length]
            if key == 'group_id':
                result['raw_group_id'] = result[key]
                result[key] = extract_group_id(result[key])

    return result


def parser(packet_data, len_dict):
    result = extract_fields(packet_data, len_dict['bytes_shift'], len_dict['length_modifier'])
    result['ble_type'] = len_dict['name']
    test_mode = test_mode_check(result)
    result['test_mode'] = test_mode
    if len_dict['name'] != 'LEGACY':
        result['extended_header'] = packet_data[:EXTENDED_HEADER_LENGTH]
        result['adi'] = packet_data[ADI_LOCATION:ADI_LOCATION + ADI_LENGTH]

    return result


def test_mode_check(pixie_dict):
    flow_version = hex(int(pixie_dict.get('flow_ver', '0x0'), 16))

    if int(flow_version, 16) < 0x42c:
        if 'FFFFFFFF' in pixie_dict.get('adv_address', ''):
            return 1
    elif int(flow_version, 16) < 0x500:
        adv_address = pixie_dict.get('adv_address', '')
        if adv_address.startswith('FFFF') or adv_address.endswith('FFFF'):
            return 1
    else:
        if int(pixie_dict.get('data_uid', '0'), 16) == 5:
            return 1
    return 0


def is_packet_from_bridge(packet_data):
    service_uuid_index = HEADER_LENGTH + ADVA_LENGTH + PACKET_DATA_INFO
    service_uuid = packet_data[service_uuid_index: service_uuid_index + SERVICE_UUID_LENGTH]
    return service_uuid == BRG_SERVICE_UUID


def extract_group_id(raw_group_id):
    """
    Extract group ID from the raw group ID packet by removing the two last bits.
    :param raw_group_id: as it received by the gateway
    :type raw_group_id: str
    :return: the group ID
    :rtype: str
    """
    raw_group_id_list = [x for x in raw_group_id]
    last_half_byte = raw_group_id_list[4]
    byte_without_2_last_bits = int(last_half_byte, 16) & 3
    raw_group_id_list[4] = str(byte_without_2_last_bits)
    return ''.join(raw_group_id_list)


def hex2bin(hex_value, min_digits=0, zfill=True):
    binary_value = format(int(hex_value, 16), 'b')

    if zfill:
        binary_value = binary_value.zfill(24)

    if len(binary_value) < min_digits:
        binary_value = binary_value.zfill(min_digits)

    return binary_value


def check_packet_length_with_no_indication(packet_data_input):
    expected_length = None
    received_len = len(packet_data_input)
    for packet_prefix, length_dict in packet_length_types.items():
        if received_len == length_dict['packet_tag_length']:
            packet_data_input += '0' * GW_DATA_LENGTH
            expected_length = length_dict

        elif received_len == length_dict['packet_tag_length'] + GW_DATA_LENGTH:
            expected_length = length_dict

        elif length_dict['name'] == 'LEGACY':
            if received_len == length_dict['packet_tag_length'] - HEADER_LENGTH:
                packet_data_input = packet_prefix + packet_data_input + '0' * GW_DATA_LENGTH
                expected_length = length_dict
            elif received_len == length_dict['packet_tag_length'] - HEADER_LENGTH + GW_DATA_LENGTH:
                packet_data_input = packet_prefix + packet_data_input
                expected_length = length_dict

        if expected_length is not None:
            break

    return packet_data_input, expected_length
