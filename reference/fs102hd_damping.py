#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

安装依赖：python -m pip install pyserial
运行示例：python fs102hd_damping.py --port COM3

"""

import argparse
import struct
import sys
import time

import serial


# 舵机 ID：阻尼模式下的保持功率（mW）
DAMPING_POWER = {
    0: 100,
    1: 100,
    3: 100,
    4: 100,
    5: 100,
    6: 100,
}


def damping_packet(servo_id, power):
    """"""
    if not 0 <= servo_id <= 253:
        raise ValueError("舵机 ID 必须在 0～253 之间")
    if not 0 <= power <= 65535:
        raise ValueError("功率必须能表示为 uint16（0～65535）")
    frame = b"\x12\x4c\x09\x03" + struct.pack("<BH", servo_id, power)
    return frame + bytes([sum(frame) & 0xFF])


def main():
    parser = argparse.ArgumentParser(description="为指定 FS-102HD 舵机开启阻尼模式")
    parser.add_argument("--port", required=True, help="串口，例如 COM3 或 /dev/ttyUSB0")
    parser.add_argument("--baudrate", type=int, default=1000000, help="舵机当前波特率，默认 1000000")
    args = parser.parse_args()

    try:
        with serial.Serial(
            port=args.port,
            baudrate=args.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1,
            write_timeout=1,
        ) as uart:
            for servo_id, power in DAMPING_POWER.items():
                packet = damping_packet(servo_id, power)
                if uart.write(packet) != len(packet):
                    raise serial.SerialException("指令未完整写入串口")
                uart.flush()
                print(f"已发送：{servo_id} 号舵机，阻尼功率 {power} mW")
                time.sleep(0.03)
    except (serial.SerialException, OSError, ValueError) as exc:
        print(f"发送失败：{exc}", file=sys.stderr)
        return 1

    print("全部指令已发送；请在设备上确认实际阻尼效果。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
