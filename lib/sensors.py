import serial

class Reader:
    __line_protocol_prefixes = ("controller", "accel", "gyro")
    def __init__(
            self,
            device: str = '/dev/ttyACM0',
            baud_rate: int = 38400,
            timeout: int = 1
        ) -> None:
        self.__serial = serial.Serial(device, baud_rate, timeout=timeout)
        self.__serial.reset_input_buffer()

    def has_lines(self) -> bool:
        return self.__serial.in_waiting > 0
    
    def read_line(self) -> tuple[str, bool]:
        line = self.__serial.readline().decode('utf-8').rstrip()
        return (line, not any(map(line.startswith, self.__line_protocol_prefixes)))
