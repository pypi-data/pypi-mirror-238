from enum import Enum


# Configurations and Enums for offline_main.py
class MainDefaults:
    MAX_QUEUE_SIZE = 100
    CALCULATE_INTERVAL = 10
    CALCULATE_ON = 50
    N_YIELD_SAMPLES_UNDER_THRESHOLD = 15
    FONT_NAME = 'SansSerif'
    FONT_SIZE = 10
    GUI_UPDATE_TIME = 500  # ms
    MAX_TTFP_ERROR = 2  # if ttfp avg is more than MAX_TTFP_ERROR, the summary window will be red
    DEFAULT_LANGUAGE = 'En'  # Default to English


# Configurations for offline_printing_and_validation.py
class PrintingAndValidationDefaults:
    PRINTER_SOCKET_TIMEOUT = 1  # seconds
    MIN_TEST_TIME = 1.5  # seconds
    TIME_BTWN_PRINTER_REQUESTS = 0.25  # seconds
    FAIL_JOB_NUM = 1  # line number for fail job
    PASS_JOB_NUM = 2  # line number for pass job
    TAG_COUNT_SIZE = 4  # number of characters per tag count inside the external id
    QUEUE_VALIDATION_OFFSET = 1  # queue size offset when no scanner is connected
    ARDUINO_BAUD_RATE = 1000000
    PASS_PULSE_GPIO = 1
    FAIL_PULSE_GPIO = 2
    START_STOP_GPIO = 3
    MISSING_LABEL_GPIO = 4
    R2R_PULSE_DURATION = 50  # msec
    MAX_R2R_WAIT_TIME = 90  # being on the safe side since r2r can wait max 99 seconds
    EVENT_WAIT_TIME = 20  # the max time to wait for an event
    MIN_WAIT_TIME = 1  # time to wait for start validation if stop is set
    MAX_TIME_BETWEEN_TESTS = 5  # the max time between the r2r movement and receiving the next trigger
    MAX_MAIN_STATES = 80
    PRINTER_90_DEG_WAIT_TIME = 1


# Configurations for offline_tag_testing.py
class TagTestingDefaults:
    TIMEOUT_FOR_MISSING_LABEL = 5
    TIME_BETWEEN_TEST_PRINTING = 2
    ENABLE_MISSING_LABEL = False
    MAX_MISSING_LABEL_ENGINEERING = 30
