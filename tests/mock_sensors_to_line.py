import random
import time
from time import sleep
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions

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

        for i in range(1, 86400):
            gyro_line = f"gyro x={random.uniform(-5, 5)},y={random.uniform(-5, 5)},z={random.uniform(-5, 5)} {time.time_ns()}"
            accel_line = f"accel x={random.uniform(-5, 5)},y={random.uniform(-5, 5)},z={random.uniform(-5, 5)} {time.time_ns()}"
            write_api.write(bucket=bucket, org=org, record=gyro_line)
            write_api.write(bucket=bucket, org=org, record=accel_line)
            print(f"WRITE: {gyro_line}")
            print(f"WRITE: {accel_line}")
            sleep(1)


if __name__ == '__main__':
    main()
