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

import mimetypes
from codecs import encode
import logging
import os
from wiliot_api import ManufacturingClient
from wiliot_core import check_user_config_is_ok


def upload_to_cloud_api(batch_name, tester_type, run_data_csv_name=None, packets_data_csv_name=None,
                        env='', is_batch_name_inside_logs_folder=True, logger_=None, is_path=False,
                        client=None, owner_id='wiliot-ops'):
    """
    uploads a tester log to Wiliot cloud
    :type batch_name: string
    :param batch_name: folder name of the relevant log
    :type run_data_csv_name: string
    :param run_data_csv_name: name of desired run_data log to upload,
                              should contain 'run_data' and end with .csv
    :type packets_data_csv_name: string
    :param packets_data_csv_name: name of desired packets_data log to upload,
                               should contain 'packets_data' and end with .csv
    :type tester_type: string
    :param tester_type: name of the tester the run was made on (offline, tal15k, conversion, yield)
    :type env: string (prod, dev, test)
    :param env: to what cloud environment should we upload the files
    :type is_batch_name_inside_logs_folder: bool
    :param is_batch_name_inside_logs_folder: flag to indicate if the batch_name is the regular run folder (logs) or
                                             this function is being used in a way we will need the full path
    :return: True for successful upload, False otherwise
    """
    # Checking the necessary files to start the upload process
    if logger_ is None:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(logger_)
    tester_type_name = tester_type.split('-')[0]
    if tester_type_name not in {'offline', 'tal15k', 'conversion', 'yield', 'sample'}:
        logger.warning('Unsupported tester_type inserted to upload_to_cloud_api()\nPlease change it and retry')
        return
    if run_data_csv_name and 'run_data' not in run_data_csv_name:
        logger.warning('Unsupported run_data_csv_name inserted to upload_to_cloud_api()\nPlease change it and retry')
        return
    if packets_data_csv_name and 'packets_data' not in packets_data_csv_name:
        logger.warning('Unsupported packets_data_csv_name inserted to upload_to_cloud_api()\nPlease change it and retry')
        return

    # Check user credentials
    if env == 'production' or env == '':
        env = 'prod'
    env = env.strip('/')
    if env not in {'prod', 'test', 'dev'}:
        logger.warning(f'Unsupported env value was inserted (env = {env})')
        return False
    user_config_file_path, api_key, is_successful = check_user_config_is_ok(env=env, owner_id=owner_id)
    if not is_successful:
        logger.warning('could not extract user credentials. please check warnings')
        return
    client = ManufacturingClient(api_key=api_key, env=env, logger_=logger.name) if client is None else client

    # Setting loggers, connection to API and headers.
    logger.info('Upload to cloud has began')

    # Set URL
    url = f'upload/testerslogs/'
    url += tester_type
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'

    # send a file to the cloud:
    def upload_a_file_to_cloud(file_type):
        if file_type == 'run':
            file_url = url + '/runs-indicators'
            csv_name = run_data_csv_name
        elif file_type == 'packets':
            file_url = url + '/packets-indicators'
            csv_name = packets_data_csv_name
        else:
            raise Exception(f'file type should be run or packets but received: {file_type}')
        logger.info("{} data csv upload to {} started".format(file_type, file_url))

        # determine the file path:
        if is_path:
            file_path = csv_name
        else:
            file_path = os.path.join("logs" if is_batch_name_inside_logs_folder else "", batch_name, csv_name)
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} could not be found. Please locate the file and try again.")

        # Prepare the multipart/form-data for the file upload
        filename = os.path.basename(file_path)
        file_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        data_list = [
            encode(f'--{boundary}'),
            encode(f'Content-Disposition: form-data; name=file; filename={filename}'),
            encode(f'Content-Type: {file_type}'),
            encode(''),
            open(file_path, 'rb').read(),
            encode(f'--{boundary}--'),
            encode('')]
        payload = b'\r\n'.join(data_list)

        # Make a POST request to upload the file data
        try:
            header_overwrite = {'Authorization': client.headers['Authorization'],
                                'Content-Type': f'multipart/form-data; boundary={boundary}'}
            rsp = client._post(path=file_url, payload=payload, override_headers=header_overwrite, verbose=True)
            logger.info(f'{rsp}\nThe file {csv_name} was uploaded successfully to Wiliot cloud')
            return True
        except Exception as e:
            logger.warning(f'Upload Failed!! due to {e}')
            return False

    run_upload_status = True
    packet_upload_status = True
    if run_data_csv_name is not None:
        run_upload_status = upload_a_file_to_cloud(file_type='run')

    if packets_data_csv_name is not None:
        packet_upload_status = upload_a_file_to_cloud(file_type='packets')

    merged_status = run_upload_status and packet_upload_status
    if merged_status:
        logger.info('\n-----------------------------------------------------------------------\n'
                    'upload to cloud is finished successfully\n'
                    '-----------------------------------------------------------------------')
    return merged_status
