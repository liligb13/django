Serial -> HTTP forwarder (for Arduino connected via USB)

Requirements
-----------
- Python 3.8+
- pip install pyserial requests

Usage
-----
1. Connect your Arduino to USB (note the COM port in Windows Device Manager, e.g., COM3).
2. Make sure Arduino sketch prints a JSON object per line like:
   {"serial":"ARDUINO1","valor":23.45,"humedad":45.2}
3. Run the forwarder (example for Windows PowerShell):

   ```powershell
   python tools/serial_forwarder.py --port COM3 --baud 9600 --url http://127.0.0.1:8000/rest/arduino/
   ```

Notes
-----
- The script attempts to extract JSON if there is debug text around it (handy if the Arduino prints additional messages).
- The forwarder will retry if the serial port disconnects.
- The script logs basic activity to the console; you can run it as a background job or service if needed.
