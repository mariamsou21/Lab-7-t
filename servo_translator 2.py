"""servo_translator.py - Lab 6

Converts an angle in degrees to the duty_u16 value for a hobby servo
(50 Hz PWM, 0-180 degrees). Importing this file does not touch any hardware.
"""

MIN = 1638    # duty_u16 value for 0 degrees
MAX = 8192    # duty_u16 value for 180 degrees
DEG = (MAX - MIN) / 180   # duty_u16 units per degree


def translate(angle: float) -> int:
    """Convert an angle in degrees to the matching duty_u16 value.

    The angle is clamped to 0-180 so the servo is never driven out of range.
    See https://docs.micropython.org/en/latest/library/machine.PWM.html
    """
    angle = max(0, min(180, angle))
    return int(angle * DEG + MIN)


if __name__ == "__main__":
    # Quick manual test (only runs when this file is run directly)
    print(translate(0), translate(90), translate(180), translate(999))
