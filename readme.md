# Govee BLE Light Controller App (Goblee)

A Python desktop application to control Govee Bluetooth LED light strips over BLE.

---

## Features

- Turn Govee lights **ON** and **OFF** successfully  
- **Note:** Setting custom RGB colors is **not fully functional yet**  

---

## Requirements

- Python 3.8 or higher  
- Bluetooth adapter compatible with BLE or a BLE compatible bluetooth card (I believe most modern computers have BLE?)
- Windows, macOS, or Linux with Bluetooth support  

---

## Dependencies

This app uses the following Python packages:  

- [`bleak`](https://pypi.org/project/bleak/) - Cross-platform Bluetooth Low Energy client  
- [`asyncio`](https://docs.python.org/3/library/asyncio.html) - For asynchronous programming (comes with Python)
- [`threading`](https://docs.python.org/3/library/threading.html)
- [`tk`](https://docs.python.org/3/library/tkinter.html) - GUI
- [`device`](https://pypi.org/project/device/)
- [`govee-api-ble `](https://github.com/softgrass/govee-api-ble) - The one thing that connects everything together (Govee wise)

To install dependencies, run:

```bash
pip install bleak asyncio threading tk device govee-api-ble
````

---

## Setup & Usage

1. Clone or download this repository to your local machine.

2. Ensure your Govee BLE device is powered on and in range.

3. Run the app:

```bash
python server.py
```

4. Use the provided commands in the app interface or API to turn lights on/off, set brightness, or activate scenes.

---

## Known Limitations

* **Setting custom RGB colors does not work reliably yet** due to BLE characteristic differences in some devices.
* The app currently assumes the write handle `0x13` is correct; some devices may require different handles.
* BLE support and behavior may vary by platform and adapter.

---

## Troubleshooting

* If the app cannot find your device or fails to write commands, verify Bluetooth is enabled and the device is in pairing mode.
* Use a BLE scanner app (e.g., nRF Connect) to confirm your device’s services and handles.
* Errors about missing characteristic UUIDs likely mean the handle needs adjustment in the code.
---

## License

This project is licensed under the MIT License.

---

Feel free to contribute or open issues if you encounter bugs or have feature requests!

---

*Happy lighting!*
