"""
  Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.

  Redistribution and use of the Software in source and binary forms, with or without modification,
   are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

     2. Redistributions in binary form, except as used in conjunction with
     Wiliot's Pixel in a product or a Software update for such product, must reproduce
     the above copyright notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the distribution.

     3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
     may be used to endorse or promote products or services derived from this Software,
     without specific prior written permission.

     4. This Software, with or without modification, must only be used in conjunction
     with Wiliot's Pixel or with Wiliot's cloud service.

     5. If any Software is provided in binary form under this license, you must not
     do any of the following:
     (a) modify, adapt, translate, or create a derivative work of the Software; or
     (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
     discover the source code or non-literal aspects (such as the underlying structure,
     sequence, organization, ideas, or algorithms) of the Software.

     6. If you create a derivative work and/or improvement of any Software, you hereby
     irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
     royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
     right and license to reproduce, use, make, have made, import, distribute, sell,
     offer for sale, create derivative works of, modify, translate, publicly perform
     and display, and otherwise commercially exploit such derivative works and improvements
     (as applicable) in conjunction with Wiliot's products and services.

     7. You represent and warrant that you are not a resident of (and will not use the
     Software in) a country that the U.S. government has embargoed for use of the Software,
     nor are you named on the U.S. Treasury Department’s list of Specially Designated
     Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
     You must not transfer, export, re-export, import, re-import or divert the Software
     in violation of any export or re-export control laws and regulations (such as the
     United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
     and use restrictions, all as then in effect

   THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
   OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
   WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
   QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
   IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
   ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
   OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
   FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
   (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
   (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
   (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
   (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""
import http.client
import serial.tools.list_ports
import PySimpleGUI as SimGUI
from wiliot_api import ManufacturingClient
from wiliot_core import check_user_config_is_ok, InlayTypes
from wiliot_testers.utils.get_version import get_version
from wiliot_testers.calibration_test.calibration_test_by_tbp import *
from wiliot_testers.tester_utils import open_json, open_json_cache
from wiliot_testers.wiliot_tester_tag_result import *
from wiliot_testers.test_equipment import serial_ports
from PIL import Image
import re
from pathlib import Path
import pathlib
import ast
import time


class ConfigDefaults(object):
    """
    contains the default values for the configuration json
    """

    def __init__(self):
        self.printer_defaults = {'TCP_IP': '192.168.6.61', 'TCP_PORT': '3003', 'TCP_BUFFER': '128',
                                 'enableLineSelection': 'Yes', 'enablePrinterAck': 'No',
                                 'printingDuringMovement': 'Yes'}
        self.single_band_gw_defaults = {'energizingPattern': '18', 'timeProfile': '3,7', 'txPower': '3',
                                        'rssiThreshold': '90', 'plDelay': '150'}
        self.dual_band_gw_defaults = {'energizingPattern': '18', 'secondEnergizingPattern': '52', 'timeProfile': '5,10',
                                      'txPower': '3', 'rssiThreshold': '90', 'plDelay': '100'}
        self.external_hw = {"temperatureSensorEnable": "No",
                            "AutoAttenuatorEnable": "No", "attnComport": "AUTO", "attnval": "0",
                            "scannerType": "rtscan"}

    def get_printer_defaults(self):
        return self.printer_defaults

    def get_single_band_gw_defaults(self):
        return self.single_band_gw_defaults

    def get_dual_band_gw_defaults(self):
        return self.dual_band_gw_defaults

    def get_external_hw_defaults(self):
        return self.external_hw


class DefaultGUIValues:
    def __init__(self, gui_type):
        if gui_type == 'Main':
            self.default_gui_values = {
                                       'toPrint': 'No', 'printOffset': '1', 'printingFormat': 'SGTIN',
                                       'batchName': 'test_reel',
                                       'tagGen': 'N/A',
                                       'testName': 'Ble_Test_Only', 'inlay': InlayTypes.TIKI_099.value,
                                       'desiredTags': '9999999', 'desiredPass': '9999999',
                                       'surface': SurfaceTypes.AIR.value,
                                       'conversion': ConversionTypes.STANDARD.value,
                                       'Environment': 'production', 'OwnerId': 'wiliot-ops', 'operator': '',
                                       'QRRead': 'No', 'QRcomport': 'COM3', 'QRoffset': '2',
                                       'QRtimeout': '200',
                                       'comments': '', 'maxFailStop': '50', 'maxYieldStop': '40',
                                       'pass_response_diff': '100', 'pass_response_diff_offset': '9999'}
        elif gui_type == 'Test':
            self.default_gui_values = {'passJobName': 'SGTIN_QR', 'passJobNum': 2, 'sgtin': 'test_test_test_test_X_',
                                       'stringBeforeCounter': 'test',
                                       'reelNumManually': 'test', 'firstPrintingValue': '0', 'tagLocation': '0',
                                       'tag_reel_location': '0'}
        elif gui_type == 'SGTIN':
            self.default_gui_values = {'passJobName': 'SGTIN_QR', 'passJobNum': 2, 'sgtin': '(01)00850027865010(21)',
                                       'stringBeforeCounter': '',
                                       'reelNumManually': '', 'firstPrintingValue': '0', 'tagLocation': '0',
                                       'tag_reel_location': '0'}
        elif gui_type == 'Barcode':
            self.default_gui_values = {'passJobName': 'BARCODE_8', 'passJobNum': 3, 'sgtin': '',
                                       'stringBeforeCounter': '',
                                       'reelNumManually': '', 'firstPrintingValue': '0', 'tagLocation': '0',
                                       'tag_reel_location': '0'}
        else:
            self.default_gui_values = {}


def simple_calibration_gui():
    """
    open pop up window
    :type message: string
    :param message: message to print on the window
    """

    dir_config = '../configs'
    tests_suites_configs_path = join(dir_config, 'tests_suites.json')
    with open(tests_suites_configs_path, 'r') as f:
        test_suite = json.load(f)

    inlay_type_list = [*test_suite]
    calibration_vals = []
    calibration_patterns = []
    calibration_powers = []
    calibration_timeprofiles = []
    layout = [[SimGUI.Text('Calibration Test Suite')],
              [SimGUI.Listbox(inlay_type_list, size=(35, len(inlay_type_list)), key='-CalibrationSuite-')],
              [SimGUI.Button('Ok')]]
    start_calib = True
    window = SimGUI.Window('Offline Simple Calibration', layout, default_element_size=(35, 1), auto_size_text=True,
                           auto_size_buttons=False,
                           default_button_element_size=(12, 1), element_justification='center')
    while True:  # the event loop
        event, values = window.read()
        if event == SimGUI.WIN_CLOSED:
            break
        if event == 'Ok':
            if values['-CalibrationSuite-']:  # if something is highlighted in the list
                for power_index in test_suite[values['-CalibrationSuite-'][0]]['tests']:
                    # if 'absGwTxPowerIndex' in power_index:
                    #     if int(power_index['absGwTxPowerIndex']) < 0 :
                    #         power_index['absGwTxPowerIndex'] = 19 + int(power_index['absGwTxPowerIndex'])
                    # else:
                    #     logging.warning('Problem with generating absGwTxPowerIndex value from\nTest suite, please check JSON file,\nWill calibrate with default power : 18')
                    #     power_index['absGwTxPowerIndex'] = 18
                    power_index['absGwTxPowerIndex'] = [14, 18]
                    if not 'timeProfile' in power_index:
                        power_index['timeProfile'] = [5, 15]
                    if not 'energizingPattern' in power_index:
                        logging.warning(
                            'Problem with read energizing power from test_suite \nPlease check test configuration file')
                        start_calib = False
                        break
                    calibration_vals.append(
                        {'pattern': power_index['energizingPattern'], 'power': power_index['absGwTxPowerIndex'],
                         'timeprofile': power_index['timeProfile']})
                    calibration_patterns.append(power_index['energizingPattern']) if power_index[
                                                                                         'energizingPattern'] not in calibration_patterns else calibration_patterns
                    # calibration_powers.append(power_index['absGwTxPowerIndex']) if power_index['absGwTxPowerIndex'] not in calibration_powers else calibration_powers
                    calibration_timeprofiles.append(power_index['timeProfile']) if power_index[
                                                                                       'timeProfile'] not in calibration_timeprofiles else calibration_timeprofiles
                calibration_powers.sort()
                calibration_power_range = range(power_index['absGwTxPowerIndex'][0],
                                                power_index['absGwTxPowerIndex'][-1] + 1)
                print('Starting calibration with values: powers: {}, time profile : {}, patterns : {}'.format(
                    str([calibration_power_range[0], calibration_power_range[-1]]),
                    str([calibration_timeprofiles[0][0], calibration_timeprofiles[0][-1]]), str(calibration_patterns)))
                SimGUI.popup(f"Calibration Started\n{values['-CalibrationSuite-'][0]}\nPlease wait",
                             button_type=SimGUI.POPUP_BUTTONS_NO_BUTTONS, non_blocking=True, no_titlebar=True,
                             auto_close=True, auto_close_duration=2)
                window.close()
                if start_calib:
                    top_score = start_calibration(
                        sweep_scan=[calibration_power_range[0], calibration_power_range[-1] + 1],
                        to_set=False, time_profiles_on=[calibration_timeprofiles[0][0]],
                        time_profiles_period=[calibration_timeprofiles[0][-1]],
                        energy_pattern_custom=calibration_patterns)

                    SimGUI.popup('Calibration Done\nWindow will be closed in 10 sec', keep_on_top=True,
                                 no_titlebar=True, auto_close=True, auto_close_duration=10)
                    print('Calibration Done')
                break
    window.close()
    return


def open_session(test_suite_list):
    """
    gets the user inputs from first GUI
    :return: dictionary of the values
    """

    def Collapsible(layout, key, title='', arrows=(SimGUI.SYMBOL_DOWN, SimGUI.SYMBOL_UP), collapsed=False):
        return SimGUI.Column(
            [[SimGUI.T((arrows[1] if collapsed else arrows[0]), enable_events=True, k=key + '-BUTTON-'),
              SimGUI.T(title, enable_events=True, key=key + '-TITLE-')],
             [SimGUI.pin(SimGUI.Column(layout, key=key, visible=not collapsed, metadata=arrows))]], pad=(0, 0))

    def check_structure(input_str):
        pattern = re.compile("^[A-Z0-9]{6}\.[0-9]{2}_[A-F]$")
        if not pattern.match(input_str):
            return False
        if not (0 < int(input_str[7:9]) <= 25):
            return False
        return True

    # move to r2r : return dict - r2r
    WILIOT_DIR = WiliotDir()
    dir_wiliot = WILIOT_DIR.get_wiliot_root_app_dir()
    tester_dir = join(dir_wiliot, 'offline')
    dir_config = join(tester_dir, '../configs')
    configuration_dir = os.path.join(dir_config, 'calibration_config.json')
    if os.path.exists(configuration_dir):
        with open(configuration_dir) as confile:
            configuration = json.load(confile)
            if configuration == '':
                confile.close()
                logging.warning('Setup configuration is not set, please execute calibration')
                with open(configuration_dir, 'w') as output:
                    configuration = default_calibration()
                    json.dump(configuration, output, indent=2, separators=(", ", ": "), sort_keys=False)

    else:
        logging.warning('Setup configuration is not set, please execute calibration')
        pathlib.Path(dir_config).mkdir(parents=True, exist_ok=True)
        with open(configuration_dir, 'w') as output:
            configuration = default_calibration()
            json.dump(configuration, output, indent=2, separators=(", ", ": "), sort_keys=False)

    current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent_path = os.path.dirname(current_path)
    wiliot_logo = os.path.join(parent_path, "docs", "wiliot_logo.png")
    wiliot_logo_image = Image.open(wiliot_logo)
    wiliot_logo_image = wiliot_logo_image.resize((128, 50), Image.LANCZOS)
    wiliot_logo_image.save(wiliot_logo, format="png")

    folder_name = 'configs'
    file_name = 'gui_inputs_do_not_delete.json'
    gui_inputs_values = open_json(folder_path=folder_name, file_path=os.path.join(folder_name, file_name),
                                  default_values=DefaultGUIValues(gui_type='Main').default_gui_values)
    for key in DefaultGUIValues(gui_type='Main').default_gui_values.keys():
        if key not in gui_inputs_values.keys():
            gui_inputs_values[key] = DefaultGUIValues(gui_type='Main').default_gui_values[key]

    EXTEND_KEY = '-SECTION-'
    SimGUI.theme('GreenTan')
    inlay_group = tuple([x.value for x in InlayTypes])
    conversion_group = tuple([conv.value for conv in ConversionTypes])
    surface_group = tuple([surf.value for surf in SurfaceTypes])

    main_data_tab = [[SimGUI.Text('Reel_name:', size=(40, 1)), SimGUI.InputText(gui_inputs_values['batchName'],
                                                                                key='batchName')],
                     [SimGUI.Text('Operator:', size=(40, 1)), SimGUI.InputText(gui_inputs_values['operator'],
                                                                               key='operator')],
                     [SimGUI.InputCombo(('D'), visible=False, default_value='D3', key='tagGen')],
                     [SimGUI.Text('Test suite:', size=(40, 1)),
                      SimGUI.InputCombo(test_suite_list, default_value=gui_inputs_values['testName'],
                                        key='testName')],
                     [SimGUI.Text('Environment', size=(40, 1), visible=True),
                      SimGUI.InputCombo((tuple(['test', 'production'])), default_value=gui_inputs_values['Environment'],
                                        key='Environment', visible=True)],
                     [SimGUI.Text('Owner Id', size=(40, 1), visible=True),
                      SimGUI.InputCombo((tuple(['wiliot-ops', '852213717688'])),
                                        default_value=gui_inputs_values['OwnerId'], key='OwnerId', visible=True)],
                     [SimGUI.Text('', size=(40, 1))],
                     [SimGUI.Text('', size=(40, 1))],
                     [SimGUI.Text('Comments:', size=(40, 1)), SimGUI.InputText(gui_inputs_values['comments'],
                                                                               key='comments')]]

    reel_tab = [[SimGUI.Text('Inlay serial number (3 digits):', size=(40, 1), visible=True),
                 SimGUI.InputCombo(inlay_group, default_value=gui_inputs_values['inlay'], key='inlay', visible=True)],
                [SimGUI.Text('Surface:', size=(40, 1), visible=True),
                 SimGUI.InputCombo(surface_group,
                                   default_value=gui_inputs_values['surface'], key='surface',
                                   visible=True)],
                [SimGUI.Text('Conversion', size=(40, 1), visible=True),
                 SimGUI.InputCombo(conversion_group, default_value=gui_inputs_values['conversion'],
                                   key='conversion', visible=True)],
                [SimGUI.Text('External attenuator', size=(40, 1), visible=False),
                 SimGUI.Checkbox('', default=False, key='externalAttenuator',
                                 disabled=False, visible=False)],
                [SimGUI.Text('Attenuator ComPort: ', size=(40, 1), visible=False),
                 SimGUI.Spin(values=['Auto', 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                             initial_value=('Auto'),
                             size=(6, 1), key='attnComport', visible=False)],
                [SimGUI.Text('Attenuation value:', size=(40, 1), visible=False),
                 SimGUI.Spin(values=[i for i in range(5, 20)], key='attnval',
                             initial_value=5,
                             size=(6, 1), visible=False)]]

    print_tab = [[SimGUI.Text('To print?', size=(40, 1)),
                  SimGUI.InputCombo(('Yes', 'No'), default_value=gui_inputs_values['toPrint'], key='toPrint')],
                 [SimGUI.Text('What is the printing job format?', size=(40, 1)),
                  SimGUI.InputCombo(('Test', 'SGTIN', 'Barcode'), default_value=gui_inputs_values['printingFormat']
                                    if gui_inputs_values['printingFormat'] != 'Test' else 'SGTIN', key='printingFormat')],
                 [SimGUI.Text('printing offset', size=(40, 1)),
                  SimGUI.Spin(values=[i for i in range(0, 5)], initial_value=int(gui_inputs_values['printOffset']),
                              size=(6, 1), key='printOffset')],
                 [SimGUI.Text('QR Validation:', size=(40, 1)),
                  SimGUI.InputCombo(('Yes', 'No'), visible=True, default_value=gui_inputs_values["QRRead"],
                                    key='QRRead')],
                 [SimGUI.Text('QR ComPort: ', size=(40, 1), visible=True),
                  SimGUI.Spin(values=[i for i in range(1, 15)], initial_value=(
                      int(gui_inputs_values['QRcomport'][-1]) if len(str(gui_inputs_values['QRcomport'])) > 1 else int(
                          gui_inputs_values['QRcomport'])),
                              size=(6, 1), key='QRcomport')],
                 [SimGUI.Text('QR offset (tags between GW and QR scanner):', size=(40, 1), visible=True),
                  SimGUI.Spin(values=[i for i in range(1, 10)], initial_value=int(gui_inputs_values['QRoffset']),
                              size=(6, 1), key='QRoffset')],
                 [SimGUI.Text('QR Timeout:', size=(40, 1), visible=True),
                  SimGUI.Spin(values=[i for i in range(100, 1000, 100)],
                              initial_value=int(gui_inputs_values['QRtimeout']),
                              size=(6, 1), key='QRtimeout')]
                 ]

    stop_conditiona_tab = [
                           [SimGUI.Text('Ignore stop conditions', size=(40, 1)),
                            SimGUI.Checkbox('', default=False, key='ignoreStop',
                                            disabled=False, visible=True)],
                           [SimGUI.Text('Max failed tags in a row:', size=(40, 1)),
                            SimGUI.Spin(values=[i for i in range(1, 999999)], key='maxFailStop',
                                        initial_value=int(
                                            gui_inputs_values['maxFailStop']),
                                        size=(6, 1))],
                           [SimGUI.Text('Minimum yield [%]', size=(40, 1)),
                            SimGUI.Spin(values=[i for i in range(1, 99)], key='maxYieldStop',
                                        initial_value=int(
                                            gui_inputs_values['maxYieldStop']),
                                        size=(6, 1))],
                           [SimGUI.Text('Desired amount of tags\n(will stop the run after this amount of tags):',
                                        size=(40, 2)),
                            SimGUI.InputText(gui_inputs_values['desiredTags'], key='desiredTags')],
                           [SimGUI.Text('Desired amount of pass\n(will stop the run after this amount of passes):',
                                        size=(40, 2)),
                            SimGUI.InputText(gui_inputs_values['desiredPass'], key='desiredPass')]]

    layout = [
        [SimGUI.Image(filename=str(wiliot_logo))],
        [SimGUI.TabGroup(
            [[
                SimGUI.Tab('Main Run Data', main_data_tab),
                SimGUI.Tab('Reel Data', reel_tab),
                SimGUI.Tab('Stop Condition', stop_conditiona_tab),
                SimGUI.Tab('Printing', print_tab)]])],
        [SimGUI.Submit(button_color=('white', '#0e6251'), size=(10, 1)),
         SimGUI.Stretch(),
         SimGUI.Text('Version: {}'.format(get_version()), font='Helvetica 8 bold', justification='right')]]

    window = SimGUI.Window('Offline Tester', layout, font='Calibri')
    calib_val = False
    while True:
        event, values = window.read()

        if event is None:
            print('User exited the program')
            window.close()
            exit()

        elif event.startswith(EXTEND_KEY):
            window[EXTEND_KEY].update(visible=not window[EXTEND_KEY].visible)
            window[EXTEND_KEY + '-BUTTON-'].update(
                window[EXTEND_KEY].metadata[0] if window[EXTEND_KEY].visible else window[EXTEND_KEY].metadata[1])

        elif event == 'Submit':
            # make sure user input is legit
            reel_name_ver = False
            if int(values['printOffset']) != int(gui_inputs_values['printOffset']):
                # popup warning message:
                change_in_printing_offset = \
                    SimGUI.popup_ok_cancel('Are you sure you want to change the printing offset?\n'
                                           '(old value:{}, new value: {})?\n'.format(gui_inputs_values['printOffset'],
                                                                                     values['printOffset']),
                                           keep_on_top=True, font=('normal', 20))
                if change_in_printing_offset.lower() == 'cancel':
                    values['printOffset'] = gui_inputs_values['printOffset']
                    SimGUI.popup('printing offset was NOT change and equals to {}'.format(values['printOffset']),
                                 button_type='ok', font=14)

            if ' ' in values['batchName'] or '/' in values['batchName'] or '\\' in values['batchName']:
                print("Reel name could not contain spaces, '\\' or '/'\nplease fix it and press Submit")
                continue

            else:
                try:
                    int(values['desiredTags'])
                    int(values['desiredPass'])
                except Exception:
                    print("the following values should be numbers (integer): packetThreshold,"
                          "desiredTags, desiredPass (and should not be smaller than 2")
                    continue
                yes_no = ['Yes', 'No']
                if values['toPrint'] not in yes_no:
                    print("the following values should be 'Yes' or 'No': toPrint")
                    continue
                if values['Environment'] == 'production' and values['toPrint'].lower() == 'yes':
                    reel_name_ver = check_structure(values['batchName'])
                else:
                    reel_name_ver = True

                if reel_name_ver:
                    break
                else:
                    SimGUI.popup('Reel name error \n Reel name should be: <6 uppercase alphanumeric chars>.'
                                 '<2 integers minimum 01 maximum 25>_<upper case char minimum A maximum F>',
                                 button_type='ok', font=14)

        elif event == 'Advanced Calibration':
            # calib_val = True
            # break
            window.hide()
            calib_values = open_calibration_config()
            window.un_hide()

        elif event == 'Simple Calibration':
            window.hide()
            simple_calibration_gui()
            window.un_hide()

        elif event == SimGUI.WIN_CLOSED or event == 'Exit':
            print('User exited the program')
            break

    window.close()
    for key in gui_inputs_values.keys():
        if key not in values.keys():
            values[key] = gui_inputs_values[key]
    # to defend against user errors
    values['tagGen'] = values['tagGen'].upper()
    with open(os.path.join(folder_name, file_name), 'w') as f:
        json.dump(values, f, indent=2, separators=(", ", ": "), sort_keys=False)

    if calib_val:
        calib_values = open_calibration_config()

    return values


def get_printed_value(string_before_the_counter: str, digits_in_counter: int, first_counter: str, printing_format: str):
    """
    builds the printed value
    :type string_before_the_counter: string
    :param string_before_the_counter: the sg1 Id of the tested reel
    :type digits_in_counter: int
    :param digits_in_counter: amount of digits in the tag counter field (usually 4)
    :type first_counter: string
    :param first_counter: counter of the run first tag
    :type printing_format: string
    :param printing_format: this run printing format (SGTIN, string)
    """
    first_print = str(string_before_the_counter)
    if 'SGTIN' in printing_format or 'Test' in printing_format or 'Barcode' in printing_format:
        first_print += 'T'
    if digits_in_counter < len(first_counter):
        is_ok = False
    else:
        dif_len = (digits_in_counter - len(first_counter))
        for i in range(digits_in_counter):
            # add zeros to where the counter is not needed
            if i < dif_len:
                first_print += '0'
            else:
                # add the first counter number by order to the string
                first_print += str(first_counter)
                break
        is_ok = True
    return first_print, is_ok


def gui_inputs_values_for_test_and_sgtin(printing_format):
    """
    A function that sends the GUI's input
    """
    folder_name = 'configs'
    file_name = get_print_user_config_file(printing_format)
    gui_inputs_values = open_json_cache(folder_path=folder_name, file_path=os.path.join(folder_name, file_name),
                                        default_values=DefaultGUIValues(printing_format).default_gui_values)
    return gui_inputs_values


def printing_process_of_test_and_sgtin(window, printing_format, gui_inputs_values, env='', owner_id='wiliot-ops'):
    """
    A function that does all the work of the printing process
    """
    read_only = False
    reel_number = ''
    tag_digits_num = 4
    pass_job_name = None
    is_ok = True
    while True:
        event, values = window.read()
        should_submit = True
        if printing_format != 'Test':
            pass_job_name = values['passJobName']
        if event == SimGUI.WINDOW_CLOSED or event is None:
            is_ok = False
            break
        if event == 'Submit':
            try:
                printing_value = 'First counter number is too big for counter digits number!!\n''Please enter a new first counter number'
                if (printing_format != 'Test' and not values['isNewReel']) or (
                        printing_format == 'Test' and not values['isManually']):
                    pass_job_name = values['passJobName']
                    first_counter = values['firstPrintingValue']
                    if printing_format == 'Test':
                        window['sgtinNumManually'].update('test_test_test_test_X_')
                        window['reelNumManually'].update('test')
                    if len(str(values['firstPrintingValue'])) > tag_digits_num:
                        if printing_format != 'Test':
                            printing_value += 'you entered: ' + str(
                                values['firstPrintingValue'] + ' in length of: ' + len(
                                    str(values['firstPrintingValue'])))
                        window['-OUTPUT-'].update(printing_value)
                        should_submit = False
                    else:
                        should_submit = True
                        if printing_format != 'Test':
                            reel_number = str(gui_inputs_values['sgtin']) + str(gui_inputs_values['reelNumManually'])
                            first_print, is_ok = get_printed_value(reel_number, tag_digits_num, first_counter,
                                                                   printing_format)
                            print('The first tag printing value will be: ' + first_print)
                elif (printing_format != 'Test' and values['isNewReel']) or (
                        printing_format == 'Test' and values['isManually']):
                    if len(str(values['firstPrintingValue'])) > tag_digits_num:
                        if printing_format != 'Test':
                            printing_value += 'you entered: ' + str(
                                values['firstPrintingValue'] + ' in length of: ' + len(
                                    str(values['firstPrintingValue'])))
                        window['-OUTPUT-'].update(printing_value)
                        should_submit = False
                    elif (printing_format == 'SGTIN' or 'SGTIN' in values['passJobName']) and not len(
                            str(values['sgtinNumManually'])) == 22:
                        window['-OUTPUT-'].update(
                            'SGTIN number is not equal to 22 chars!!\n'
                            'Please enter correct SGTIN, its length is: ' + str(len(str(values['sgtinNumManually']))))
                        should_submit = False
                    elif (printing_format == 'SGTIN' or 'SGTIN' in values['passJobName']) and not len(
                            str(values['reelNumManually'])) == 4:
                        window['-OUTPUT-'].update(
                            'Reel number is not equal to 4 chars!!\n'
                            'Please enter correct Reel number')
                        should_submit = False
                    elif (printing_format == 'Barcode' or 'Barcode' in values['passJobName']) and len(
                            values['reelNumManually']) != 3:
                        window['-OUTPUT-'].update(
                            'Reel number is not equal to 3 chars!!\n'
                            'Please enter correct Reel number')
                        if printing_format == 'Barcode':
                            should_submit = False
                    else:
                        pass_job_name = values['passJobName']
                        reel_number = str(values['sgtinNumManually']) + str(values['reelNumManually'])
                        first_counter = values['firstPrintingValue']
                        first_print, is_ok = get_printed_value(reel_number, tag_digits_num,
                                                               first_counter, printing_format)
                        if printing_format == 'Test':
                            window['-OUTPUT-'].update('The first tag printing value will be:\n' + first_print)
                        else:
                            print('The first tag printing value will be: ' + first_print)
                        should_submit = True

            except Exception:

                window['-OUTPUT-'].update(

                    'First counter is not a number!!\nPlease enter a new first counter number')

                should_submit = False

            if should_submit:
                break
    if (printing_format != 'Test' and is_ok) or (printing_format == 'Test'):
        v = {'passJobName': pass_job_name, 'digitsInCounter': tag_digits_num, 'passJobNum': values['passJobNum'],
             'firstPrintingValue': values['firstPrintingValue'], 'tagLocation': values['firstPrintingValue'],
             'tag_reel_location': gui_inputs_values['tag_reel_location']}

        data_to_save = {'passJobName': pass_job_name,
                        'passJobNum': values['passJobNum'],
                        'sgtin': values['sgtinNumManually'],
                        'reelNumManually': values['reelNumManually'],
                        'firstPrintingValue': values['firstPrintingValue'],
                        'tagLocation': values['firstPrintingValue'],
                        'tag_reel_location': gui_inputs_values['tag_reel_location']}

        if printing_format != 'Test':
            v['stringBeforeCounter'] = reel_number
            v['failJobName'] = 'line_'
            v['printingFormat'] = printing_format
            data_to_save['stringBeforeCounter'] = reel_number
            data_to_save['printingFormat'] = printing_format
        elif printing_format == 'Test':
            v['stringBeforeCounter'] = values['sgtinNumManually'] + values['reelNumManually']
            v['failJobName'] = pass_job_name
        folder_name = 'configs'
        file_name = get_print_user_config_file(printing_format)
        f = open(os.path.join(folder_name, file_name), "w")
        json.dump(data_to_save, f)
        f.close()
        return v, is_ok

    return gui_inputs_values, is_ok


def get_print_user_config_file(printing_format):
    if printing_format.lower() == 'test':
        filename = 'gui_printer_inputs_4_Test_do_not_delete.json'
    elif printing_format.lower() in ('sgtin', 'barcode'):
        filename = 'gui_printer_inputs_4_SGTIN_do_not_delete.json'
    else:
        filename = ''
        print(f'unsupported printing format: {printing_format}, valid formats are: sgtin, barcode, test')
    return filename


def printing_test_window():
    """
    opens the GUI for user input for test print
    :return: dictionary of user inputs
    """
    printing_format = 'Test'
    gui_inputs_values = gui_inputs_values_for_test_and_sgtin(printing_format)

    if gui_inputs_values['reelNumManually'] == "":
        reel_num = 'test_test_test_test_X_test'
        gui_inputs_values['sgtin'] = reel_num[:22]
        gui_inputs_values['reelNumManually'] = reel_num[22:]
        gui_inputs_values['firstPrintingValue'] = '0'
        gui_inputs_values['tagLocation'] = '0'
        gui_inputs_values['tag_reel_location'] = '0'

    layout = [[SimGUI.Text('Job to print for pass and fail:'),
               SimGUI.InputCombo(('SGTIN_only', 'SGTIN_QR', 'BARCODE_8', 'devkit_TEO', 'devkit_TIKI', 'empty'),
                                 default_value=gui_inputs_values['passJobName'], key='passJobName')],
              [SimGUI.Text('pass line number:'),
               SimGUI.Input(gui_inputs_values['passJobNum'], key='passJobNum')],
              [SimGUI.Text("What is the first counter number?")],
              [SimGUI.Input(gui_inputs_values['firstPrintingValue'], key='firstPrintingValue')],
              [SimGUI.Checkbox('Insert reel number manually?', default=False, key='isManually')],
              [SimGUI.Text("For manual mode only - what is the sgtin number?", key='sgtinNumManuallyText'),
               SimGUI.Input(gui_inputs_values['sgtin'], key='sgtinNumManually')],
              [SimGUI.Text("For manual mode only - what is the reel number?", key='reelNumManuallyText'),
               SimGUI.Input(gui_inputs_values['reelNumManually'], key='reelNumManually')],
              [SimGUI.Text(size=(60, 3), key='-OUTPUT-')],
              [SimGUI.Text("*Tags in this run will not be serialized")],
              [SimGUI.Button('Check first print'), SimGUI.Button('Submit', button_color=('white', '#0e6251'))]]
    window = SimGUI.Window('Printing Test', layout, keep_on_top=True)
    wanted_v, wanted_is_ok = printing_process_of_test_and_sgtin(window, printing_format, gui_inputs_values)
    window.close()
    return wanted_v, wanted_is_ok


def printing_sgtin_window(env='', owner_id='wiliot-ops', printing_format='SGTIN'):
    """
    opens the GUI for user input for SGTIN print
    :return: dictionary of user inputs
    """
    read_only = False
    gui_inputs_values = gui_inputs_values_for_test_and_sgtin(printing_format)

    # Checking if it's a new reel run and updating the GUI inputs according to this
    new_run = SimGUI.popup_yes_no('    New Reel?    \n', keep_on_top=True, font=('normal', 20))
    if env == 'production' or env == '':
        env = 'prod'
    if new_run == 'Yes':
        gui_inputs_values['tagLocation'] = '0'
        gui_inputs_values['tag_reel_location'] = '0'
        try:
            logging.info('Receiving data from the cloud, please wait')
            reel_num = get_reel_name_from_cloud_api(env, owner_id, printing_format)
            print(reel_num)
        except Exception:
            logging.warning('Problem with receiving data from cloud')
            raise Exception
        gui_inputs_values['firstPrintingValue'] = '0000'
        if 'data' in reel_num:
            reel_number = reel_num['data']
            if printing_format == 'SGTIN':
                gui_inputs_values['sgtin'] = reel_number[:22]
                gui_inputs_values['reelNumManually'] = reel_number[22:26]
            elif printing_format == 'Barcode':
                gui_inputs_values['sgtin'] = ''
                gui_inputs_values['reelNumManually'] = reel_number
            else:
                raise Exception(f'printing_format is not supported: {printing_format}')
            read_only = True
        else:
            gui_inputs_values['sgtin'] = ''
            gui_inputs_values['reelNumManually'] = ''
            read_only = False

    layout = [[SimGUI.Text('Job to print for pass:'),
               SimGUI.InputCombo(('SGTIN_only', 'SGTIN_QR', 'BARCODE_8', 'devkit_TEO', 'devkit_TIKI', 'empty'),
                                 default_value='BARCODE_8' if printing_format == 'Barcode' else 'SGTIN_QR',
                                 key='passJobName')],
              [SimGUI.Text('fail line number: 1, pass line number:'),
               SimGUI.Input(gui_inputs_values['passJobNum'], key='passJobNum')],
              [SimGUI.Text("First counter number")],
              [SimGUI.Input(0000 if read_only else gui_inputs_values['firstPrintingValue'], key='firstPrintingValue',
                            readonly=read_only)],
              [SimGUI.Checkbox('Insert reel number manually?', default=not read_only, key='isNewReel',
                               disabled=read_only, visible=False)],
              [SimGUI.Text("SGTIN number", key='sgtinNumManuallyText'),
               SimGUI.Input(gui_inputs_values['sgtin'], key='sgtinNumManually', readonly=read_only)],
              [SimGUI.Text("Reel number", key='reelNumManuallyText'),
               SimGUI.Input(gui_inputs_values['reelNumManually'], key='reelNumManually', readonly=read_only)],
              [SimGUI.Text(size=(60, 3), key='-OUTPUT-')],
              [SimGUI.Text('Tag Reel Location: {}'.format(gui_inputs_values['tag_reel_location']))],
              [SimGUI.Button('Submit', button_color=('white', '#0e6251'))]]
    window = SimGUI.Window('Printing Test', layout, keep_on_top=True)
    wanted_v, wanted_is_ok = printing_process_of_test_and_sgtin(window, printing_format, gui_inputs_values, env,
                                                                owner_id)
    window.close()
    return wanted_v, wanted_is_ok


def save_screen(tested, passed, yield_, missing_labels, problem_in_locations_hist_val, ttfgp_avg, ttfp_max_error=1,
                default_upload_value=None, responded = None):
    """
    open last GUI
    :type tested: int
    :param tested: amount of tested tags
    :type passed: int
    :param passed: amount of passed tags
    :type yield_: float
    :param yield_: yield in the run
    :type missing_labels: int
    :param missing_labels: amount of missing_labels tags
    :type problem_in_locations_hist_val: dictionary or None
    :param problem_in_locations_hist_val: histogram of problem in the run (amount of locations)
    :type ttfgp_avg: float or None
    :param ttfgp_avg: average of ttfgp (time to first good packet) in this run
    :type default_upload_value: string ('Yes' or 'No')
    :param default_upload_value: default value to use in upload to cloud field
    :return dictionary with the user inputs (should upload, last comments)
    """
    SimGUI.theme('GreenTan')
    if ttfgp_avg is None or str(ttfgp_avg) == 'nan':
        ttfgp_avg_line = []
    elif ttfgp_avg < ttfp_max_error:
        ttfgp_avg_line = [
            SimGUI.Text("Average time to first good packet is OK (" + '{0:.4g}'.format(ttfgp_avg) + " secs)",
                        border_width=10, background_color='green')]
    else:
        ttfgp_avg_line = [SimGUI.Text("Average time to first good packet is too high (" + '{0:.4g}'.format(ttfgp_avg) +
                                      " secs)", border_width=10, background_color='red')]
    if default_upload_value is not None:
        def_upload = default_upload_value
    else:
        def_upload = "Yes"

    layout = [
        [SimGUI.Text('Tags tested = ' + str(tested), size=(21, 1)),
         SimGUI.Text('Tags responded = ' + str(responded if responded is not None else 0), size=(21, 1)),
         SimGUI.Text('Tags passed = ' + str(passed), size=(21, 1))],
        [SimGUI.Text('Yield = ' + '{0:.4g}'.format(yield_) + '%', size=(21, 2)),
         SimGUI.Text('Missing labels = ' + str(missing_labels), size=(21, 2))],
        ttfgp_avg_line,
        [SimGUI.Text('Would you like to upload this log to the cloud?'),
         SimGUI.InputCombo(('Yes', 'No'), default_value=def_upload, key='upload')],
        [SimGUI.Text('Post run comments:')],
        [SimGUI.InputText('', key='comments')],
        [SimGUI.Submit(button_color=('white', '#0e6251'))]]

    window = SimGUI.Window('Offline Tester - Summary ', layout, force_toplevel=True, keep_on_top=True)
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == SimGUI.WINDOW_CLOSED or event is None:
            print("user exited the program, upload did not happen")
            break
        if event == 'Submit':
            break
    window.close()
    # sys.exit(0)
    return values


def get_reel_name_from_cloud_api(env, owner_id, printing_format='SGTIN'):
    """
    api to receive reel number from cloud (should use it to avoid duplications)
    :return: the reel number (in 0x)
    """
    assert ('R2R_station_name' in os.environ), 'R2R_station_name is missing from PC environment variables'
    tester_station_name = os.environ['R2R_station_name']
    try:

        file_path, api_key, is_successful = check_user_config_is_ok(env=env, owner_id=owner_id)
        client = ManufacturingClient(api_key=api_key, logger_=logging.getLogger().name, env=env)
    except Exception as e:
        raise Exception('Failed to get token. Check previous errors.\n{}'.format(str(e)))

    try:

        payload = {"printerId": tester_station_name}
        reel_id_type = '?reelIdType=threeCharacters' if printing_format == "Barcode" else ''
        reel_id_type = {'reelIdType': 'threeCharacters'} if printing_format == "Barcode" else None

        rsp = client._post(path=f'{owner_id}/tag/roll/print', url_params=reel_id_type,
                           payload=payload, override_client_path='owner/', verbose=True)

        return rsp

    except Exception as e:
        raise ("An exception occurred at get_reel_name_from_cloud_API()\n{}".format(str(e)))


"""
    R2R Arduino
