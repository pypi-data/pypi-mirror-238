from wiliot_testers.test_equipment import BarcodeScanner
global scan_timeout
import logging
from time import sleep, time
from datetime import datetime



if __name__ =='__main__':
    testlogger = logging.getLogger('QRLog')
    formatter = logging.Formatter('\x1b[36;20m%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                  '%H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    testlogger.addHandler(stream_handler)
    testlogger.setLevel(logging.DEBUG)
    scan_time = 400
    scanner = BarcodeScanner(write_to_log=True, timeout=str(scan_time), log_name=testlogger.name)

    t_i = datetime.now()
    dt = 0
    while dt < 60:
        sleep(0.1)
        results = scanner.scan_ext_id()
        # print(results)
        dt = (datetime.now() - t_i).total_seconds()
    scanner.close_port()


