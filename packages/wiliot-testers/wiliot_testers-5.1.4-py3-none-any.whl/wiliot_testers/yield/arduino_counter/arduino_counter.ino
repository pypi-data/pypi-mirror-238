// Counter code which uses panasonic ex-23-c5 sensor
// to interact with this code please look for CounterThread under pywiliot->wiliot->wiliot_testers->tester_utils

String config_time_cmd = "*time_btwn_triggers ";
#define TIME_CMD_SIZE 20

const int input = 2; // This is where the input is fed.
int pulse = 0; // Variable for saving pulses count.
unsigned long time_btwn_triggers_ms = 0; // Fixed the variable name typo
bool last_gpio_state = false;
unsigned long trigger_time = millis();  // the time when the first trigger was detected

void setup(){
  pinMode(input, INPUT);

  Serial.begin(1000000);
  Serial.println(F("No pulses yet...")); // Message to send initially (no pulses detected yet).
}

void loop() {
  if (Serial.available() > 0) {
    delay(10);  // add delay to make sure all bytes were received
    String incoming_data = Serial.readString();
    if (incoming_data.substring(0, TIME_CMD_SIZE) == config_time_cmd) {
      time_btwn_triggers_ms = incoming_data.substring(TIME_CMD_SIZE).toInt();
      Serial.print("Max movement time was set to ");
      Serial.print(time_btwn_triggers_ms);
      Serial.println("[sec]");
      time_btwn_triggers_ms *= 1000; // Converting seconds to milliseconds
    }
  }

  bool cur_gpio_state = digitalRead(input);

  if (cur_gpio_state != last_gpio_state) {
    unsigned long current_time = millis();

    last_gpio_state = cur_gpio_state;

    if (cur_gpio_state == true) {
        if (current_time - trigger_time > time_btwn_triggers_ms) {
            pulse++;
            Serial.print(pulse); 
            Serial.println(" pulses detected.");
            trigger_time = current_time; // Update trigger time to the current time
        }
    }
  }
  delay(50); // Delay for stability 50 ms.
}
