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
import signal
import socket
import subprocess
from os.path import isfile, isdir
from tkinter import Tk, INSERT, END, filedialog, Toplevel, Frame
from tkinter.font import Font
from tkinter.messagebox import askyesno
import serial.tools.list_ports
import pygubu
import json
import os
import sys
import multiprocessing
import logging
import datetime
import threading
import pandas as pd
import numpy as np
import csv
import re
from tkinter import ttk
import time
import tkinter as tk
import webbrowser
from wiliot_core import WiliotGateway, StatType, ActionType, DataType, valid_output_power_vals, \
    valid_sub1g_output_power
from wiliot_core import TagCollection, PacketList, Packet
from wiliot_core import WiliotDir
from wiliot_tools.local_gateway_gui.utils.gw_macros import macros
from wiliot_tools.local_gateway_gui.utils.debug_mode import debug_flag
from pygubu.builder import ttkstdwidgets, tkstdwidgets  # used for EXE generating, do not remove

from wiliot_tools.utils.get_version import get_version

if sys.platform == "darwin":
    from appdirs import *
    import PySimpleGUI

    multiprocessing.freeze_support()  # will open the script nonstop without it

DECRYPTION_MODE = False


def print_exceptions():
    package_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(package_dir, "extended")

    if (os.path.isfile(path) and os.path.getsize(path) > 0) or debug_flag['debug_bool']:
        return True
    return False


try:
    from wiliot_core import DecryptedTagCollection, DecryptedPacket
    from wiliot_tools.extended.pixie_analyzer.config_files.plot_config import plot_config
    from wiliot_tools.extended.pixie_analyzer.pixie_analyzer import PixieAnalyzer
    from wiliot_core.packet_data.extended.config_files.packet_data_map import packet_data_map
    from wiliot_tools.local_gateway_gui.live_portal.wiliot_live_plotting import WiliotLivePlotting

    DECRYPTION_MODE = True
    print('Working on decrypted mode')
except Exception as e:
    if print_exceptions():
        print('Working on encrypted mode')  # SHOULD NOT BE PRINTED FOR PUBLIC USER!
        print(e)  # SHOULD NOT BE PRINTED FOR PUBLIC USER!
    pass

# default config values:
MAX_CONSECUTIVE_EXCEPTION = 30
EP_DEFAULT = 18  # Energizing pattern
EPs_DEFAULT = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
               50, 51, 52)  # All Energizing pattern
TP_O_DEFAULT = 5  # timing profile on
TP_P_DEFAULT = 15  # timing profile period
PI_DEFAULT = 0  # pace interval
RC_DEFAULT = 37
RCs_DEFAULT = (37, 38, 39)
DATA_TYPES = ('raw', 'processed', 'statistics', 'full_UID_mode', 'decoded_packet')
CONFIG_SUM = "EP:{EP}\nTP_ON:{TP_ON}\nTP_P:{TP_P}\nRC:{RC}\nPI:{PI}\nF:{F}"
baud_rates = ["921600"]
energy_pattern_dict = {18: 'Energizing on channel 39 only',
                       20: '20% channel 37 , 80% channel 39',
                       50: 'Energizing in 915Mhz',
                       51: 'Energizing on both channel 39 and 915Mhz',
                       }

__version__ = get_version()


def prepare_version_attribute_options():
    version_attributes = {}

    all_packet_versions = list(packet_data_map.keys())
    all_packet_versions.sort(reverse=True)  # new version documented better
    for version in packet_data_map:
        num_set = set()
        str_set = set()
        if version < 2.2:
            continue
        if packet_data_map[version]['static']:
            for feature in packet_data_map[version]['static']:
                if feature in str_set or feature in num_set:
                    continue
                if packet_data_map[version]['static'][feature].get('type', 0) != 'str':
                    num_set.add(feature)
                else:
                    str_set.add(feature)
                if 'output' in packet_data_map[version]['static'][feature]:
                    for f in packet_data_map[version]['static'][feature]['output']:
                        if f.get('type', 0) != 'str':
                            num_set.add(f['name'])
                # if 'Output' not in packet_data_map[version]['static']

        for version_number in range(4):
            if version_number in packet_data_map[version]:
                for feature in packet_data_map[version][version_number]:
                    if packet_data_map[version][version_number].get('type', 0) != 'str':
                        num_set.add(feature)
                    if 'output' in packet_data_map[version][version_number][feature]:
                        for f in packet_data_map[version][version_number][feature]['output']:
                            if f.get('type', 0) != 'str':
                                num_set.add(f['name'])

        features_list = list(num_set)
        features_list.append('')
        features_list.sort()
        version_attributes[version] = features_list
    return version_attributes


def create_logger():
    wiliot_dir = WiliotDir()
    gw_gui_path = os.path.join(wiliot_dir.get_wiliot_root_app_dir(), 'local_gateway_gui')
    if not os.path.exists(gw_gui_path):
        os.makedirs(gw_gui_path)
    gw_gui_log_path = os.path.join(gw_gui_path, 'logs')
    if not os.path.exists(gw_gui_log_path):
        os.makedirs(gw_gui_log_path)
    date_time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_log_name = f'gw_gui_{date_time_str}.log'

    logger = logging.getLogger('GatewayGUiLog')
    logger.setLevel(logging.DEBUG)

    log_file_path = os.path.join(gw_gui_log_path, file_log_name)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


