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
"""
Calculating Yield fraction by the following steps (with elaboration):
1)Counting the unique advas in AdvaProcess class
2)Counting number of tags in CountThread
3)Creating two threads in MultiThreadingCalculation in order to run AdvaProcess instance and CountThread instance
at the same time
4)Calculating the Yield fraction according to the results we got from the instances
5)Creating two threads in MainWindow class in order to calculate the fraction by MultiThreadingCalculation instance
and to run the GUI function (open_session) at the same time.
"""
import sys
import pandas as pd
from wiliot_core import *
from wiliot_testers.test_equipment import YoctoSensor
from configs.inlay_data import csv_dictionary
from wiliot_testers.utils.get_version import get_version
from wiliot_testers.utils.upload_to_cloud_api import upload_to_cloud_api
import serial
from wiliot_testers.tester_utils import dict_to_csv
import logging
import threading
import time
import datetime
import matplotlib
import serial.tools.list_ports
import PySimpleGUI as sg
import platform

SET_VALUE_MORE_THAN_100 = 110
VALUE_WHEN_NO_SENSOR = -10000
PACKET_DATA_FEATURES_TITLE = [
    'raw_packet', 'adv_address', 'decrypted_packet_type', 'group_id',
    'flow_ver', 'test_mode', 'en', 'type', 'data_uid', 'nonce', 'enc_uid',
    'mic', 'enc_payload', 'gw_packet', 'rssi', 'stat_param', 'time_from_start',
    'counter_tag', 'is_valid_tag_packet', 'gw_process', 'is_valid_packet', 'inlay_type'
]

matplotlib.use('TkAgg')
inlay_types_dict = {item.name: item.value for item in InlayTypes}
today = datetime.date.today()
formatted_today = today.strftime("%Y%m%d")  # without -
formatted_date = today.strftime("%Y-%m-%d")
current_time = datetime.datetime.now()
cur_time_formatted = current_time.strftime("%I%M%S")  # without :
time_formatted = current_time.strftime("%I:%M:%S")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
root_logger = logging.getLogger()

for handler in root_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setLevel(logging.INFO)


class AdvaProcess(object):
    """
    Counting the number of unique advas
    """

    def __init__(self, stop_event, received_channel, time_profile_val, energy_pattern_val, inlay_type, logging_file,
                 advas_before_tags, listener_path):
        self.gw_instance = None
        self.logger_file = logging_file
        self.init_gw(listener_path)
        self.all_tags = Queue()
        self.advas_before_tags = advas_before_tags
        self.stop = stop_event
        self.received_channel = received_channel
        try:
            self.time_profile_val = [int(time_pr) for time_pr in time_profile_val]
        except Exception as ee:
            raise Exception(f'could not retireive time profile from inlay_data value for {inlay_type}.\n'
                            f'time profile should be x,y but was {time_profile_val} [{ee}]')
        self.energy_pattern_val = energy_pattern_val
        self.gw_reset_config()
        self.inlay_type = inlay_type

    def init_gw(self, listener_path):

        try:
            self.gw_instance = WiliotGateway(auto_connect=True, logger_name='yield', is_multi_processes=sys.platform != "darwin",
                                             log_dir_for_multi_processes=listener_path)
            is_connected, _, _ = self.gw_instance.get_connection_status()
            if is_connected:
                self.gw_instance.start_continuous_listener()
                self.gw_instance.reset_gw()
                time.sleep(2)
            else:
                self.logger_file.warning("Couldn't connect to GW in main thread")
        except Exception as ee:
            self.gw_instance = None
            self.logger_file.warning(f"Couldn't connect to GW in main thread, error: {ee}")

    def gw_reset_config(self):
        """
        Configs the gateway
        """
        if self.gw_instance.connected:
            self.gw_instance.reset_gw(reset_port=False)
            self.gw_instance.reset_listener()
            time.sleep(2)
            if not self.gw_instance.is_gw_alive():
                self.logger_file.warning('gw_reset_and_config: gw did not respond')
                raise Exception('gw_reset_and_config: gw did not respond after rest')
            self.gw_instance.config_gw(received_channel=self.received_channel, time_profile_val=self.time_profile_val,
                                       energy_pattern_val=self.energy_pattern_val,
                                       start_gw_app=False, with_ack=True,
                                       effective_output_power_val=22, sub1g_output_power_val=29)
        else:
            raise Exception('Could NOT connect to GW')

    def run(self):
        """
        Receives available data then counts and returns the number of unique advas
        """
        self.gw_instance.config_gw(start_gw_app=True)
        while not self.stop.is_set():
            time.sleep(0)
            if self.gw_instance.is_data_available():
                raw_packets_in = self.gw_instance.get_packets(action_type=ActionType.ALL_SAMPLE, data_type=DataType.RAW,
                                                              tag_inlay=self.inlay_type)
                self.all_tags.put(raw_packets_in)
            else:
                time.sleep(0.050)
                continue
            if not self.gw_instance.is_connected():
                self.logger_file.info('GW was disconnected. trying to initiate connection...')
            if self.gw_instance.get_read_error_status():
                self.logger_file.info('A GW reading Error was detected')

        self.gw_instance.exit_gw_api()

    def get_raw_packets_queue(self):
        """
        Returns the packet queue that is created above
        """
        return self.all_tags


