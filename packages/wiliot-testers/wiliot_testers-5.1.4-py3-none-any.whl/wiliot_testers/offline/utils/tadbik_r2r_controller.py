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
from wiliot_testers.offline.modules.offline_utils import *
from wiliot_core import WiliotGateway


class tadbikR2rController():
    def __init__(self):
        self.my_gpio = R2rGpio()
        self.GwObj = WiliotGateway(auto_connect=True, logger_name='root')
        self.GwObj.reset_gw()
        time.sleep(5)
        self.GwObj.config_gw(energy_pattern_val=18, pl_delay_val=0, start_gw_app=False, with_ack=True)
        self.GwObj.write('!pl_gw_config 1')  # to enable production line trigger
    
    def stop(self):
        self.my_gpio.gpio_state(3, "OFF")
    
    def start(self):
        self.my_gpio.gpio_state(3, "ON")
    
    def failed(self):
        self.my_gpio.pulse(2, 50)
    
    def passed(self):
        self.my_gpio.pulse(1, 50)
    
    def set_missing_label_state(self, state="ON"):
        self.my_gpio.gpio_state(4, state)
    
    def toggle_direction(self):
        self.my_gpio.pulse(5, 50)
    
    def restart(self):
        self.stop()
        self.start()
    
    def is_r2r_moved(self):
        gw_answer = self.GwObj.read_specific_message(msg="Start Production Line GW", read_timeout=1)
        if gw_answer == '':
            return False
        else:
            self.GwObj.write('!cancel', with_ack=True)
            return True
    
    def rewind(self, max_missing_labels=6, num_tags=0):
        assert max_missing_labels > 0, f"max missing labels must be bigger than zero, got {max_missing_labels}"
        done = False
        missing_label_counter = 0
        self.GwObj.start_continuous_listener()
        self.restart()
        self.toggle_direction()
        tags_counter = 0
        missing_labels_stop = False
        while not done:
            self.passed()
            if not self.is_r2r_moved():
                missing_label_counter += 1
                print(f"missing labels {missing_label_counter}")
                if missing_label_counter >= max_missing_labels:
                    print(f"Rewind finished after {missing_label_counter} missing labels")
                    missing_labels_stop = True
                    done = True
                else:
                    self.restart()
                    self.toggle_direction()
            else:
                tags_counter += 1
                missing_label_counter = 0
                if num_tags != 0 and tags_counter >= num_tags:
                    done = True
                    print(f"Rewind finished after {tags_counter} tags")
                
                if tags_counter % 100 == 0:
                    print('rewinding {} tags'.format(tags_counter))
        
        if missing_labels_stop:
            print("start searching for first tag")
            missing_label_counter = 0
            while not self.is_r2r_moved():
                self.restart()
                self.passed()
                missing_label_counter += 1
                print(f"missing labels {missing_label_counter}")
                if missing_label_counter > 100:
                    print("Start of reel wasn't found for 100 tags!")
                    break
            
            print("Roll to first tag:")
            locations_from_sensor_to_dut = 8
            for num_tags in range(locations_from_sensor_to_dut):
                self.restart()
                self.passed()
        self.GwObj.close_port(is_reset=True)
        self.GwObj.stop_continuous_listener()
        self.stop()
        self.my_gpio.__del__()


if __name__ == '__main__':
    tadbik_r2r_controller = tadbikR2rController()
    tadbik_r2r_controller.rewind(max_missing_labels=10, num_tags=1000)
    print("Done!")
