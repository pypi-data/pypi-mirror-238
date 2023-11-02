import os
import time
from PIL import Image
import PySimpleGUI as sg
from wiliot_core import check_user_config_is_ok, WiliotDir, open_json
from wiliot_api import ManufacturingClient

class DataPullGUI:

    """
    To create .exe file for this script use the next line:
    pywiliot-testers> pyinstaller --onefile --windowed --add-data "./wiliot_testers/docs/wiliot_logo.png;./docs" ./wiliot_testers/utils/ppfp_tool.py
    """

    def __init__(self):
        current_script = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_script)
        os.chdir(current_dir)
        try:
            wiliot_logo = os.path.join('docs', 'wiliot_logo.png')
            if os.path.exists(wiliot_logo):
                pass
            else:
                raise Exception('Trying to lcoate .png')
        except Exception:
            wiliot_logo = os.path.join('..', 'docs', 'wiliot_logo.png')
        wiliot_logo_image = Image.open(wiliot_logo)
        wiliot_logo_image = wiliot_logo_image.resize((128, 50), Image.BICUBIC)
        wiliot_logo_image.save(wiliot_logo, format="png")
        sg.theme('GreenTan')
        self.layout = [
            [sg.Column([[sg.Image(wiliot_logo)]], justification='center')],
            [sg.Text('Owner ID', size=(15, 1)), sg.InputText(key='owner_id')],
            [sg.Text('Environment'), sg.Combo(['Production', 'Test'], default_value='Production', key='env')],
            [sg.Text('Tester Type'), sg.Combo(['Offline', 'Sample'], default_value='Offline', key='tester_type')],
            [sg.Text('Select mode for Common Run Name Insert')],
            [sg.Radio('Single CRN', "RADIO1", default=True, key='single_crn', enable_events=True), sg.Radio('CRN List (CSV)', "RADIO1", key='csv', enable_events=True)],
            [sg.Column([[sg.Text('CRN', size=(15, 1)), sg.InputText(key='crn')]], key='crn_col', visible=True),
             sg.Column([[sg.Text('CSV File', size=(15, 1)), sg.InputText(), sg.FileBrowse(key='csv_file')]], key='csv_file_col', visible=False)],
            [sg.Text('Select Target Directory')],
            [sg.Text('Directory', size=(15, 1)), sg.InputText(), sg.FolderBrowse(key='target_dir')],
            [sg.Submit(), sg.Cancel()]
        ]


    def run(self):
        window = sg.Window('PPFP Tool', self.layout, finalize=True, size=(600,350))

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancel'):
                break
            elif event == 'Submit':
                try:
                    env_dirs = WiliotDir()
                    config_dir_path = env_dirs.get_config_dir()
                    user_config_file_path = env_dirs.get_user_config_file()
                    loading_window = sg.Window('Loading', [[sg.Text('Loading...')]], finalize=True, no_titlebar=True,
                                               grab_anywhere=True)

                    if os.path.exists(user_config_file_path):
                        cfg_data = open_json(folder_path=config_dir_path, file_path=user_config_file_path)

                    window.minimize()
                    tester_type = 'offline-test' if values['tester_type'] == 'Offline' else 'sample-test'
                    file_path, api_key, is_successful = check_user_config_is_ok(env=values['env'][0:4].lower(), owner_id=values['owner_id'])
                    if not is_successful:
                        sg.popup_error('User configuration check failed')
                        continue
                    client = ManufacturingClient(api_key=api_key, env=values['env'][0:4].lower())

                    if values['single_crn']:
                        common_run_name = values['crn'].strip()
                        path_to_send = f'upload/testerslogs/{tester_type}?commonRunName={common_run_name}'
                        path = os.path.join(values['target_dir'], f'{common_run_name}.zip')
                        with open(path, 'wb') as f1:
                            rsp = client._get_file(path=path_to_send, out_file=f1, file_type='zip')

                    else:
                        try:
                            with open(values['csv_file'], 'r') as f:
                                for line in f:
                                    common_run_name = line.strip()  # Assuming each line in the CSV is a CRN
                                    path_to_send = f'upload/testerslogs/{tester_type}?commonRunName={common_run_name}'
                                    path = os.path.join(values['target_dir'], f'{common_run_name}.zip')
                                    with open(path, 'wb') as f1:
                                        rsp = client._get_file(path=path_to_send, out_file=f1, file_type='zip')
                        except Exception as e:
                            print(e)
                            sg.popup_error(f'An error occurred while loading CSV file - please check it', title='Error')
                            continue

                    loading_window.close()
                    if rsp:
                        print('Job Success')
                        done_window = sg.Window('Finish', [[sg.Text('Job Success')]], finalize=True, no_titlebar=True,
                                                   grab_anywhere=True, auto_close=True, auto_close_duration=5)
                        time.sleep(5)
                        window.close()
                    else:
                        sg.popup_error(f'An error occurred while getting data from cloud', title='Error')
                        break

                except Exception as e:
                    print(e)
                    sg.popup_error(f'An error occurred: {e}', title='Error')
                    break
            elif event == 'single_crn':
                window['csv_file_col'].update(visible=False)
                window['crn_col'].update(visible=True)
            elif event == 'csv':
                window['csv_file_col'].update(visible=True)
                window['crn_col'].update(visible=False)
        window.close()

if __name__ == '__main__':
    gui = DataPullGUI()
    gui.run()