class CountThread(object):
    """
    Counting the number of tags
    """

    def __init__(self, stop_event, logger_file, rows=1, max_movement_time=3, ther_cols=1):
        self.max_movement_time = max_movement_time
        self.logger_file = logger_file
        self.available_ports = [s.device for s in serial.tools.list_ports.comports()]
        self.get_ports_of_arduino()
        self.baud = 1000000
        self.ports = self.get_ports_of_arduino()
        try:
            self.comPortObj = serial.Serial(self.ports[0], self.baud, timeout=0.1)
            time.sleep(1)
            self.config()
        except serial.SerialException:
            self.logger_file.error("NO ARDUINO")
            raise Exception('could not connect to the Arduino')
        self.rows = rows
        self.ther_cols = ther_cols
        self.stop = stop_event
        self.tested = 0

    def config(self):
        """
        @return:
        @rtype:
        """
        self.comPortObj.write(f'*time_btwn_triggers {int(self.max_movement_time)}'.encode())
        rsp = self.comPortObj.readline()
        if rsp == b'' or rsp != b'No pulses yet...\r\n':
            raise Exception('A problem in the first message of Arduino')
        for i in range(5):
            time.sleep(0.500)
            rsp = self.comPortObj.readline()
            if rsp.decode() == f'Max movement time was set to {int(self.max_movement_time)}[sec]\r\n':
                self.logger_file.info(f'config Arduino and got the following msg: {rsp.decode()}')
                return
        raise Exception('Arduino Configuration was failed')

    def get_ports_of_arduino(self):
        """
        Gets all the ports we have, then chooses Arduino's ports
        """
        arduino_ports = []
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                arduino_ports.append(p.device)
        if not arduino_ports:
            self.logger_file.info('NO ARDUINO')
        return arduino_ports

    def run(self):
        """
        Tries to read data and then counts the number of tags
        """
        while not self.stop.is_set():
            time.sleep(0.100)
            data = ''
            try:
                data = self.comPortObj.readline()
            except Exception as ee:
                self.logger_file.error(f"NO READLINE: {ee}")
            if data.__len__() > 0:
                try:
                    tmp = data.decode().strip(' \t\n\r')
                    if "pulses detected" in tmp:
                        self.tested += (self.rows * int(self.ther_cols))

                except Exception as ee:
                    self.logger_file.error(f'Warning: Could not decode counter data or Warning: {ee}')
                    continue
        self.comPortObj.close()

    def get_tested(self):
        """
        returns the number of tags
        """
        return self.tested


