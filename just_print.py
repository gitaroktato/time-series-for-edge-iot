#!/usr/bin/env python3
from lib.downsampling import Downsampler
from lib.sensors import Reader

def main() -> None:
    downsampler = Downsampler(10)
    sensor_reader = Reader()
    while True:
        if sensor_reader.has_lines():
            try:
                line, is_debug_message = sensor_reader.read_line()
                if is_debug_message:
                    print(f"DEBUG - {line}")
                else:
                    downsampler.print(line)
            except (UnicodeDecodeError):
                print(f"Failed to write - {line}")

if __name__ == '__main__':
    main()
