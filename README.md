# OWON OW18B Bluetooth BLE Connector / Logger 

<img src="https://github.com/rbelnienk/OWON-OW18B-BLE-Connector/blob/main/OW18B.jpg" width="250">


This Script will connect to your OWON OW18B Multimeter via Windows machine Bluetooth. 

Currently only Supports Volts and mVolts measurement, feel free to add more. 

Before use make sure you install bleak or simply use the requirements.txt:

`pip install bleak`

The script prints out the values to the Terminal. Make sure your device is turned on and bluetooth is enabled before you execute the file.

__BLE Characteristic:__

The measurement Values are Published on the Notify Characteristic:

`UUID: 0000fff4-0000-1000-8000-00805f9b34fb`

__Protocol:__

Protocol is really simple. For each Measurement you will recieve 5 Bytes. 

`34 240 4 0 0 0`

First Byte represents the Measurement Method e.g. 34 --> Volts Measurement.

Last two Bytes contain the Measurement Value.
Last Byte from 0-127 counts the overflow of the 4th Byte. 
If last Byte is between 128-256 the value is negative.