class MainWindow:
    """
    The main class the runs the GUI and supervise the multi-threading process of fraction's calculation and GUI viewing
    """

    def __init__(self):

        self.latest_yield_value = None
        self.latest_yield_formatted = 0
        self.number_of_unique_advas = None
        self.all_tag_coll = TagCollection()
        self.start_run = None
        self.inlay_select = None
        self.energy_pat = None
        self.time_pro = None
        self.rec_channel = None
        self.temperature = VALUE_WHEN_NO_SENSOR
        self.humidity = VALUE_WHEN_NO_SENSOR
        self.light_intensity = VALUE_WHEN_NO_SENSOR
        self.ttfp = None
        self.cnt = None
        self.curr_adva_for_log = None
        self.matrix_tags = None
        self.logger = None
        self.conversion = None
        self.surface = None
        self.matrix_sec = None
        self.adva_process = None
        self.adva_process_thread = None
        self.count_process = None
        self.count_process_thread = None
        self.folder_path = None
        self.py_wiliot_version = None
        self.final_path_run_data = None
        self.run_data_dict = None
        self.tags_num = 0
        self.last_printed = 0
        self.stop = threading.Event()
        self.neg_col = 0
        self.thermodes_col = None
        self.print_neg_advas = False
        self.selected = ''
        self.wafer_lot = ''
        self.wafer_number = ''
        self.operator = ''
        self.tester_type = 'yield-test'
        self.tester_station_name = ''
        self.comments = ''
        self.gw_energy_pattern = None
        self.gw_time_profile = None
        self.rows_number = 1
        self.upload_flag = True
        self.cmn = ''
        self.final_path_packets_data = ''
        self.seen_advas = set()
        self.not_neg_advas = 0  # used only to be shown in the small window
        self.update_packet_data_flag = False
        self.first_time_between_0_and_100 = False
        self.tags_counter_time_log = 0
        self.advas_before_tags = set()
        try:
            self.main_sensor = YoctoSensor(self.logger)
        except Exception as ee:
            self.main_sensor = None
            print(f'No sensor is connected ({ee}')

    def get_result(self):
        """
        Calculates the yield fraction
        """
        result = 100
        tags_num = self.count_process.get_tested()
        if tags_num > 0:
            result = (self.not_neg_advas / tags_num) * 100
        return result

    def run(self):
        """
        Viewing the window and checking if the process stops
        """
        self.open_session()
        if self.start_run:
            self.init_processes(self.rec_channel, self.time_pro, self.energy_pat, self.inlay_select, self.matrix_sec)
            time.sleep(0.5)
            self.init_run_data()
            self.start_processes()
            self.overlay_window()
        else:
            self.logger.warning('Error Loading Program')

    def init_file_path(self):
        self.py_wiliot_version = get_version()
        d = WiliotDir()
        d.create_tester_dir(tester_name='yield_tester')
        yield_test_app_data = d.get_tester_dir('yield_tester')
        self.cmn = self.wafer_lot + '.' + self.wafer_number
        run_path = os.path.join(yield_test_app_data, self.cmn)
        if not os.path.exists(run_path):
            os.makedirs(run_path)
        self.cmn = self.wafer_lot + '.' + self.wafer_number + '_' + formatted_today + '_' + cur_time_formatted
        self.folder_path = os.path.join(run_path, self.cmn)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def init_run_data(self):
        self.final_path_run_data = os.path.join(self.folder_path, self.cmn + '@run_data.csv')
        gw_version = self.adva_process.gw_instance.get_gw_version()[0]
        start_time = datetime.datetime.now()
        run_start_time = start_time.strftime("%I:%M:%S")
        value = csv_dictionary[self.selected]
        self.run_data_dict = {'common_run_name': self.cmn, 'tester_station_name': self.tester_station_name,
                              'operator': self.operator, 'received_channel': value['received_channel'],
                              'run_start_time': formatted_date + ' ' + run_start_time, 'run_end_time': '',
                              'wafer_lot': self.wafer_lot, 'wafer_number': self.wafer_number,
                              'tester_type': self.tester_type, 'energy_pattern_val': value['energy_pattern_val'],
                              'comments': self.comments, 'inlay': self.selected, 'total_run_tested': 0,
                              'total_run_responding_tags': 0, 'conversion_type': self.conversion,
                              'gw_version': gw_version, 'surface': self.surface, 'matrix_tags': self.matrix_tags,
                              'py_wiliot_version': self.py_wiliot_version, 'thermodes_col': self.thermodes_col,
                              'gw_time_profile': self.gw_time_profile, 'gw_energy_pattern': self.gw_energy_pattern,
                              'rows_number': self.rows_number, 'upload_date': formatted_date + ' ' + time_formatted,
                              'time_profile_val': value['time_profile_val']}

    @staticmethod
    def update_run_data_file(run_data_path, run_data_dict, run_end_time, tags_num, advas, result, conversion, surface):
        """
        Updates the run_data CSV file while running the program
        """
        run_data_dict['run_end_time'] = run_end_time
        run_data_dict['total_run_tested'] = tags_num
        run_data_dict['total_run_responding_tags'] = advas
        run_data_dict['yield'] = result
        run_data_dict['conversion_type'] = conversion
        run_data_dict['surface'] = surface
        dict_to_csv(dict_in=run_data_dict, path=run_data_path)

    def update_packet_data(self):
        """
        Updates the run_data CSV file while running the program
        """

        raw_packet_queue = self.adva_process.get_raw_packets_queue()

        self.number_of_unique_advas = len(self.seen_advas)

        if not raw_packet_queue.empty():
            cur_p_df = pd.DataFrame()
            # Collecting Packets from the queue and putting them into a TagCollection
            for _ in range(raw_packet_queue.qsize()):
                for p in raw_packet_queue.get():
                    cur_p = Packet(p['raw'])
                    self.all_tag_coll.append(cur_p)

            # passing all over the PacketLists in TagCollection
            for tag_id, tag_packet_list in self.all_tag_coll.tags.items():
                if tag_id not in self.seen_advas and tag_id not in self.advas_before_tags:
                    packet_list_df = tag_packet_list.get_df()
                    if not packet_list_df.empty:
                        first_row = packet_list_df.iloc[[0]]
                        cur_p_df = pd.concat([cur_p_df, first_row], ignore_index=True)
                    self.seen_advas.add(tag_id)
            if not self.update_packet_data_flag:
                # Initializing the packets_data file
                try:
                    for col in PACKET_DATA_FEATURES_TITLE:
                        cur_p_df.insert(loc=len(cur_p_df.columns), column=col, value='')
                    cur_p_df.insert(loc=len(cur_p_df.columns), column='common_run_name', value=self.cmn)
                    cur_p_df.insert(loc=len(cur_p_df.columns), column='matrix_tags_location', value=self.cnt)
                    cur_p_df.insert(loc=len(cur_p_df.columns), column='tag_matrix_ttfp', value=self.ttfp)
                    cur_p_df.insert(loc=len(cur_p_df.columns), column='environment_light_intensity',
                                    value=self.light_intensity)
                    cur_p_df.insert(loc=len(cur_p_df.columns), column='environment_humidity', value=self.humidity)
                    cur_p_df.insert(loc=len(cur_p_df.columns), column='environment_temperature', value=self.temperature)
                    self.final_path_packets_data = os.path.join(self.folder_path, self.cmn + '@packets_data.csv')
                    cur_p_df.to_csv(self.final_path_packets_data, index=False)
                    self.update_packet_data_flag = True
                except Exception as ee:
                    self.logger.error(f"Exception occurred: {ee}")
            else:
                # updating packets_data_file
                cur_p_df.insert(loc=len(cur_p_df.columns), column='common_run_name', value=self.cmn)
                cur_p_df.insert(loc=len(cur_p_df.columns), column='matrix_tags_location', value=self.cnt)
                cur_p_df.insert(loc=len(cur_p_df.columns), column='tag_matrix_ttfp', value=self.ttfp)
                cur_p_df.insert(loc=len(cur_p_df.columns), column='environment_light_intensity', value=self.light_intensity)
                cur_p_df.insert(loc=len(cur_p_df.columns), column='environment_humidity', value=self.humidity)
                cur_p_df.insert(loc=len(cur_p_df.columns), column='environment_temperature', value=self.temperature)
                cur_p_df.to_csv(self.final_path_packets_data, mode='a', index=False, header=False)

    def stop_button(self, window, run_end_time, tags_num, advas, result):
        """
        Finishing the program and saves the last changes after pressing Stop in the second window
        """
        import matplotlib.pyplot as plt
        self.stop.set()
        window.close()
        plt.close()
        self.adva_process_thread.join()
        self.count_process_thread.join()

        self.update_run_data_file(self.final_path_run_data, self.run_data_dict, formatted_date + ' ' + run_end_time,
                                  tags_num, advas, result, self.conversion, self.surface)
        self.update_packet_data()

        if self.upload_flag:
            try:
                is_uploaded = upload_to_cloud_api(self.cmn, self.tester_type,
                                                  run_data_csv_name=self.final_path_run_data,
                                                  packets_data_csv_name=self.final_path_packets_data,
                                                  env='test', is_path=True)

            except Exception as ee:
                self.logger.error(f"Exception occurred: {ee}")
                is_uploaded = False

            if is_uploaded:
                self.logger.info("Successful upload")
            else:
                sg.popup_ok(
                    "Run upload failed. Check exception error at the console and check Internet connection is available"
                    " and upload logs manually", title='Upload Error', font='Calibri', keep_on_top=True,
                    auto_close=False, no_titlebar=True)

    def init_processes(self, rec_channel, time_pro, energy_pat, inlay_select, max_movement_time):
        """
        Initializing the two main instances and threads in order to start working
        """
        self.adva_process = AdvaProcess(self.stop, rec_channel, time_pro, energy_pat,
                                        inlay_select, self.logger,
                                        self.advas_before_tags, self.folder_path)
        self.adva_process_thread = threading.Thread(target=self.adva_process.run, args=())
        self.count_process = CountThread(self.stop, self.logger, self.rows_number, max_movement_time,
                                         self.thermodes_col)
        self.count_process_thread = threading.Thread(target=self.count_process.run, args=())

    def start_processes(self):
        """
        Starting the work of the both threads
        """
        self.adva_process_thread.start()
        self.count_process_thread.start()

    def overlay_window(self):
        """
        The small window open session
        """
        import matplotlib.pyplot as plt
        yes_or_no = ['Yes', 'No']
        layout = [
            [sg.Text('Number of tags:', font=4), sg.Text(key='num_rows', font=4)],
            [sg.Text('Number of advas:', font=4), sg.Text(key='num_advas', font=4)],
            [sg.Text('Do you want to stop or upload?')],
            [sg.Button('Stop'), [sg.Text('Upload:', font=6)],
             [sg.Combo(values=yes_or_no, default_value=yes_or_no[0], key='upload', font=4, enable_events=True)]],
            [sg.Canvas(key='-CANVAS-', size=(10, 100))],
        ]

        sub = False
        window = sg.Window('Upload CSV files', layout, modal=True, finalize=True, location=(870, 200))

        # initialize num_advas and num_rows
        num_rows_text_elem = window['num_rows']
        num_advas_text_elem = window['num_advas']
        num_rows = (self.rows_number * self.neg_col)
        num_advas = 0
        num_rows_text_elem.update(f"{num_rows}")
        num_advas_text_elem.update(f"{num_advas}")

        # initialize the first graph
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['red'])
        fig, ax = plt.subplots()
        ax.set_xlabel('Number of tags')
        ax.set_ylabel('Yield %')
        ax.set_ylim([-2, 112])
        plt.ion()
        manager = plt.get_current_fig_manager()
        manager.window.wm_geometry("-100-100")
        plt.show()
        prev_tests = 0
        prev_val = 100
        text_box = ax.text(0.68, 1.05, f"Current Matrix Yield: {self.latest_yield_formatted:.2f} %",
                           transform=ax.transAxes)

        # initialize the second graph
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['red'])
        fig, axy = plt.subplots()
        axy.set_xlabel('Number of tags')
        axy.set_ylabel('Yield %')
        axy.set_ylim([-2, 112])
        plt.ion()
        manager1 = plt.get_current_fig_manager()
        manager1.window.wm_geometry("+1000+1000")
        plt.show()
        prev_tests1 = 0
        prev_val1 = 100
        text_box1 = axy.text(0.68, 1.05, f"Cumulative Yield: {prev_val:.2f} %", transform=axy.transAxes)

        self.neg_advas = len(self.seen_advas)
        self.curr_adva_for_log = len(self.seen_advas)
        self.cnt = 1
        while True:

            event, values = window.read(timeout=100)
            new_num_rows = self.count_process.get_tested() + (self.rows_number * self.neg_col)
            new_num_advas = len(self.seen_advas) - self.neg_advas
            self.not_neg_advas = new_num_advas

            # updating number of rows in GUI
            if new_num_rows != num_rows:
                num_rows = new_num_rows
                num_rows_text_elem.update(f"{num_rows}")

            # updating number of advas in GUI
            if new_num_advas != num_advas and new_num_advas > -1:
                num_advas = new_num_advas
                num_advas_text_elem.update(f"{num_advas}")
            matrix_size = int(self.thermodes_col) * int(self.rows_number)

            # ignoring all advas before receiving the first arduino trigger
            while new_num_rows < matrix_size + (self.rows_number * self.neg_col):
                if self.adva_process.gw_instance.is_data_available():
                    packet_list_in = self.adva_process.gw_instance.get_packets(action_type=ActionType.ALL_SAMPLE,
                                                                               tag_inlay=self.adva_process.inlay_type)
                    for packet in packet_list_in:
                        adva = packet.get_adva()
                        self.adva_process.advas_before_tags.add(adva)
                self.not_neg_advas = 0
                new_num_rows = self.count_process.get_tested() + (self.rows_number * self.neg_col)
                if not new_num_rows < matrix_size + (self.rows_number * self.neg_col):
                    self.print_neg_advas = True
                continue

            # writing the number of neglected advas in LOG
            if self.print_neg_advas:
                self.logger.info('neglected advas:  %05d', len(self.advas_before_tags))
                self.print_neg_advas = False
            # all processes when getting a new matrix
            if self.count_process.get_tested() % matrix_size == 0 and self.count_process.get_tested() != self.last_printed:
                first_moment_new_num_rows = self.count_process.get_tested()
                if self.main_sensor:
                    self.light_intensity = self.main_sensor.get_light()
                    self.humidity = self.main_sensor.get_humidity()
                    self.temperature = self.main_sensor.get_temperature()

                yield_result = "%.5f" % self.get_result()
                latest_adva = len(self.seen_advas) - self.curr_adva_for_log
                self.latest_yield_value = float(latest_adva / matrix_size) * 100
                self.latest_yield_formatted = "{:.5f}".format(self.latest_yield_value).zfill(9)
                text_box.set_text(f"Current Matrix Yield : {self.latest_yield_value:.2f} %")
                if '.' in yield_result and len(yield_result.split('.')[0]) < 2:
                    yield_result = "0" + yield_result
                latest_adva = len(self.seen_advas) - self.curr_adva_for_log
                self.latest_yield_formatted = "{:.5f}".format(float(latest_adva / matrix_size) * 100).zfill(9)

                self.logger.info(
                    'Matrix Number: %05d, Cumulative Yield: %s, Cumulative Tags: %05d, Cumulative Advas: %05d,'
                    'Latest Yield: %s, Latest Tags: %05d, Latest Advas: %05d, Light Intensity: '
                    '%05.1f, Humidity: %05.1f, Temperature: %05.1f', self.cnt, yield_result,
                    self.count_process.get_tested(), len(self.seen_advas), self.latest_yield_formatted,
                    matrix_size, latest_adva, self.light_intensity, self.humidity, self.temperature)

                # updating the first graph
                curr_tests = new_num_rows
                curr_val = 100 * ((len(self.seen_advas) - self.curr_adva_for_log) / matrix_size)
                if curr_val > 100:
                    curr_val = SET_VALUE_MORE_THAN_100
                self.curr_adva_for_log = len(self.seen_advas)
                ax.plot([prev_tests, curr_tests], [prev_val, curr_val], color='red')
                prev_tests = curr_tests
                prev_val = curr_val
                self.last_printed = first_moment_new_num_rows
                self.cnt += 1
            # update packet data
            self.update_packet_data()

            # updating the second graph
            curr_tests1 = new_num_rows
            curr_val1 = self.get_result()
            if curr_val1 > 100:
                curr_val1 = SET_VALUE_MORE_THAN_100
            elif 0 < curr_val1 < 101:
                self.first_time_between_0_and_100 = True
            if new_num_rows != 0 and self.first_time_between_0_and_100:
                axy.plot([prev_tests1, curr_tests1], [prev_val1, curr_val1], color='red')
            prev_tests1 = curr_tests1
            prev_val1 = curr_val1
            text_box1.set_text(f"Comulitive Yield : {curr_val1:.2f} %")

            # updating run_data_file
            end_time = datetime.datetime.now()
            run_end_time = end_time.strftime("%I:%M:%S")
            advas = len(self.seen_advas)
            tags_num = self.count_process.get_tested()
            result = float(100 * (advas / tags_num)) if tags_num != 0 else float('inf')
            self.update_run_data_file(self.final_path_run_data, self.run_data_dict, formatted_date + ' ' + run_end_time,
                                      tags_num, advas, result, self.conversion, self.surface)

            if event == sg.WIN_CLOSED or event in ('Stop', 'upload'):
                if event == 'upload':
                    if values['upload'] == 'No':
                        self.upload_flag = False
                    else:
                        self.upload_flag = True  # if we press No then yes
                if event == 'Stop':
                    self.logger.info('Final Yield: %s, Final Tags: %05d, Final Advas: %05d,',
                                     result, self.count_process.get_tested(), len(self.seen_advas), )
                    self.stop_button(window, run_end_time, tags_num, advas, result)
                    sub = True
                    break
                if sub:
                    break

        return sub

    def open_session(self):
        """
        opening a session for the process
        """
        # save data to configs file
        if os.path.exists("configs/gui_input_do_not_delete.json"):
            with open("configs/gui_input_do_not_delete.json", "r") as f:
                previous_input = json.load(f)

        else:
            previous_input = {'inlay': '', 'number': '', 'received_channel': '',
                              'energy_pattern_val': '', 'time_profile_val': '', 'tester_station_name': '',
                              'comments': '', 'operator': '', 'wafer_lot': '', 'wafer_num': '', 'conversion_type': '',
                              'surface': '', 'matrix_tags': '', 'thermodes_col': '', 'gw_energy_pattern': '',
                              'gw_time_profile': '', 'rows_number': '', 'matrix_sec': ''}
        # update fields from configs
        self.start_run = False
        selected_inlay = csv_dictionary[previous_input['inlay']]
        energy_pat = selected_inlay['energy_pattern_val']
        time_pro = selected_inlay['time_profile_val']
        rec_channel = selected_inlay['received_channel']
        lst_inlay_options = list(inlay_types_dict.keys())
        conv_opts = ['Not converted', 'Standard', 'Durable']
        surfaces = ['Air', 'Cardboard', 'RPC', 'General Er3', 'General Er3.5']
        layout = [
            [sg.Text('Wafer Lot:', size=(13, 1), font=4),
             sg.InputText(previous_input['wafer_lot'], key='wafer_lot', font=4),
             sg.Text('Wafer Number:', size=(13, 1), font=4),
             sg.InputText(previous_input['wafer_num'], key='wafer_num', font=4)],

            [
             sg.Text('Time of matrix:', size=(13, 1), font=4),
             sg.InputText(previous_input['matrix_sec'], key='matrix_sec', font=4)],

            [sg.Text('Thermode Col:', size=(13, 1), font=4),
             sg.InputText(previous_input['thermodes_col'], key='thermodes_col', font=4, enable_events=True),
             sg.Text('Rows Number :', size=(13, 1), font=4),
             sg.InputText(previous_input['rows_number'], key='rows_number', font=4, enable_events=True)],

            [sg.Text('Matrix tags: ', size=(13, 1), font=4),
             sg.Text(key='matrix_tags', font=4)],

            [sg.Text('Inlay:', size=(13, 1), font=4),
             sg.Combo(values=lst_inlay_options, default_value=previous_input['inlay'], key='inlay', font=4,
                      enable_events=True), sg.Text('Energy Pattern:', font=4),
             sg.Text(energy_pat, key='energy_pattern_val', font=4),
             sg.Text('Time Profile:', font=4), sg.Text(time_pro, key='time_profile_val', font=4),
             sg.Text('Received Channel:', font=4), sg.Text(rec_channel, key='received_channel', font=4)],

            [sg.Text('Tester Station:', size=(13, 1), font=4),
             sg.InputText(previous_input['tester_station_name'], key='tester_station_name', font=4),
             sg.Text('Comments:', size=(13, 1), font=4),
             sg.InputText(previous_input['comments'], key='comments', font=4)],

            [sg.Text('Operator:', size=(13, 1), font=4),
             sg.InputText(previous_input['operator'], key='operator', font=4),
             sg.Text('Conversion:', size=(13, 1), font=4),
             sg.Combo(values=conv_opts, default_value=previous_input['conversion_type'], key='conversion_type', font=4,
                      enable_events=True), sg.Text('Surface:', font=4),
             sg.Combo(values=surfaces, default_value=previous_input['surface'], key='surface', font=4,
                      enable_events=True)],

            [sg.Submit()]
        ]

        window = sg.Window('WILIOT Yield Tester', layout, finalize=True)

        while True:
            event, values = window.read(timeout=100)
            inlay_select = values['inlay']
            self.selected = values['inlay']
            if event == 'inlay':
                inlay_select = values['inlay']
                self.selected = values['inlay']

                if inlay_select in csv_dictionary:
                    selected_inlay = csv_dictionary[inlay_select]
                    energy_pat = selected_inlay['energy_pattern_val']
                    time_pro = selected_inlay['time_profile_val']
                    rec_channel = selected_inlay['received_channel']

                else:
                    energy_pat = 'Invalid Selection'
                    time_pro = 'Invalid Selection'
                    rec_channel = 'Invalid Selection'

                window.find_element('rows_number').Update(value=self.rows_number)
                window.find_element('energy_pattern_val').Update(value=energy_pat)
                window.find_element('time_profile_val').Update(value=time_pro)
                window.find_element('received_channel').Update(value=rec_channel)
            if event == 'Submit':
                self.matrix_sec = (values['matrix_sec'])
                self.wafer_lot = values['wafer_lot']
                self.wafer_number = values['wafer_num']
                self.comments = values['comments']
                self.rows_number = int(values['rows_number'])
                self.gw_energy_pattern = energy_pat
                self.gw_time_profile = time_pro
                self.matrix_tags = str(int(values['thermodes_col']) * int(values['rows_number']))
                self.thermodes_col = values['thermodes_col']
                self.conversion = values['conversion_type']
                self.surface = values['surface']
                self.tester_station_name = values['tester_station_name']
                self.operator = values['operator']
                self.init_file_path()

                # Logger setup
                self.logger = logging.getLogger('yield')
                if self.logger.hasHandlers():
                    self.logger.handlers.clear()
                self.logger.setLevel(logging.INFO)
                final_path_log_file = os.path.join(self.folder_path, self.cmn + '@yield_log.log')
                file_handler = logging.FileHandler(final_path_log_file)
                file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
                file_handler.setLevel(logging.INFO)
                self.logger.addHandler(file_handler)
                self.rec_channel, self.time_pro, self.energy_pat, self.inlay_select = \
                    rec_channel, time_pro, energy_pat, inlay_select
                # starting the main run
                self.start_run = True
                with open("configs/gui_input_do_not_delete.json", "w") as f:
                    json.dump(values, f)
                break
            elif event == 'thermodes_col' or event == 'rows_number':
                try:
                    matrix_size = int(values['thermodes_col']) * int(values['rows_number'])
                    window['matrix_tags'].update(str(matrix_size))
                except ValueError:
                    window['matrix_tags'].update('')

            elif event == sg.WIN_CLOSED:
                exit()
        window.close()


if __name__ == '__main__':
    m = MainWindow()
    m.run()
