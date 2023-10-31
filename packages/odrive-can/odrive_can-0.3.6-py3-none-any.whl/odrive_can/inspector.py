#!/usr/bin/env python3
"""
 Inspect and decode ODrive CAN messages

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

import can
import odrive_can

TIMEOUT = 1.0


def receive_and_decode(bus: can.Bus, dbc):
    while True:
        msg = bus.recv(TIMEOUT)

        if msg is None:
            raise TimeoutError("Timeout occurred, no message.")

        axis_id = odrive_can.get_axis_id(msg)

        if msg.is_remote_frame:
            # RTR messages are requests for data, they don't have a data payload
            db_msg = dbc.get_message_by_frame_id(msg.arbitration_id)
            print(f"Axis{axis_id} RTR: {db_msg.name}")
            continue

        try:
            # Attempt to decode the message using the DBC file
            decoded_message = dbc.decode_message(msg.arbitration_id, msg.data)
            print(f"Axis{axis_id} Message: {decoded_message}")
        except KeyError:
            # If the message ID is not in the DBC file, print the raw message
            print(f"Axis{axis_id} Raw Message: {msg}")


def main(channel: str = "vcan0"):
    # Load the DBC file
    dbc = odrive_can.get_dbc()

    bus = can.Bus(channel=channel, bustype="socketcan", receive_own_messages=True)

    try:
        receive_and_decode(bus, dbc)
    except KeyboardInterrupt:
        print("Stopped")
    except TimeoutError as error:
        print(error)
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
