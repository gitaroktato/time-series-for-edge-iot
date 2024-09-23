#!/usr/bin/env python3
from lib.downsampling import Downsampler
from lib.sensors import Reader
from influxdb_client import InfluxDBClient
from influxdb_client.rest import ApiException
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions, WriteApi

# InfluxDB credentials
bucket = "sensors"
org = "docs"
token = "WAlkSZnxrLK3dRGDKHKSbfmVPFOCS3iX_oPEvsOb-_0cVR7LacuKh3KWwCHxqNFECwfQir5GinSBOFJ7ubjA5A=="
# Store the URL of your InfluxDB instance
url = "http://localhost:8086"


def write_and_print(write_api: WriteApi, line: str) -> None:
    write_api.write(bucket=bucket, org=org, record=line)
    print(line)

def main() -> None:
    downsampler = Downsampler(15)
    sensor_reader = Reader()
    with InfluxDBClient(
       url=url,
       token=token,
       org=org
    ) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        while True:
            if sensor_reader.has_lines():
                try:
                    line, is_debug_message = sensor_reader.read_line()
                    if is_debug_message:
                        print(f"DEBUG - {line}")
                    else:
                        downsampler.call(lambda: write_and_print(write_api, line))
                except (ApiException, UnicodeDecodeError):
                    print(f"Failed to write - {line}")

if __name__ == '__main__':
    main()
