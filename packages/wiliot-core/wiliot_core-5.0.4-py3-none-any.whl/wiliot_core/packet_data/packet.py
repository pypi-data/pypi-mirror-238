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
import datetime
import logging
import numpy as np
import pandas as pd
import copy
from enum import Enum
from wiliot_core.packet_data.packet_map import parse_packet, gw_result_dict
from wiliot_core.utils.utils import valid_packet_start


FULL_PACKET_PREFIX = 'full_packet'
LEGACY_PACKET_PREFIX = 'process_packet'


packet_tag_length = 74
max_stat_param_val = 65535  # 2 bytes


class InlayTypes(Enum):
    TEO_086 = '086'
    TIKI_096 = '096'
    TIKI_099 = '099'
    BATTERY_107 = '107'
    TIKI_117 = '117'
    TIKI_118 = '118'
    TIKI_121 = '121'
    TIKI_122 = '122'
    TIKI_136 = '136'


class Packet(object):
    """
    Wiliot Packet Object

        :param raw_packet: the raw packet to create a Packet object
        :type raw_packet: str or dict

        :return:
    """

    def __init__(self, raw_packet, time_from_start=None, custom_data=None,
                 inlay_type=None, logger_name=None):
        """
        :param raw_packet:
        :type raw_packet: str or dict
        :param logger_name: the log file we want to write into it.
        :type time_from_start: str
        :param time_from_start: the time when the packet was received according to the gw timer
        :type time_from_start: float
        :param custom_data: the packet custom data as dictionary
        :type custom_data: dict
        :param inlay_type: the antenna/ inlay type (e.g. tiki, teo)
        :type inlay_type: str
        """

        self.is_valid_packet = False
        if logger_name is not None:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = None

        # init packet input:
        packet_in = None
        time_in = None
        self.gw_process = False
        if type(raw_packet) is dict and raw_packet['is_valid_tag_packet']:
            packet_in = raw_packet['packet']
            time_in = raw_packet['time_from_start']
            self.gw_process = True
        elif type(raw_packet) is str:
            packet_in = raw_packet
            time_in = time_from_start

        # check packet type:
        if FULL_PACKET_PREFIX in packet_in:
            self.is_full_packet = True
        elif LEGACY_PACKET_PREFIX in packet_in:
            self.is_full_packet = False
        else:
            self.is_full_packet = None

        # parse packet
        try:
            packet_in_strip = valid_packet_start(packet_in) or packet_in
            self.packet_data, self.gw_data = parse_packet(packet_in_strip, self.is_full_packet)

            # assign results
            self.is_valid_packet = self.gw_data['is_valid_tag_packet'].take(0)
            self.gw_data['time_from_start'] = np.array(time_in)
            self.packet_data['is_full_packet'] = self.is_full_packet
        except Exception as e:
            self.printing_and_logging(f'Could not parse the following packet {packet_in} due to {e}')
            self.is_valid_packet = False
            self.gw_data = {'is_valid_tag_packet': np.array(False)}

        # add more info to packet struct
        self.decoded_data = {}
        if custom_data is not None:
            self.custom_data = custom_data
        else:
            self.custom_data = {}
        self.custom_data['timestamp'] = datetime.datetime.now().timestamp()
        self.inlay_type = inlay_type

        if self.is_valid_packet:
            # TODO need to understand if this section supports everything - START
            if int(self.packet_data['data_uid'], 16) == 5:
                # TX LPM\HPM:
                tx_lpm_hpm = int(self.packet_data['decrypted_packet_type']) & 1
                self.decoded_data['tx_lpm_hpm'] = tx_lpm_hpm
                if tx_lpm_hpm == 0:
                    self.decoded_data['tx_lpm_hpm_str'] = 'LPM'
                else:
                    self.decoded_data['tx_lpm_hpm_str'] = 'HPM'
                # battery mode:
                battery_tag_ind = (int(self.packet_data['decrypted_packet_type']) & 2) >> 1
                self.decoded_data['battery_tag_ind'] = battery_tag_ind
            # TODO - END

    def __len__(self):
        """
        gets number of sprinkler occurrences in packet
        """
        return self.gw_data['rssi'].size

    def __eq__(self, packet):
        """
        packet comparison
        """
        if self.is_same_sprinkler(packet):
            if packet.gw_data['gw_packet'].item() == self.gw_data['gw_packet'].item():
                return True
        return False

    def __str__(self):
        """
        packet print method
        """
        return str(
            'packet_data={packet_data}, gw_data={gw_data}'.format(packet_data=self.packet_data, gw_data=self.gw_data))

    def printing_and_logging(self, message):
        if self.logger:
            self.logger.info(message)
        else:
            print(message)

    def is_packet_from_bridge(self):
        return self.gw_data['is_packet_from_bridge']

    def get_payload(self):
        if self.is_valid_packet:
            return self.packet_data['data_uid'] + self.packet_data['raw_group_id'] + self.packet_data['nonce'] + \
                   self.packet_data['enc_uid'] + self.packet_data['mic'] + self.packet_data['enc_payload']
        else:
            return ''

    def set_inlay_type(self, inlay_type):
        inlay_type = inlay_type if isinstance(inlay_type, str) else inlay_type.value
        self.inlay_type = inlay_type

    def is_in(self, packet):
        """
        is packet contains another packet

        :param packet: the other packet to verify
        :type packet: Packet

        :return: bool
        """
        if self.is_same_sprinkler(packet):
            if packet.gw_data['gw_packet'].item() in self.gw_data['gw_packet']:
                return True
        return False

    def get_packet(self):
        """
        gets raw packet string
        """
        return str(self.packet_data['raw_packet'])

    def split_packet(self, index):
        """
        split packet by index
        """
        packet_a = self.copy()
        packet_b = self.copy()
        remain = len(self) - index
        for key in self.gw_data.keys():
            for i in range(index):
                packet_a.gw_data[key] = np.delete(packet_a.gw_data[key], -1)

            for i in range(remain):
                packet_b.gw_data[key] = np.delete(packet_b.gw_data[key], 0)

        return packet_a, packet_b

    def copy(self):
        return copy.deepcopy(self)

    def sort(self):
        """
        sort gw_data lists according to gw_time
        """
        isort = np.argsort(self.gw_data['stat_param'])
        for key in self.gw_data.keys():
            self.gw_data[key] = self.gw_data[key][isort]

    def get_average_rssi(self):
        return np.average(self.gw_data['rssi'])

    def get_packet_size(self):
        return int(self.packet_data['packet_length'])

    def is_short_packet(self):
        return len(self.get_packet_string(process_packet=False)) < self.get_packet_size()

    def get_packet_content(self, raw_packet=None, get_gw_data=False, sprinkler_num=0):
        if raw_packet is None:
            parsed_packet = self
        else:
            raw_packet = valid_packet_start(raw_packet) or raw_packet
            parsed_packet = Packet(raw_packet=raw_packet)

        if get_gw_data:
            return parsed_packet.packet_data['raw_packet'] + parsed_packet.gw_data['gw_packet'].take(sprinkler_num)

        return parsed_packet.packet_data['raw_packet']

    def get_packet_string(self, i=0, gw_data=True, process_packet=True, full_packet=False):
        """
        gets process_packet string
        """
        if not self.is_valid_packet:
            return None

        process_packet_string = ['', '']
        if process_packet:
            if full_packet:
                raise Exception('Could not get packet string since both full and process packet flags are true')
            process_packet_string = ['process_packet("', '")']
        if full_packet:
            process_packet_string = ['full_packet("', '")']

        if gw_data:
            gw_data = self.gw_data['gw_packet'].take(i)
        else:
            gw_data = ''
        return '{raw_packet}{gw_data}'.format(raw_packet=self.packet_data['raw_packet'],
                                              gw_data=gw_data).join(process_packet_string)

    def get_adva(self):
        return self.packet_data['adv_address']

    def get_flow(self):
        flow_version = hex(int(self.packet_data['flow_ver'], 16))
        return flow_version

    def get_rssi(self):
        return str(self.gw_data['rssi'])

    def get_packet_data_names(self):
        """
        extract all keys name which can potentially be a column in packet df
        :return:
        :rtype: list
        """
        dict_temp = self.__dict__
        keys = list(dict_temp.keys())
        for k in dict_temp.keys():
            if isinstance(dict_temp[k], dict):
                keys = keys + list(dict_temp[k].keys())
        return keys

    @staticmethod
    def get_attribute(raw_packet, loc_length):
        loc = loc_length[0] * 2
        length = loc_length[1] * 2
        return raw_packet[loc:loc + length]

    def is_same_sprinkler(self, packet):
        raw_packet = packet.packet_data['raw_packet']
        if raw_packet == self.packet_data['raw_packet']:
            return True
        return False

    def append_to_sprinkler(self, packet, output_log=True):
        status = True
        if self.is_same_sprinkler(packet):
            for i in range(len(packet)):
                try:
                    # stat param should be unique (time + rssi for same packet)- we make sure no duplications are added.
                    if np.take(packet.gw_data['stat_param'], i).item() not in self.gw_data['stat_param'] or \
                            np.take(packet.gw_data['time_from_start'], i).item() not in self.gw_data['time_from_start']:
                        for key in gw_result_dict.keys():
                            self.gw_data[key] = np.append(self.gw_data[key], np.take(packet.gw_data[key], i))
                        for key in self.custom_data.keys():
                            if key in packet.custom_data.keys():
                                self.custom_data[key] = np.append(self.custom_data[key],
                                                                  np.take(packet.custom_data[key], i))
                            else:
                                self.custom_data[key] = np.append(self.custom_data[key], [None])
                    else:
                        if output_log:
                            self.printing_and_logging('Tried to add duplicated packet to sprinkler {}'.format(packet))
                except Exception as e:
                    self.printing_and_logging('Failed to add packet {} to sprinkler, exception: {}'
                                              .format(packet, str(e)))
        else:
            self.printing_and_logging('Not from the same sprinkler')
            status = False
        # self.sort()
        return status

    def as_dict(self, sprinkler_index=None):  # None not tested
        packet_data = self.packet_data.copy()
        sprinkler_gw_data = self.gw_data.copy()
        custom_data = self.custom_data.copy()
        if sprinkler_index is not None:
            if sprinkler_index > self.gw_data['stat_param'].size:
                return None
            for gw_attr in gw_result_dict.keys():
                sprinkler_gw_data[gw_attr] = np.take(self.gw_data[gw_attr], sprinkler_index)
            for custom_attr in self.custom_data.keys():
                custom_data[custom_attr] = np.take(self.custom_data[custom_attr], sprinkler_index)
            dict_len = 1
        else:
            dict_len = len(self)
            for k, v in packet_data.items():
                packet_data[k] = [v] * dict_len

        data = {**packet_data, **sprinkler_gw_data, **custom_data}
        data['gw_process'] = [self.gw_process] * dict_len  # bool should be a list for pd.DataFrame.from_dict(data)
        data['is_valid_packet'] = [self.is_valid_packet] * dict_len  # bool should be a list
        data['inlay_type'] = [self.inlay_type] * dict_len
        return data

    def as_dataframe(self, sprinkler_index=None):
        data = self.as_dict(sprinkler_index=sprinkler_index)
        packet_df = pd.DataFrame.from_dict(data)

        return packet_df

    def get_per(self, expected_sprinkler_count=6):
        """
        Calculates the packet per at the sprinkler
        @param expected_sprinkler_count - in case of no beacons environment, sprinkler can be bigger than 6.
        @return packet per at percentage
        """
        return 100 * (1 - len(self) / expected_sprinkler_count)

    def get_tbp(self):
        """
        calculates the rate of packets from the same sprinkler
        :return: min_times_found - in msec
        :rtype: int
        """

        def triad_ratio_logic(diff_time_1, diff_time_2, ratio=1.0, error=10):
            """ estimate the time between successive packet according to only 3 packets out of 6 """
            if abs(diff_time_1 - ratio * diff_time_2) <= diff_time_2 / error:
                return True
            elif abs(diff_time_1 - (1 / ratio) * diff_time_2) <= diff_time_1 / error:
                return True
            else:
                return False

        def estimate_diff_packet_time(times_list, pc_time_list):
            if times_list.size < 3:
                return None
            sort_idx = pc_time_list.argsort()
            pc_time_list_sorted = pc_time_list.copy()[sort_idx]
            times_list_sorted = times_list.copy()[sort_idx]

            fix_sort_idx = []
            ind = 0
            pc_time_unique, pc_time_counts = np.unique(pc_time_list_sorted, return_counts=True)
            for unique, counts in zip(pc_time_unique, pc_time_counts):
                if counts > 1:  # several packets
                    ind_with_same_time = [i for i, t in enumerate(pc_time_list_sorted) if t == unique]
                    fix_sort_idx += list(times_list_sorted[ind_with_same_time].argsort() + ind_with_same_time[0])
                else:
                    fix_sort_idx.append(sort_idx[ind])
                ind += counts

            times_list_sorted = times_list_sorted[fix_sort_idx]

            dt = []
            for i, t_hw in enumerate(zip(times_list_sorted[1::], times_list_sorted[:-1])):
                dt_tmp = t_hw[0] - t_hw[1]
                if dt_tmp < 0:  # HW timing was zeroing during the same packets sprinkler
                    n_wrap = 1 + (round(
                        (pc_time_list_sorted[i + 1] - pc_time_list_sorted[i]) * 1000) // max_stat_param_val)
                    dt_tmp = (n_wrap * max_stat_param_val) + t_hw[0] - t_hw[1]
                dt.append(dt_tmp)

            return dt

        def check_if_nan(lst):
            is_nan = pd.isnull(lst)
            if (not isinstance(is_nan, np.ndarray) and is_nan) or (isinstance(is_nan, np.ndarray) and any(is_nan)):
                return True
            return False

        if check_if_nan(self.gw_data['time_from_start']) or check_if_nan(self.gw_data['stat_param']):
            return None

        estimate_diff_time = estimate_diff_packet_time(self.gw_data['stat_param'], self.gw_data['time_from_start'])
        if estimate_diff_time is None:
            return None
        elif len(self) == 3:
            if triad_ratio_logic(estimate_diff_time[0], estimate_diff_time[1], ratio=1):
                return None
            else:
                for ratio in [2, 3, 4]:
                    if triad_ratio_logic(estimate_diff_time[0], estimate_diff_time[1], ratio=ratio):
                        estimate_diff_time = [min(estimate_diff_time[0], estimate_diff_time[1]),
                                              max(estimate_diff_time[0], estimate_diff_time[1]) / ratio]
                        break
                if triad_ratio_logic(estimate_diff_time[0], estimate_diff_time[1], ratio=1.5):
                    estimate_diff_time = [min(estimate_diff_time[0], estimate_diff_time[1]) / 2,
                                          max(estimate_diff_time[0], estimate_diff_time[1]) / 3]

        return int(min(estimate_diff_time))

    def extract_packet_data_by_name(self, key):
        """
        extract data from all packet attribute according to the key name
        :param key: the name of the data (the key of the relevant dictionary)
        :type key: str
        :return: list of the data
        :rtype: list
        """

        if key in self.packet_data:
            data_attr = self.packet_data[key]
        elif hasattr(self, 'decoded_data') and key in self.decoded_data:
            data_attr = self.decoded_data[key]
        elif key in self.gw_data:
            data_attr = self.gw_data[key]
        elif key in self.custom_data:
            data_attr = self.custom_data[key]
        else:
            self.printing_and_logging('key:{} does not exist in packet structure')
            return None
        if isinstance(data_attr, np.ndarray):
            data_attr = data_attr.tolist()
        if not isinstance(data_attr, list):
            data_attr = [data_attr]
        return data_attr

    def filter_by_sprinkler_id(self, sprinkler_ids):
        """
        keep only specific sprinklers in a packet according to the sprinkler id
        :param sprinkler_ids:
        :type sprinkler_ids: list
        :return: filtered packet
        :rtype: Packet or DecryptedPacket
        """

        def filter_per_attr(data_attr):
            for key in data_attr.keys():
                if isinstance(data_attr[key], list) or \
                        (isinstance(data_attr[key], np.ndarray) and data_attr[key].size > 1):
                    filtered_data = [data_attr[key][i] for i in sprinkler_ids]
                    if isinstance(data_attr[key], np.ndarray):
                        data_attr[key] = np.array(filtered_data)
                    else:
                        data_attr[key] = filtered_data
            return data_attr

        filtered_packet = self.copy()
        filtered_packet.gw_data = filter_per_attr(filtered_packet.gw_data)
        filtered_packet.custom_data = filter_per_attr(filtered_packet.custom_data)

        return filtered_packet

    def add_custom_data(self, custom_data):
        for key in custom_data.keys():
            if isinstance(custom_data[key], list):
                if len(custom_data[key]) == self.__len__():
                    self.custom_data[key] = custom_data[key]
                else:
                    self.printing_and_logging('add_custom_data failed - '
                                              'the custom data is a list of a different length than'
                                              ' the number of packets')
            else:
                self.custom_data[key] = self.__len__() * [custom_data[key]]


if __name__ == '__main__':

    packet_1 = {'packet': '03B28DCD99201EFF0005FE0000E0210FFF93B635EBFF1DB118C6D782DC2ED98C404200486436AE8F',
                'is_valid_tag_packet': True, 'adv_address': '03B28DCD9920', 'group_id': 'FE0000', 'rssi': 54,
                'stat_param': 44687,
                'time_from_start': 1.528374, 'counter_tag': 1}
    packet_2 = '03B28DCD99201EFF0005FE0000E0210FFF93B635EBFF1DB118C6D782DC2ED98C404200486436AE82'

    p1 = Packet(packet_1)

    print(p1.get_packet_content('03B28DCD99201EFF0005FE0000E0210FFF93B635EBFF1DB118C6D782DC2ED98C404200486436AE82', get_gw_data=True),)

    p2 = Packet(packet_2)

    p3 = Packet('0437E62F33341E16AFFD02000058AD2AE76DE1D314B003083386A2A1AD139E42C10A0448F93472DC')
    print(p3.get_payload())

    packet_no_gw = Packet('03B28DCD99201EFF0005FE0000E0210FFF93B635EBFF1DB118C6D782DC2ED98C4042004864')
    packet_corrupted_length = Packet('03B28DCD99201EFF0005FE0000E0210FFF93B635EBFF1DB118C6D782DC2ED98C4042004864x')

    print(p1.get_packet_string(0))
    print(p1.get_average_rssi())

    print(p1 == p2)
    print(p1.append_to_sprinkler(p2))

    print(len(p1))
    print(p1.get_average_rssi())

    p1_dict = p1.as_dict()
    p1_df = pd.DataFrame(data=p1_dict)
    print(p1_df)

    print('end')
