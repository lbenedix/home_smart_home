1. Install [esptool.py](https://github.com/espressif/esptool)
2. Download [ESPEasy](https://github.com/letscontrolit/ESPEasy/releases)
3. ```bash
   # find tty of Wemos
   ls -lah /dev/tty.*  | grep usbserial
   
   # clear flash
   esptool.py --port /dev/tty.usbserial-1411320 erase_flash
   
   # flash ESPEasy
   esptool.py --port /dev/tty.usbserial-1411320 write_flash -fs 4MB -fm dout 0x00000 ESP_Easy_mega_20200801_normal_ESP8266_4M1M.bin
    ```
4. connect to the ESP_Easy WiFi which will prompt you with a connection Wizzard to connect the ESP 
5. 