class GatewayUI(object):
    gwCommandsPath = os.path.join(os.path.abspath('utils'), '.gwCommands.json')
    gwUserCommandsPath = os.path.join(os.path.abspath('utils'), '.gwUserCommands.json')
    gwAllCommands = []
    gwCommands = []
    gwUserCommands = []
    portActive = False
    log_state = False
    autoscroll_state = True
    logger = None
    stat_type = StatType.N_FILTERED_PACKETS
    log_path = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'gw_log.{}'.format("log")
    prev_packet_cntr = 0
    dash_plotting_instance = None
    live_plot_type = 'dash'
    stop_live_plots_event = threading.Event()

    def __init__(self, main_app_folder='', tk_frame=None):
        print('GW UI mode is activated')
        print(__version__)
        self.busy_processing = False
        self.close_requested = False
        # check which mode we are:
        self.decryption_mode = DECRYPTION_MODE
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()
        self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])
        self.filter_tag = [re.compile('')]
        self.data_handler_listener = None
        self.full_run_logger = create_logger()
        self.live_plots_data = {}

        if self.decryption_mode:
            try:
                self.myPixieAnalyzer = PixieAnalyzer()
                self.packet_decoder = self.myPixieAnalyzer.PacketDecoder()
            except Exception as e:
                self.myPixieAnalyzer = None
                if print_exceptions():
                    self.full_run_logger.exception('problem during loading PixieAnalyzer: {}'.format(e))

        self.env_dir = WiliotDir()
        self.logs_dir = os.path.join(self.env_dir.get_tester_dir("local_gateway_gui"), "logs")
        if not isdir(self.logs_dir):
            self.env_dir.create_dir(self.logs_dir)

        # 2: Load an ui file
        utils_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils')
        if self.decryption_mode:
            uifile = os.path.join(utils_path, 'gw_debugger.ui')
        else:
            uifile = self.get_encrypted_ui(os.path.join(utils_path, 'gw_debugger.ui'))
        builder.add_from_file(uifile)
        builder.add_resource_path(utils_path)

        if tk_frame:
            self.ttk = tk_frame  # tkinter.Frame , pack(fill="both", expand=True)
        else:
            self.ttk = Tk()
        self.ttk.title(f"Wiliot Local Gateway GUI Application (V{__version__})")

        # 3: Create the widget using a self.ttk as parent
        self.mainwindow = builder.get_object('mainwindow', self.ttk)

        self.ttk = self.ttk

        # set the scroll bar of the main textbox
        textbox = self.builder.get_object('recv_box')
        scrollbar = self.builder.get_object('scrollbar')
        textbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=textbox.yview)
        self.builder.get_object('scrollbar').set(self.builder.get_object('recv_box').index(INSERT),
                                                 self.builder.get_object('recv_box').index(END))
        self.builder.get_object('recv_box').grid()

        self.builder.connect_callbacks(self)

        # upload pre-defined commands
        self.gwCommandsPath = os.path.join(main_app_folder, self.gwCommandsPath)
        if isfile(self.gwCommandsPath):
            with open(self.gwCommandsPath, 'r') as f:
                self.gwCommands = json.load(f)

        self.gwUserCommandsPath = os.path.join(main_app_folder, self.gwUserCommandsPath)
        if isfile(self.gwUserCommandsPath):
            with open(self.gwUserCommandsPath, 'r') as f:
                self.gwUserCommands = json.load(f)

        self.gwAllCommands = self.gwCommands + self.gwUserCommands

        self.ttk.lift()
        self.ttk.attributes("-topmost", True)
        self.ttk.attributes("-topmost", False)

        self.ObjGW = WiliotGateway(logger_name=self.full_run_logger.name)
        self.config_param = {}
        self.formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S')
        self.logger_num = 1

        # update ui
        if self.decryption_mode:
            self.multi_tag = DecryptedTagCollection()
            self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])
            self.plot_config = plot_config()
            self.custom_plot = True
            self.builder.get_object('plot_log')['state'] = 'disabled'
            self.builder.get_object('load_log')['state'] = 'disabled'
        else:
            self.multi_tag = TagCollection()
            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'disabled'

            self.plot_config = None
            self.custom_plot = False

        self.ui_update('init')
        self.ui_update('available_ports')

        self.ttk.protocol("WM_DELETE_WINDOW", self.close_window)

        self.ttk.after_idle(self.periodic_call)
        self.ttk.mainloop()

    @staticmethod
    def get_encrypted_ui(ui_path):
        decrypted_guis = ['save_to_file', 'plot_log', 'load_log', 'custom_plots', 'packet_show_button',
                          'analysis_plot_label', 'live_plot_label', 'plotting_configs']
        enc_ui_path = ui_path.replace('.ui', '_encrypted.ui')
        if os.path.isfile(enc_ui_path):
            return enc_ui_path

        with open(ui_path, 'r') as f:
            lines = f.readlines()
            new_lines = []
            need_to_del_section = False
            n_child = 0
            for line in lines:
                if not need_to_del_section:
                    for dec_gui in decrypted_guis:
                        if dec_gui in line:
                            need_to_del_section = True
                            break
                if need_to_del_section:
                    if 'child' in line:
                        n_child += 1
                    if n_child == 2:
                        need_to_del_section = False
                        n_child = 0
                else:
                    new_lines.append(line)

        with open(enc_ui_path, 'w') as new_f:
            new_f.writelines(new_lines)
        return enc_ui_path

    def get_log_file_name(self, filename=None):
        if filename is None:
            filename = self.builder.get_object('log_path').get()
        if filename:
            filename = filename.strip("\u202a")  # strip left-to-right unicode if exists
            if os.path.isfile(filename):
                return filename
            return os.path.join(self.logs_dir, filename)
        else:
            return None

    def get_filter_text(self, text=''):
        if len(text) > 0:
            text = text.replace(' ', '')
            self.filter_tag = text.split(',')
            self.filter_tag = [re.compile(f.lower()) for f in self.filter_tag]
        else:
            self.filter_tag = [re.compile('')]

    def close_window(self):
        self.close_requested = True
        print("User requested close at:", time.time(), "Was busy processing:", self.busy_processing)

    def periodic_call(self):
        if not self.close_requested:
            self.busy_processing = True
            self.busy_processing = False
            self.ttk.after(500, self.periodic_call)

        else:
            print("Destroying GUI at:", time.time())
            try:
                self.ObjGW.exit_gw_api()
                if self.data_handler_listener is not None and self.data_handler_listener.is_alive():
                    self.data_handler_listener.join()
                if self.dash_plotting_instance is not None:
                    self.stop_live_plots_event.set()
                if self.log_state:
                    logging.FileHandler(self.get_log_file_name()).close()
                self.exit_packet_show()
                self.ttk.destroy()
                exit(0)
            except Exception as e:
                self.full_run_logger.exception('problem during periodic call: {}'.format(e))
                exit(1)

    def on_connect(self):
        if not self.portActive:  # Port is not opened
            try:
                port = self.builder.get_object('port_box').get().rsplit(' ', 1)[0]
                baud = self.builder.get_object('baud_rate_box').get().rsplit(' ', 1)[0]
                if port == '' or baud == '':
                    return

                if self.ObjGW.open_port(port, baud):  # open and check if succeed
                    self.print_function(str_in="> Port successfully opened")
                    self.portActive = True
                    self.builder.get_object('connect_button').configure(text='Disconnect')
                    # print version:
                    self.print_function(str_in=self.ObjGW.hw_version + '=' + self.ObjGW.sw_version)
                    self.builder.get_object('recv_box').see(END)
                    # config gw to receive packets (and not only manage bridges):
                    rsp = self.ObjGW.write('!set_tester_mode 1', with_ack=True)
                    if 'command complete event' in rsp['raw'].lower():
                        self.config_param['pacer_val'] = '0'
                        self.config_param['filter'] = 'N'
                    # update UI:
                    self.ui_update('connect')
                    self.start_listening()
                    # update config:
                    rsp = self.ObjGW.write('!print_config_extended', with_ack=True)
                    if rsp['raw'] and 'unsupported' not in rsp['raw'].lower():
                        self.print_function(rsp['raw'])
                        self.from_gw_msg_to_config_param(rsp['raw'])

                else:
                    self.print_function(str_in="> Can't open Port - check connection parameters and try again")
                    self.portActive = False
            except Exception as e:
                self.print_function(str_in="> Encounter a problem during connection: {}".format(e))

        else:  # Port is opened, close it...
            try:
                self.print_function(str_in="> Disconnecting from Port")
                self.ObjGW.stop_continuous_listener()
                self.ObjGW.close_port()
                self.builder.get_object('connect_button').configure(text="Connect")
                self.portActive = False
                self.ui_update('connect')
            except Exception as e:
                self.print_function(str_in="> Encounter a problem during disconnection: {}".format(e))

    def from_gw_msg_to_config_param(self, gw_msg):
        conv_str = [{'msg': 'Energizing Pattern=', 'param': 'energy_pattern'},
                    {'msg': 'Scan Ch/Freq=', 'param': 'received_channel'},
                    {'msg': 'Transmit Time=', 'param': 'time_profile_on'},
                    {'msg': 'Cycle Time=', 'param': 'time_profile_period'}]
        for d in conv_str:
            if d['msg'] in gw_msg:
                x = gw_msg.split(d['msg'])[1].split(',')[0]
                try:
                    int(x)
                    self.config_param[d['param']] = x
                except Exception as e:
                    self.full_run_logger.exception(e)
                    pass
        self.ui_update('config')

    def start_listening(self):
        # start listening:
        self.ObjGW.start_continuous_listener()
        if self.data_handler_listener is None or not self.data_handler_listener.is_alive():
            self.data_handler_listener = threading.Thread(target=self.recv_data_handler, args=())
            self.data_handler_listener.start()

    def on_search_ports(self):
        self.ObjGW.available_ports = [s.device for s in serial.tools.list_ports.comports() if
                                      'Silicon Labs' in s.description or 'CP210' in s.description]
        if len(self.ObjGW.available_ports) == 0:
            self.ObjGW.available_ports = [s.name for s in serial.tools.list_ports.comports()
                                          if 'Silicon Labs' in s.description or 'CP210' in s.description]
        # update ui:
        self.ui_update('available_ports')

    def get_data_type(self):
        selected_data_type = self.builder.get_object('data_type').get()
        tag_collection_type = ['processed', 'statistics', 'full_UID_mode', 'full_UID_mode', 'decoded_packet']
        if selected_data_type == 'raw':
            data_type = DataType.RAW
        elif selected_data_type in tag_collection_type:
            data_type = DataType.DECODED_TAG_COLLECTION if DECRYPTION_MODE else DataType.TAG_COLLECTION
        else:
            data_type = DataType.RAW
        return selected_data_type, data_type

    def add_filtered_tag_collection(self, new_tag_col, cur_tag_col):
        tag_id_to_remove = []
        for tag_id in new_tag_col.tags.keys():
            for f in self.filter_tag:
                if not f.search(tag_id.lower()):
                    tag_id_to_remove.append(tag_id)

        for tag_id in tag_id_to_remove:
            new_tag_col.tags.pop(tag_id)

        cur_tag_col.__add__(new_tag_col)
        return new_tag_col

    @staticmethod
    def get_full_uid_str(tag_col):
        str_prefix = 'TagID: ' if DECRYPTION_MODE else 'AdvA: '
        str_out = []
        for tag_id, packet_list in tag_col.tags.items():
            str_out.append(str_prefix + tag_id + f', Counter: {len(packet_list)}')
        return '\n'.join(str_out)

    def get_processed_str(self, tag_col):
        str_out = []
        for tag_id, packet_list in tag_col.tags.items():
            for packet in packet_list:
                final_str = self.get_processed_line_per_packet(packet)
                str_out.append(final_str)
        return '\n'.join(str_out)

    @staticmethod
    def get_processed_line_per_packet(packet):
        packet_data = packet.packet_data
        gw_data = packet.gw_data
        raw_packet = packet_data.get('raw_packet', 'N/A')
        ble_type = packet_data.get('ble_type', 'N/A')

        packet_data_without_raw = {key: value for key, value in packet_data.items() if
                                   (key != 'raw_packet' and key != 'ble_type')}

        gw_data_converted = \
            {key: value.item() if isinstance(value, np.ndarray) and value.size == 1 else value
             for key, value in gw_data.items()}

        packet_data_str = ''
        for key, value in packet_data_without_raw.items():
            if key == 'nonce':
                packet_data_str += f"{key}:{value}\n"
            else:
                packet_data_str += f"{key}:{value},"

        packet_data_str = packet_data_str.rstrip(',')

        gw_data_str = ','.join(
            f"{key}:{value}" for key, value in gw_data_converted.items())

        raw_packet_str = f"Raw Packet: {raw_packet}, BLE Type: {ble_type}"
        final_str = f"{raw_packet_str}\n{packet_data_str}\n{gw_data_str}\n{'*' * 130}"
        return final_str

    @staticmethod
    def get_statistics_str(tag_col):
        uid = 'tag_id' if DECRYPTION_MODE else 'adv_address'
        attr = [uid, 'num_cycles', 'num_packets', 'tbp_mean', 'rssi_mean']

        statistics_list = tag_col.get_statistics_list(attributes=attr)
        str_out = f'---------------------- {datetime.datetime.now()}: Tags Statistics ----------------------'
        for stat in statistics_list:
            str_out += f'\n{stat}'
        return str_out

    @staticmethod
    def get_raw_str(dict_in):
        str_out = []
        for pkt in dict_in:
            data_str = []
            for key, value in pkt.items():
                if key == 'time':
                    value = '{:.6f}'.format(value)
                data_str.append("{}:{}".format(key, value))
            str_out.append(','.join(data_str))
        return '\n'.join(str_out)

    @staticmethod
    def get_decoded_str(tag_col):
        str_out = []
        for tag_id, packet_list in tag_col.tags.items():
            for packet in packet_list:
                packet_de_str = packet.to_oneline_log()
                if packet_de_str is not None:
                    str_out.append(packet_de_str)
        return '\n'.join(str_out)

    def recv_data_handler(self):
        self.full_run_logger.info("DataHandlerProcess Start")
        consecutive_exception_counter = 0
        last_stat_time = time.time()
        while True:
            time.sleep(0)
            try:
                if self.close_requested or not self.portActive:
                    self.full_run_logger.info("DataHandlerProcess Stop")
                    return

                # check if there is data to read
                if self.ObjGW.is_data_available():
                    selected_data_type, data_type = self.get_data_type()
                    data_in = self.ObjGW.get_packets(action_type=ActionType.ALL_SAMPLE, num_of_packets=None,
                                                     data_type=data_type)

                    if data_type == DataType.TAG_COLLECTION or data_type == DataType.DECODED_TAG_COLLECTION:
                        tag_col = self.multi_tag
                        filtered_new_data = self.add_filtered_tag_collection(new_tag_col=data_in, cur_tag_col=tag_col)
                        str_to_print = None
                        if selected_data_type == 'full_UID_mode':
                            self.on_clear(restart=False)
                            str_to_print = self.get_full_uid_str(tag_col)

                        elif selected_data_type == 'statistics' and time.time() - last_stat_time > 2:
                            str_to_print = self.get_statistics_str(tag_col)
                            last_stat_time = time.time()

                        elif selected_data_type == 'decoded_packet':
                            self.update_tags_count_label(self.multi_tag.get_tags_count())
                            str_to_print = self.get_decoded_str(filtered_new_data)

                        elif selected_data_type == 'processed':
                            str_to_print = self.get_processed_str(filtered_new_data)

                        if str_to_print:
                            self.print_function(str_in=str_to_print)

                    elif data_type == DataType.RAW:
                        str_to_print = self.get_raw_str(data_in)
                        self.print_function(str_in=str_to_print)

                    consecutive_exception_counter = 0
            except Exception as e:
                print(f'got exception during recv_data: {e}, try to recovery')
                consecutive_exception_counter = consecutive_exception_counter + 1
                if consecutive_exception_counter > MAX_CONSECUTIVE_EXCEPTION:
                    self.full_run_logger.exception(f"Abort DataHandlerProcess due to {e}")
                    return

    def on_macro_folder(self):
        macro_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils', 'gw_macros.py')
        self.print_function(str_in=f"> Go to {macro_path} to edit macros")

    def on_update_gw_version_helper(self, version_path_entry=None):
        if version_path_entry:
            version_path_entry = version_path_entry.strip("\u202a")  # strip left-to-right unicode if exists
            if not os.path.isfile(version_path_entry):
                self.print_function(str_in="> cannot find the entered gw version file:")
                return
        success_update = self.ObjGW.update_version(versions_path=version_path_entry)
        return success_update

    def on_update_gw_version(self):
        # The waiting window
        loading_window = Tk()
        loading_window.title('Loading')
        loading_window.geometry('300x200')
        loading_window.configure(bg='#ededed')
        frame = Frame(loading_window, bg='#ededed')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        message_label = ttk.Label(frame, text='Loading new version update...', font=("Helvetica", 16),
                                  background='#ededed')
        message_label.pack(pady=10)
        progress = ttk.Progressbar(frame, length=200, mode='indeterminate')
        progress.pack(pady=10)
        progress.start()
        loading_window.grab_set()
        loading_window.after(30000, lambda: [progress.stop(), loading_window.destroy()])
        # The actual process
        self.print_function(str_in="> Updating GW version, please wait...")
        version_path_entry = self.builder.get_object('version_path').get()
        success_update = self.on_update_gw_version_helper(version_path_entry)
        # listen again:
        self.start_listening()
        if success_update:
            self.builder.get_object('version_path').delete(0, END)
            self.builder.get_object('version_num_cur').delete('1.0', END)
            self.builder.get_object('version_num_cur').insert(END, 'current:' + self.ObjGW.sw_version)
            self.print_function(str_in="> Update GW version was completed [{}]".format(self.ObjGW.sw_version))
        else:
            self.print_function(str_in="> Update GW version was failed ")

    def on_reset(self):
        self.ObjGW.reset_gw()
        time.sleep(1)
        self.ObjGW.write('!set_tester_mode 1', with_ack=True)
        self.ObjGW.reset_listener()

    def exit_packet_show(self):
        try:
            # Check if the Bokeh server is already running on port 5006 and kill it
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 5006))  # bokeh port
            if result == 0:
                # Server is already running on port 5006, kill it and start a new server
                if sys.platform == "darwin" or sys.platform == 'linux':
                    p = subprocess.Popen(['lsof', '-i', ':5006'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = p.communicate()
                    pid = out.decode('utf-8').split('\n')[1].split()[1]
                else:
                    # windows
                    p = os.popen('netstat -ano | findstr :5006')
                    out = p.read()
                    pid_list = list(set([pid.split(' ')[-1] for pid in out.split('\n') if '0.0.0.0:5006' in pid]))
                    if len(pid_list) != 1:
                        self.print_function("Could not decide which process to kill: {}".format(pid_list))
                        return
                    pid = pid_list[0]
                need_to_kill = askyesno(title='Kill Packet Show', message='There is a running Live Plot application. '
                                                                          'Would you like to kill it?')
                if need_to_kill:
                    os.kill(int(pid), signal.SIGILL)

        except Exception as e:
            self.print_function(f"Error during exit_packet_show: {e}")

    def on_plotting_configs(self):

        settings_window = tk.Toplevel()
        settings_window.title("Select Plotting Tool")

        def dash_selected():
            self.live_plot_type = 'dash'
            self.bokeh_var.set(False)

        def bokeh_selected():
            self.live_plot_type = 'bokeh'
            self.dash_var.set(False)

        self.dash_var = tk.BooleanVar()
        self.dash_var.set(self.live_plot_type == 'dash')
        dash_check = ttk.Checkbutton(settings_window, variable=self.dash_var, text="Dash", command=dash_selected)
        dash_check.pack(pady=10)
        self.bokeh_var = tk.BooleanVar()
        self.bokeh_var.set(self.live_plot_type == 'bokeh')
        bokeh_check = ttk.Checkbutton(settings_window, variable=self.bokeh_var, text="Bokeh", command=bokeh_selected)
        bokeh_check.pack(pady=10)

    def plotting_choosing_window(self):

        def open_dash():
            # dash plotting instance for live plotting
            if self.dash_plotting_instance is None:
                if not DECRYPTION_MODE:
                    raise Exception('Cannot run WiliotLivePlotting on public version, '
                                    'please make sure you have Wiliot Private package')
                self.dash_plotting_instance = WiliotLivePlotting(self, self.stop_live_plots_event)
                self.dash_plotting_instance.init_live_plot()
            webbrowser.open("http://127.0.0.1:8050/")

        def open_bokeh():
            self.on_packet_show()

        if self.live_plot_type == 'bokeh':
            open_bokeh()
        elif self.live_plot_type == 'dash':
            open_dash()
        else:
            raise Exception('plot type is not supported')

    def on_packet_show(self):
        try:
            # Check if the Bokeh server is already running on port 5006 and kill it
            self.exit_packet_show()

            self.ObjGW.open_socket_connection()
            # Server is not running on port 5006, start a new server and show the app
            current_script = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_script)
            os.chdir(current_dir)
            package_dir = os.getcwd()

            if 'extended' not in os.listdir(package_dir):
                package_dir = os.path.dirname(package_dir)

            path = os.path.join(package_dir, "extended", "packet_show", "packet_show.py")
            subprocess.Popen(['bokeh', 'serve', '--port', '5006', '--show', path])
        except Exception as e:
            self.print_function(f"Error during on_packet_show: {e}")

    def on_enter_write(self, args):
        if args.char == '\r':
            self.on_write()

    def on_write(self):
        cmd_value = self.builder.get_object('write_box').get()
        rsp_val = self.ObjGW.write(cmd_value, with_ack=True, max_time=0.100)
        self.on_user_event(user_event_text=cmd_value)
        self.print_function(', '.join(['{}: {}'.format(k, v) for k, v in rsp_val.items()]))

        if cmd_value.strip() not in list(self.builder.get_object('write_box')['values']):
            temp = list(self.builder.get_object('write_box')['values'])

            # keep only latest instances
            if temp.__len__() == 20:
                temp.pop(0)
            if len(self.gwUserCommands) >= 20:
                self.gwUserCommands.pop(0)
            self.gwUserCommands.append(cmd_value)
            temp.append(cmd_value)
            self.builder.get_object('write_box')['values'] = tuple(temp)
            with open(self.gwUserCommandsPath, 'w+') as f:
                json.dump(self.gwUserCommands, f)

        self.ui_update(state='config')

    def on_run_macro(self):
        from wiliot_tools.local_gateway_gui.utils.gw_macros import macros  # import again to check changes during run
        selected_macro = self.builder.get_object('macros_ddl').get()
        if selected_macro in macros.keys():
            data_handler_listener = threading.Thread(target=self.run_macro, args=())
            data_handler_listener.start()
        else:
            self.print_function("Please select a valid macro")

    def run_macro(self):
        selected_macro = self.builder.get_object('macros_ddl').get()
        macro_commands = macros[selected_macro]
        for c in macro_commands:
            command_value = c["command"]
            time_value = c["wait"]
            self.print_function("Command: {c},\t Wait: {t}".format(c=command_value, t=time_value))
            command_start_time = time.time()
            if command_value == 'user_event':
                self.on_user_event(user_event_text=c.get('values', 'user_event'))
            elif command_value == 'save_log':
                self.on_processed_data(c.get('values', r'~/Downloads/output.csv'))
            elif command_value == 'update_version':
                self.on_update_gw_version_helper(c.get('values', r''))
            else:
                rsp_val = self.ObjGW.write(command_value, with_ack=True)
                self.on_user_event(user_event_text=command_value)
                self.print_function(', '.join(['{}: {}'.format(k, v) for k, v in rsp_val.items()]))
                # self.start_listening()
            while time.time() - command_start_time < time_value:
                time.sleep(1)
        self.print_function('Macro {selected_macro} Done.'.format(selected_macro=selected_macro))

    def on_config(self):
        pacer_val = int(self.builder.get_object('pace_inter').get())
        energ_ptrn_val = int(self.builder.get_object('energizing_pattern').get())
        time_profile_val = [int(self.builder.get_object('timing_profile_on').get()),
                            int(self.builder.get_object('timing_profile_period').get())]
        received_channel_val = int(self.builder.get_object('received_channel').get())
        self.print_function(str_in="> Setting GW configuration...")
        if energ_ptrn_val in energy_pattern_dict.keys():
            self.print_function(str_in='Setting pattern {energ_ptrn_val} -> {pattern_explanation}'.format(
                energ_ptrn_val=str(energ_ptrn_val), pattern_explanation=energy_pattern_dict[energ_ptrn_val]))

        config_param_set, gateway_response = self.ObjGW.config_gw(pacer_val=pacer_val,
                                                                  energy_pattern_val=energ_ptrn_val,
                                                                  time_profile_val=time_profile_val,
                                                                  received_channel=received_channel_val,
                                                                  with_ack=True)
        # update config parameters:
        for key, value in config_param_set.__dict__.items():
            if key == 'filter' or key == 'modulation':
                self.config_param[key] = str(value)[0]
            else:
                self.config_param[key] = str(value)

        self.ui_update(state='config')
        self.print_function(str_in="> Configuration is set")

    def on_clear(self, restart=True):
        self.builder.get_object('recv_box').delete('1.0', END)
        self.builder.get_object('recv_box').see(END)
        if restart:
            self.multi_tag = DecryptedTagCollection() if DECRYPTION_MODE else TagCollection()
            if self.decryption_mode:
                self.update_tags_count_label(0)
                self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])
                if self.dash_plotting_instance is not None:
                    self.dash_plotting_instance.reset_live_plot()

    def set_logger(self, level=logging.DEBUG):
        """
        setup logger to allow running multiple logger
        """
        handler = logging.FileHandler(self.get_log_file_name())
        handler.setFormatter(self.formatter)

        self.logger = logging.getLogger('logger{}'.format(self.logger_num))
        self.logger.setLevel(level)
        self.logger.addHandler(handler)
        self.logger_num = self.logger_num + 1

    def on_filter_id(self, args):
        if args.char == '\r':
            f_input = self.builder.get_object('filter_id').get()
            if not f_input == 'filter ids':
                self.get_filter_text(f_input)
            if self.dash_plotting_instance is not None:
                self.dash_plotting_instance.reset_live_plot()

    def on_log(self):
        """ This function creates log for a specific part of the process that the user chooses"""
        # Setting the boolean variable's value to opposite when clicking the button
        self.log_state = not self.log_state
        # Clicking on Start Logging for the first time, or clicking Stop log
        if self.log_state:
            check_log_path = self.get_log_file_name()
            if not check_log_path:
                self.log_state = False
                self.print_function(str_in='> Log path is invalid')
                self.builder.get_object('log_button')['text'] = 'Start Log'
                return
            try:
                self.set_logger()
                self.on_clear()
                self.print_function(str_in='> Start Logging [{}]'.format(self.get_log_file_name()))
                self.builder.get_object('log_button')['text'] = 'Stop Log'
                return
            except Exception as e:
                self.print_function(str_in='> Log path is invalid: {}'.format(e))
                self.log_state = False
                self.builder.get_object('log_button')['text'] = 'Start Log'
                return
        # Clicking Stop logging
        else:
            self.builder.get_object('log_button')['text'] = 'Start Log'
            self.print_function(str_in='> Stop Logging')
            logging.FileHandler(self.get_log_file_name()).close()
            self.on_processed_data(output_path=self.get_log_file_name())
            # reset log path and user events
            self.log_path = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'gw_log.{}'.format("log")
            self.builder.get_object('log_path').delete(0, 'end')
            self.builder.get_object('log_path').insert(END, self.log_path)
            self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])

    def on_autoscroll(self):
        self.autoscroll_state = self.builder.get_variable('autoscroll_state').get()

    def on_data_type_change(self, selected):
        self.on_clear()
        if selected.widget.get() == 'decoded_packet' or selected.widget.get() == 'full_UID_mode':
            self.builder.get_object('filter_id')['state'] = 'enabled'
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id').insert(0, 'filter ids')
            self.get_filter_text()
            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'enabled'
                self.builder.get_object('plot_log')['state'] = 'enabled'

        else:
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id')['state'] = 'disabled'
            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'disabled'
                self.builder.get_object('plot_log')['state'] = 'disabled'
            self.update_tags_count_label(clear=True)

    def update_tags_count_label(self, count=0, clear=False):
        text_obj = self.builder.get_object('tags_count')
        text_obj.delete("end")
        if clear:
            text_obj.insert(END, "\n".format(
                tag_format=str(count)))
        else:
            text_obj.insert(END, "\ntags count: {tag_format}".format(
                tag_format=str(count)))
        text_obj.see(END)

    def on_custom_plots(self):
        t = Toplevel(self.ttk)
        CustomPlotGui(plot_config=self.plot_config, print_func=self.print_function, tk_frame=t,
                      logger=self.full_run_logger)

    def on_user_event(self, user_event_text=None):
        if user_event_text is None:
            user_event_text = self.builder.get_object('user_event_text').get()
        self.print_function(str_in="user_event_time: {}, User event: {}".format(self.ObjGW.get_curr_timestamp_in_sec(),
                                                                                user_event_text))
        user_event_row = {'user_event_time': self.ObjGW.get_curr_timestamp_in_sec(), 'user_event_data': user_event_text}
        self.user_events = self.user_events = pd.concat([self.user_events,
                                                         pd.DataFrame(data=[user_event_row.values()],
                                                                      columns=user_event_row.keys())],
                                                        axis=0, ignore_index=True)

    def on_plot_log(self):
        plots_location = filedialog.askdirectory(initialdir="~/Documents",
                                                 title="Choose output location")
        if plots_location != '':
            if len(self.multi_tag) > 0:
                try:
                    self.print_function(str_in="Starting plot analyzing")
                    plot_thread = threading.Thread(target=self.myPixieAnalyzer.plot_graphs,
                                                   args=(self.multi_tag, self.user_events, 6, 'Yes', 50,
                                                         False, self.plot_config, plots_location))
                    plot_thread.start()
                    self.print_function(
                        str_in='Plot files will be saved in {plots_location}'.format(plots_location=plots_location))
                except PermissionError as pe:
                    self.print_function(
                        str_in='Got "{strerror}" in folder: {plots_location}'.format(strerror=pe.strerror,
                                                                                     plots_location=plots_location))
                except Exception as e:
                    self.print_function(str_in='Unknown error: {}'.format(e))

            else:
                self.print_function(str_in='No packets received in decoded_packet mode yet.')
        else:
            self.print_function(str_in='No output location selected.')

    def on_load_log(self):
        file_path_input = filedialog.askopenfilename(initialdir="~/Documents",
                                                     title="Select packet log input file",
                                                     filetypes=[("csv files", "*.csv")])
        plots_location = filedialog.askdirectory(initialdir="~/Documents",
                                                 title="Choose output location")
        if plots_location != '':
            if '_plot.csv' not in file_path_input:
                self.print_function(str_in='Invalid file, choose *_plot.csv file')
            elif file_path_input != '':
                try:
                    self.print_function(str_in="Starting plot analyzing")
                    start = time.time()
                    [_, plot_data, user_event] = self.packet_decoder.parse(input=file_path_input)

                    user_event_file = file_path_input.replace('_plot', '_user_event')
                    if os.path.isfile(user_event_file):
                        user_event = pd.read_csv(user_event_file, index_col=False)

                    end = time.time()
                    self.print_function(str_in='PlotGraphsGen2: {t}'.format(t=round(end - start, 2)))

                    if len(plot_data) > 0:
                        plot_thread = threading.Thread(target=self.myPixieAnalyzer.plot_graphs,
                                                       args=(plot_data, user_event, 6, 'Yes', 50,
                                                             False, self.plot_config, plots_location))
                        plot_thread.start()
                        self.print_function(
                            str_in='Plot files will be saved in {plots_location}'.format(plots_location=plots_location))
                    else:
                        self.print_function(str_in='Empty TagCollection')
                except Exception as e:
                    self.print_function(str_in='problem during on_load_log: {}'.format(e))
            else:
                self.print_function(str_in='No file selected.')
        else:
            self.print_function(str_in='No output location selected.')

    def extract_tag_collection_from_log(self, log_path=None):
        tag_col_out = DecryptedTagCollection() if DECRYPTION_MODE else TagCollection()
        packets, packets_time = self.extract_packets_from_log(log_path=log_path)
        for p, t in zip(packets, packets_time):
            new_packet = DecryptedPacket(raw_packet=p, time_from_start=t, logger_name=self.full_run_logger.name) \
                if DECRYPTION_MODE else Packet(raw_packet=p, time_from_start=t, logger_name=self.full_run_logger.name)
            tag_col_out.append(new_packet)
        return tag_col_out

    def extract_packets_from_log(self, log_path=None):
        if log_path is None:
            self.print_function(str_in='no log path was found. Export csv failed')
            return
        try:
            packets = []
            packets_time = []
            if isfile(log_path):
                f = open(log_path, 'r')
                lines = f.readlines()

                for line in lines:
                    if 'raw:process_packet("' in line or 'is_valid_tag_packet:True' in line:
                        # a data line
                        if 'raw:process_packet("' in line:
                            re_match = re.search("process_packet\(\"(\w+)\"", line)
                            packet_raw = str(re_match.groups(1)[0])
                        else:  # packet: ABCD format (data type = processed
                            re_match = re.search(",packet:(\w+)", line)
                            packet_raw = str(re_match.groups(1)[0])
                        if 'time_from_start:' in line:
                            re_match = re.search("time_from_start:(\d+.\d+)", line)
                            packet_time = float(re_match.groups(1)[0])
                        else:
                            re_match = re.search("time:(\d+.\d+)", line)
                            packet_time = float(re_match.groups(1)[0])

                        packets.append(packet_raw)
                        packets_time.append(packet_time)
                f.close()
            return packets, packets_time
        except Exception as e:
            self.print_function(str_in='export packets from log was failed due to: {}'.format(e))
            return None, None

    @staticmethod
    def return_time_str():
        now = datetime.datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
        return dt_string

    def on_processed_data(self, output_path=None):
        if output_path is None:
            output_path = filedialog.asksaveasfilename(
                filetypes=[("txt file", ".csv")], defaultextension=".csv", title='Choose location to save csv',
                initialfile='{current_date}.csv'.format(current_date=self.return_time_str()))
        # check path
        if output_path == '':
            self.print_function(str_in='No output location selected.')
            return
        # check data
        if len(self.multi_tag) == 0:
            raw_tag_col = TagCollection()
            if output_path.endswith('.log'):
                raw_tag_col = self.extract_tag_collection_from_log(log_path=output_path)
            if len(raw_tag_col) == 0:
                self.print_function(str_in='No packets received yet.')
                return
            else:
                self.multi_tag = raw_tag_col
        # log
        try:
            csv_location = output_path.replace('.log', '.csv')
            packet_data_location = csv_location.replace('.csv', '_plot.csv')
            stat_data_location = csv_location.replace('.csv', '_stat.csv')
            user_event_location = csv_location.replace('.csv', '_user_event.csv')

            self.multi_tag.to_csv(packet_data_location, add_sprinkler_info=True)
            stat_df = self.multi_tag.get_statistics()

            self.user_events.to_csv(user_event_location, index=False)
            stat_df.to_csv(path_or_buf=stat_data_location)
            self.print_function(str_in='Export multi-tag csv - {path}'.format(path=packet_data_location))

        except Exception as e:
            self.print_function(str_in=f'during save to file got the following error: {e}')

    def on_custom_ep(self):
        # open a new gui:
        tk_frame = Toplevel(self.ttk)
        CustomEPGui(gw_obj=self.ObjGW, print_func=self.print_function, tk_frame=tk_frame,
                    logger=self.full_run_logger)

    def ui_update(self, state):
        # updating UI according to the new state
        if state == 'init':
            self.builder.get_object('write_box')['values'] = tuple(self.gwAllCommands)
            self.builder.get_object('macros_ddl')['values'] = tuple(macros.keys())
            # default config values:
            self.builder.get_object('energizing_pattern')['values'] = tuple(EPs_DEFAULT)
            self.builder.get_object('energizing_pattern').set(EP_DEFAULT)
            self.builder.get_object('timing_profile_on').set(TP_O_DEFAULT)
            self.builder.get_object('timing_profile_period').set(TP_P_DEFAULT)
            self.builder.get_object('pace_inter').set(PI_DEFAULT)
            self.builder.get_object('received_channel')['values'] = tuple(RCs_DEFAULT)
            self.builder.get_object('received_channel').set(RC_DEFAULT)

            self.config_param = {"energy_pattern": str(EP_DEFAULT),
                                 "received_channel": str(RC_DEFAULT),
                                 "time_profile_on": str(TP_O_DEFAULT),
                                 "time_profile_period": str(TP_P_DEFAULT),
                                 "pacer_val": str(PI_DEFAULT),
                                 "filter": "N"}

            self.builder.get_object('config_sum').insert(END, CONFIG_SUM.format(
                RC="", EP="", TP_ON="", TP_P="", PI="", F=""))
            self.builder.get_object('config_sum').see(END)
            if self.decryption_mode:
                self.builder.get_object('data_type')['values'] = tuple(DATA_TYPES)
            else:
                self.builder.get_object('data_type')['values'] = tuple(DATA_TYPES[:-1])
            self.builder.get_object('data_type').set('raw')

            self.builder.get_object('log_button')['text'] = 'Start Log'
            self.builder.get_object('log_path').insert(END, self.log_path)

            self.builder.get_variable('autoscroll_state').set(self.autoscroll_state)

            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'disabled'
                self.builder.get_object('plot_log')['state'] = 'disabled'
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id')['state'] = 'disabled'
            if self.decryption_mode:
                self.builder.get_object('load_log')['state'] = 'enabled'
                self.builder.get_object('custom_plots')['state'] = 'enabled'

            ver_num, _ = self.ObjGW.get_latest_version_number()
            if ver_num is not None:
                self.builder.get_object('version_num').insert(END, 'new:' + ver_num)
            self.builder.get_object('version_num_cur').insert(END, 'current:')
            self.builder.get_object('version_browser')['state'] = 'disable'

        elif state == 'available_ports':
            if self.ObjGW.available_ports:
                self.print_function(str_in=f'> Finished searching for ports, available ports: '
                                           f'{", ".join(self.ObjGW.available_ports)}')
                self.builder.get_object('port_box')['values'] = tuple(self.ObjGW.available_ports)
                self.builder.get_object('port_box').set(self.ObjGW.available_ports[0])
            else:
                self.print_function(str_in="no serial ports were found. please check your connections and refresh")
            self.builder.get_object('baud_rate_box')['values'] = tuple(baud_rates)
            self.builder.get_object('port_box')['state'] = 'enabled'
            self.builder.get_object('baud_rate_box')['state'] = 'enabled'
            self.builder.get_object('baud_rate_box').set(baud_rates[0])

        elif state == 'connect':
            if self.portActive:
                # connected
                enable_disable_str = 'enabled'
                enable_disable_con_str = 'disabled'
                self.builder.get_object('version_num_cur').delete('1.0', END)
                self.builder.get_object('version_num_cur').insert(END, 'current:' + self.ObjGW.sw_version)
            else:
                # disconnected
                enable_disable_str = 'disabled'
                enable_disable_con_str = 'enabled'
                self.builder.get_object('version_num_cur').delete('1.0', END)
                self.builder.get_object('version_num_cur').insert(END, 'current:')

            self.builder.get_object('config_button')['state'] = enable_disable_str
            self.builder.get_object('energizing_pattern')['state'] = enable_disable_str
            self.builder.get_object('timing_profile_on')['state'] = enable_disable_str
            self.builder.get_object('timing_profile_period')['state'] = enable_disable_str
            self.builder.get_object('pace_inter')['state'] = enable_disable_str
            self.builder.get_object('write_button')['state'] = enable_disable_str
            self.builder.get_object('write_box')['state'] = enable_disable_str
            self.builder.get_object('macros_ddl')['state'] = enable_disable_str
            self.builder.get_object('run_macro')['state'] = enable_disable_str
            self.builder.get_object('reset_button')['state'] = enable_disable_str
            self.builder.get_object('received_channel')['state'] = enable_disable_str
            self.builder.get_object('data_type')['state'] = enable_disable_str
            self.builder.get_object('update_button')['state'] = enable_disable_str
            self.builder.get_object('version_path')['state'] = enable_disable_str
            self.builder.get_object('version_browser')['state'] = enable_disable_str
            # self.builder.get_object('custom_ep')['state'] = enable_disable_str  #TODO remove comment when fw support

            self.builder.get_object('port_box')['state'] = enable_disable_con_str
            self.builder.get_object('baud_rate_box')['state'] = enable_disable_con_str

        elif state == 'config':
            self.builder.get_object('config_sum').delete(1.0, END)
            self.builder.get_object('config_sum').insert(END,
                                                         CONFIG_SUM.format(RC=self.config_param["received_channel"],
                                                                           EP=self.config_param["energy_pattern"],
                                                                           TP_ON=self.config_param["time_profile_on"],
                                                                           TP_P=self.config_param[
                                                                               "time_profile_period"],
                                                                           PI=self.config_param["pacer_val"],
                                                                           F=self.config_param["filter"]))
            self.builder.get_object('config_sum').see(END)

    def on_log_browser(self):
        path_loc = filedialog.asksaveasfilename(
            filetypes=[("txt file", ".log")], defaultextension=".log", title='Choose location to save log',
            initialfile='gw_log_{}.log'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        self.builder.get_object('log_path').delete(0, 'end')
        self.builder.get_object('log_path').insert(END, path_loc)

    def on_version_browser(self):
        path_loc = filedialog.askopenfilename(
            filetypes=[("txt file", ".zip")], defaultextension=".zip", title='Choose version file location')
        self.builder.get_object('version_path').delete(0, 'end')
        self.builder.get_object('version_path').insert(END, path_loc)

    def print_function(self, str_in):
        try:
            self.full_run_logger.info(str_in)
            recv_box = self.builder.get_object('recv_box')
            recv_box.insert(END, str_in + '\n')
            recv_box.config()
            if self.autoscroll_state:
                recv_box.see(END)
            if self.log_state:
                self.logger.info(str_in)
        except Exception as e:
            self.full_run_logger.exception('print function failed due to: {}'.format(e))


class CustomEPGui(object):

    def __init__(self, gw_obj=None, print_func=None, tk_frame=None, logger=None):
        self.close_requested = False
        self.logger = logger if logger is not None else logging.getLogger('root')
        if gw_obj is None:
            self.gw_obj = WiliotGateway()
        else:
            self.gw_obj = gw_obj
        if print_func is None:
            self.print_func = print
        else:
            self.print_func = print_func
        self.ep_builder = pygubu.Builder()
        ep_ui_file = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils'), 'custom_ep.ui')
        self.ep_builder.add_from_file(ep_ui_file)
        if tk_frame:
            self.ttk_ep = tk_frame
        else:
            self.ttk_ep = Tk()

        self.ttk_ep.title('Wiliot Custom Energy Pattern')
        self.custom_ep_window = self.ep_builder.get_object('custom_ep_window', self.ttk_ep)
        self.ep_builder.connect_callbacks(self)
        self.ttk_ep.lift()
        self.ttk_ep.attributes("-topmost", True)
        # update ui
        self.energy_power_2_4 = [p['abs_power'] for p in valid_output_power_vals]
        valid_bb = (0, 2, 7, 12, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 33, 36, 40)
        self.ep_builder.get_object('beacon_2_4_power')['values'] = tuple([self.energy_power_2_4[-1] - b
                                                                          for b in valid_bb])
        self.ep_builder.get_object('beacon_2_4_power').set(self.energy_power_2_4[-1])
        self.ep_builder.get_object('energy_2_4_power')['values'] = tuple(self.energy_power_2_4)
        self.ep_builder.get_object('energy_2_4_power').set(self.energy_power_2_4[-1])
        self.ep_builder.get_object('energy_sub1g_power')['values'] = tuple(valid_sub1g_output_power)
        self.ep_builder.get_object('energy_sub1g_power').set(valid_sub1g_output_power[-1])
        font = Font(family="Segoe UI", size=12)
        self.ttk_ep.option_add("*TCombobox*Listbox*Font", font)
        self.ttk_ep.option_add("*TCombobox*Font", font)
        self.ttk_ep.protocol("WM_DELETE_WINDOW", self.close_window)
        self.ttk_ep.after_idle(self.periodic_call)
        self.ttk_ep.mainloop()

    def on_set_custom_ep(self):
        custom_ep_dict = {'scan_ch': None, 'period_2_4': None, 'beacon_to_beacon': None, 'beacon_to_energy': None,
                          'beacon_2_4_duration': None, 'beacon_2_4_frequencies': None, 'beacon_2_4_power': None,
                          'energy_2_4_duration': None, 'energy_2_4_frequencies': None, 'energy_2_4_power': None,
                          'period_sub1g': None,
                          'energy_sub1g_duration': None, 'energy_sub1g_frequencies': None, 'energy_sub1g_power': None
                          }

        def extract_val(field_name):
            try:
                if 'frequencies' in field_name:
                    # extract a list:
                    all_freq = self.ep_builder.get_object(field_name).get()
                    all_freq = all_freq.replace(' ', '')
                    all_freq = all_freq.split(',')
                    val_list = []
                    for f in all_freq:
                        if f != '':
                            val_list.append(int(f))
                    return val_list
                else:
                    return int(self.ep_builder.get_object(field_name).get())
            except Exception as e:
                self.logger.exception('failed to extract the value of field {} due to {}'.format(field_name, e))

        for k in custom_ep_dict.keys():
            custom_ep_dict[k] = extract_val(k)

        custom_gw_commands = []
        if custom_ep_dict['scan_ch'] is not None:
            custom_gw_commands.append('!scan_ch {} 37'.format(custom_ep_dict['scan_ch']))

        if custom_ep_dict['period_2_4'] is not None:
            custom_gw_commands.append('!set_2_4_ghz_time_period {}'.format(custom_ep_dict['period_2_4']))

        if custom_ep_dict['beacon_2_4_duration'] is not None and custom_ep_dict['beacon_2_4_frequencies'] is not None:
            cmd = '!set_beacons_pattern {} {}'.format(custom_ep_dict['beacon_2_4_duration'],
                                                      len(custom_ep_dict['beacon_2_4_frequencies']))
            for f in custom_ep_dict['beacon_2_4_frequencies']:
                cmd += ' {}'.format(f)
            if custom_ep_dict['beacon_to_beacon'] is not None:
                cmd += ' {}'.format(custom_ep_dict['beacon_to_beacon'])
                if custom_ep_dict['beacon_to_energy'] is not None:
                    cmd += ' {}'.format(custom_ep_dict['beacon_to_energy'])
            custom_gw_commands.append(cmd)

        if custom_ep_dict['beacon_2_4_power'] is not None:
            custom_gw_commands.append('!beacons_backoff {}'.format(valid_output_power_vals[-1]['abs_power'] -
                                                                   custom_ep_dict['beacon_2_4_power']))

        if custom_ep_dict['energy_2_4_frequencies'] is not None \
                and custom_ep_dict['energy_sub1g_frequencies'] is not None:
            cmd = '!set_dyn_energizing_pattern 6 {} {}'.format(len(custom_ep_dict['energy_sub1g_frequencies']) > 0,
                                                               len(custom_ep_dict['energy_2_4_frequencies']))
            for f in custom_ep_dict['energy_2_4_frequencies']:
                cmd += ' {}'.format(f)
            if custom_ep_dict['energy_2_4_duration'] is not None:
                cmd += ' {}'.format(custom_ep_dict['energy_2_4_duration'])
            custom_gw_commands.append(cmd)

        if custom_ep_dict['energy_2_4_power'] is not None:
            abs_output_power_index = self.energy_power_2_4.index(custom_ep_dict['energy_2_4_power'])
            custom_gw_commands.append(
                '!bypass_pa {}'.format(valid_output_power_vals[abs_output_power_index]['bypass_pa']))
            custom_gw_commands.append(
                '!output_power {}'.format(valid_output_power_vals[abs_output_power_index]['gw_output_power']))

        if custom_ep_dict['period_sub1g'] is not None:
            custom_gw_commands.append('!set_sub_1_ghz_time_period {}'.format(custom_ep_dict['period_sub1g']))

        if custom_ep_dict['energy_sub1g_frequencies'] is not None:
            cmd = '!set_sub_1_ghz_energy_params {}'.format(len(custom_ep_dict['energy_sub1g_frequencies']))
            for f in custom_ep_dict['energy_sub1g_frequencies']:
                cmd += ' {}'.format(f)
            if custom_ep_dict['energy_sub1g_duration'] is not None:
                cmd += '{}'.format(custom_ep_dict['energy_sub1g_duration'])
            custom_gw_commands.append(cmd)

        if custom_ep_dict['energy_sub1g_power'] is not None:
            custom_gw_commands.append('!set_sub_1_ghz_power {}'.format(custom_ep_dict['energy_sub1g_power']))

        custom_gw_commands.append('!gateway_app')
        # send gw commands:
        for cmd in custom_gw_commands:
            rsp = self.gw_obj.write(cmd, with_ack=True)
            self.print_func('time: {}, command:{}, response:{}'.format(rsp['time'], cmd, rsp['raw']))

        self.close_requested = True
        pass

    def on_cancel_custom_ep(self):
        self.close_requested = True

    def periodic_call(self):
        if not self.close_requested:
            self.ttk_ep.after(500, self.periodic_call)

        else:
            print("Destroying Custom EP GUI at:", time.time())
            try:
                self.ttk_ep.destroy()
            except Exception as e:
                self.logger.exception('problem occured during exit the gui: {}'.format(e))
                exit(1)

    def close_window(self):
        self.close_requested = True
        print("User requested close at:", time.time())


class CustomPlotGui(object):

    def __init__(self, plot_config=None, print_func=None, tk_frame=None, logger=None):
        self.close_requested = False
        self.logger = logger if logger is not None else logging.getLogger('root')
        if print_func is None:
            self.print_func = print
        else:
            self.print_func = print_func
        if plot_config is None:
            self.plot_config = None
        else:
            self.plot_config = plot_config
        self.plot_builder = pygubu.Builder()
        plots_ui_file = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils'),
                                     'custom_plots.ui')
        self.plot_builder.add_from_file(plots_ui_file)
        if tk_frame:
            self.ttk_plots = tk_frame
        else:
            self.ttk_plots = Tk()

        self.ttk_plots.title('Wiliot Custom plots')
        self.custom_plots_window = self.plot_builder.get_object('custom_plots_window', self.ttk_plots)
        self.plot_builder.connect_callbacks(self)

        # update ui
        self.plot_builder.get_variable('summary_cb_state').set(self.plot_config.plot_files.get('summary', True))
        self.plot_builder.get_variable('tags_detailed_cb_state').set(
            self.plot_config.plot_files.get('tags_detailed', True))

        self.plot_builder.get_variable('analysis_plot_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('analysis_plot', True))
        self.plot_builder.get_variable('rx_tx_intervals_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('rx_tx_intervals', True))
        self.plot_builder.get_variable('wkup_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('wkup_metrics', True))
        self.plot_builder.get_variable('aux_meas_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('aux_meas_metrics', True))
        self.plot_builder.get_variable('lo_dco_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('lo_dco_metrics', True))
        self.plot_builder.get_variable('sprinkler_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('sprinkler_metrics', True))
        self.plot_builder.get_variable('sym_dco_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('sym_dco_metrics', True))
        self.plot_builder.get_variable('sensing_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('sensing_metrics', True))
        self.plot_builder.get_variable('temp_comp_and_tuning_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('temp_comp_and_tuning', True))

        # self.ttk_plots.lift()
        # self.ttk_plots.attributes("-topmost", True)

        self.ttk_plots.protocol("WM_DELETE_WINDOW", self.close_window)
        self.ttk_plots.after_idle(self.periodic_call)
        self.ttk_plots.mainloop()

    def on_set_custom_plot(self):
        self.plot_config.plot_files['summary'] = self.plot_builder.get_variable('summary_cb_state').get()
        self.plot_config.plot_files['tags_detailed'] = self.plot_builder.get_variable('tags_detailed_cb_state').get()

        self.plot_config.detailed_tag_graphs['analysis_plot'] = self.plot_builder.get_variable(
            'analysis_plot_cb_state').get()
        self.plot_config.detailed_tag_graphs['rx_tx_intervals'] = self.plot_builder.get_variable(
            'rx_tx_intervals_cb_state').get()
        self.plot_config.detailed_tag_graphs['wkup_metrics'] = self.plot_builder.get_variable(
            'wkup_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['aux_meas_metrics'] = self.plot_builder.get_variable(
            'aux_meas_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['lo_dco_metrics'] = self.plot_builder.get_variable(
            'lo_dco_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['sprinkler_metrics'] = self.plot_builder.get_variable(
            'sprinkler_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['sym_dco_metrics'] = self.plot_builder.get_variable(
            'sym_dco_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['sensing_metrics'] = self.plot_builder.get_variable(
            'sensing_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['temp_comp_and_tuning'] = self.plot_builder.get_variable(
            'temp_comp_and_tuning_cb_state').get()

        self.close_requested = True
        pass

    def on_cancel_custom_plot(self):
        self.close_requested = True

    def periodic_call(self):
        if not self.close_requested:
            self.ttk_plots.after(500, self.periodic_call)

        else:
            print("Destroying Custom EP GUI at:", time.time())
            try:
                self.ttk_plots.destroy()
            except Exception as e:
                self.logger.exception('problem occured during exit the gui: {}'.format(e))
                exit(1)

    def close_window(self):
        self.close_requested = True
        print("User requested close at:", time.time())


if __name__ == '__main__':
    # Run the UI
    GWApp = GatewayUI()
    # CustomPlotGui(plot_config=plot_config())
