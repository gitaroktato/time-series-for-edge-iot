#!/usr/bin/env python3
import serial
import time
from time import sleep
from influxdb_client import InfluxDBClient
from influxdb_client.rest import ApiException
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions

# InfluxDB credentials
bucket = "sensors"
org = "docs"
token = "WAlkSZnxrLK3dRGDKHKSbfmVPFOCS3iX_oPEvsOb-_0cVR7LacuKh3KWwCHxqNFECwfQir5GinSBOFJ7ubjA5A=="
# Store the URL of your InfluxDB instance
url = "http://localhost:8086"

def main():
    with InfluxDBClient(
       url=url,
       token=token,
       org=org
    ) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').rstrip()
                    write_api.write(bucket=bucket, org=org, record=line)
                    print(line)
                except (ApiException, UnicodeDecodeError):
                    print(f"Failed to write - {line}")

if __name__ == '__main__':
    main()
