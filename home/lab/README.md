
## Linux bluetooth


```sh
bluetoothctl power on
bluetoothctl agent on
bluetoothctl scan on  # listens for new devices to get their MAC

# not sure of the ordering here
bluetoothctl connect  "4A:D4:99:19:7D:23"
bluetoothctl trust    "4A:D4:99:19:7D:23"
bluetoothctl pair     "4A:D4:99:19:7D:23"

bluetoothctl paired-devices
```



### LD2410B

https://github.com/amandel/esphome-ld2410/blob/main/ld2410.h

The module IO level is 3.3V. The default baud rate of the serial port is 256000, 1 stop bit, noparity bit

doesn't pair..


### FT232H

https://learn.adafruit.com/adafruit-ft232h-breakout/serial-uart