"""

ARDUINO_BAUD_RATE = 1000000


class R2rGpio(object):
    """
    class to open and use communication to Arduino on R2R machine
    """

    def __init__(self, logger_name=None):
        """
        initialize params and port
        """
        self.baud_rate = ARDUINO_BAUD_RATE
        self.comport = ''
        self.s = None
        self.connected = False
        self.logger = logging.getLogger(logger_name) if logger_name is not None else None
        ports_list = serial_ports()
        if len(ports_list) == 0:
            raise Exception("no serial ports were found. please check your connections")
        self.connect(ports_list)

    def is_connected(self):
        if self.s is None:
            return False

        if not self.s.isOpen():
            return False

        response = self.query("*IDN?")

        if "Williot R2R GPIO" in response:
            self.connected = True
            if self.logger is None:
                print('R2R: Found ' + response + " Serial Number " + self.query("SER?"))
            else:
                self.logger.info('R2R: Found ' + response + " Serial Number " + self.query("SER?"))
            self.s.flushInput()
            return True
        else:
            self.s.close()
            return False

    def connect(self, ports_list):
        for port in ports_list:
            try:
                self.comport = port
                self.s = serial.Serial(self.comport, self.baud_rate, timeout=0, write_timeout=0)

                if self.is_connected():
                    break

            except (OSError, serial.SerialException):
                pass
            except Exception as e:
                if self.logger is None:
                    print(e)
                else:
                    self.logger.warning(f'R2R: connect: {e}')
        if not self.connected:
            raise Exception('Could NOT connect to the Arduino, please check connections')

    def __del__(self):
        if self.s is not None:
            self.s.close()

    def write(self, cmd):
        """
        Send the input cmd string via COM Socket
        """
        if self.s.isOpen():
            pass
        else:
            self.s.open()

        try:
            self.s.flushInput()
            self.s.write(str.encode(cmd))
        except Exception:
            pass

    def query(self, cmd):
        """
        Send the input cmd string via COM Socket and return the reply string
        :return: massage from arduino (w/o the '\t\n')
        """
        if self.s.isOpen():
            pass
        else:
            self.s.open()
            sleep(1)
        self.s.flushInput()
        sleep(1)
        try:
            self.s.write(str.encode(cmd))
            sleep(2)
            data = self.s.readlines()
            value = data[0].decode("utf-8")
            # Cut the last character as the device returns a null terminated string
            value = value[:-2]
        except Exception:
            value = ''
        return value

    def read(self):
        """
        Send the input cmd string via COM Socket and return the reply string
        :return: massage from arduino (w/o the '\t\n')
        """
        if self.s.isOpen():
            pass
        else:
            self.s.open()
        try:
            timeout = time.time() + 5  # 5 second to receive arudio pulse
            while self.s.in_waiting == 0 and time.time() < timeout:
                pass
            if time.time() > timeout:
                logging.warning('No data received from Arduino')
                self.reconnect()

            data = self.s.readlines()
            self.s.flushInput()
            value = data[0].decode("utf-8")
            # Cut the last character as the device returns a null terminated string
            value = value[:-2]
        except Exception:
            value = ''
        return value

    def gpio_state(self, gpio, state):
        """
        gets the gpio state:
            my_gpio.gpio_state(3, "ON")
               start"on"/stop"off"
            my_gpio.gpio_state(4, "ON")
               enable missing label
        :param gpio: what gpio to write to
        :param state: to what state to transfer (ON / OFF)
        :return: reply from Arduino
        """
        cmd = 'GPIO' + str(gpio) + "_" + state
        replay = self.query(cmd)
        return replay

    def pulse(self, gpio, time):
        """
        send a pulse to the r2r machine:
            my_gpio.pulse(1, 1000)
               Pass
            my_gpio.pulse(2, 1000)
               fail
        :param gpio: what gpio to write to
        :param time: how long is the pulse
        :return: True if succeeded, False otherwise
        """
        cmd = 'GPIO' + str(gpio) + '_PULSE ' + str(time)
        self.write(cmd)
        sleep(time * 2 / 1000)
        replay = self.read()
        if replay == "Completed Successfully":
            return True
        else:
            return False

    def reconnect(self):
        if self.is_connected():
            logging.info(f'Already connected to Arduino on {self.comport}')
            return True
        try:
            # Attempt to open a connection to the specified comport
            self.s = serial.Serial(self.comport, self.baud_rate, timeout=0, write_timeout=0)
            logging.info(f'Connection to Arduino on {self.comport} reestablished.')
            reconnect_success = True

        except serial.serialutil.SerialException:
            logging.warning(
                f'Connection to {self.comport} failed. Attempting to close the connection and detect Arduino...')
            try:
                self.s.close()
                time.sleep(1)
                self.s = serial.Serial(self.comport, self.baud_rate, timeout=0, write_timeout=0)
                logging.info(f'Connection to Arduino on {self.comport} reestablished.')
                reconnect_success = True

            except Exception as e:
                logging.warning(f"Failed to close connection to {self.comport} {e} - Please restart connection")
                return False

        if reconnect_success:

            if self.is_connected():
                logging.info(
                    'Connection was restablished on COM{} with version {}'.format(self.comport, self.query("SER?")))
                self.s.flushInput()
            else:
                self.s.close()
                logging.warning(f"Failed to close connection to {self.comport} - Please restart connection")
                reconnect_success = False
        return reconnect_success


if __name__ == '__main__':
    rsp = get_reel_name_from_cloud_api(env='test', owner_id='wiliot-ops', printing_format='Barcode')

    open_session(['Single Band', 'Dual Band'])
    printing_test_window()
    printing_sgtin_window(env='test', printing_format='Barcode')
    printing_sgtin_window(env='test', printing_format='SGTIN')

    r = R2rGpio()
    open_session(['Single Band', 'Dual Band'])
    pass
