import asyncio
from bleak import BleakClient,  BleakGATTCharacteristic, BleakScanner, BleakError
import time

ADDRESS = ""
MODEL_NBR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

#write a simple text file with the current value, this can easily be imported to OBS (update rate is not that good though)
def writeOBSfile(value):
    f = open(r"C:\Users\reneb\Documents\ble_stream.txt", "w")
    f.write(value)
    f.close()
    

def decode(sender: BleakGATTCharacteristic, data: bytearray):
    if data[0] == 34:
        #decode positive Volts
        if data[5] < 128:
            value = str((data[5]*256 + data[4])/100) + " V"
            writeOBSfile(value)
            print(value)
            
        #decode negative Volts
        if data[5] >= 128:
            value = ("-" + str(((data[5]-128)*256 + data[4])/100) + " V")
            writeOBSfile(value)
            print(value)
             
        
    if data[0] == 25:
        #decode positive milli Volts
        if data[5] < 128:
            value = (str((data[5]*256 + data[4])/10)+ " mV")
            writeOBSfile(value)
            print(value)
    	#decode negative milli Volts 
        if data[5] >= 128:
            value = ("-"+ str(((data[5]-128)*256 + data[4])/10)+ " mV")
            writeOBSfile(value)
            print(value)
        
    else: 
        # data[0] represents the Measurement Type (e.g. Volts, mVolts, Ohms etc.) 
        # last two bytes data[4] & data[5] represent the measurement value 
        # data[5] counts the overflow of byte data[4] pos. values from 0-127 negative values from 128-256
        print(f"{data[0]}",f"{data[1]}",f"{data[2]}",f"{data[3]}",f"{data[4]}",f"{data[5]}")
        

async def main():
    print('Looking for Device "BDM"')
    print('Make sure your Device is turned on and Bluetooth is enabled')
    print("scanning for 5 seconds, please wait...")
    devices = await BleakScanner.discover(return_adv=True)

    for d, a in devices.values():
        if d.name == "BDM": #change the name in case your device name differs
            ADDRESS = d.address
        else:
            ADDRESS = "A5:B3:C2:20:0A:D8"

    async with BleakClient(ADDRESS) as client:
        if not client:
            raise BleakError(f"Device not found")
        print("Press any Key + Enter to stop the BLE stream")
        await asyncio.sleep(5)

        flag = True

        while flag:
            
            if flag:
                value = await client.start_notify(MODEL_NBR_UUID,decode)
            
            await asyncio.sleep(3)
            if input() is not None:
                flag = False
                print("Closing app please wait, there might be some values still coming through")
                time.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())



