"""plotter_control.py - Lab 7: Plotter Control (SED1115)

Calling structure:
    G-Code file -> parser -> command interpreter -> servo translator -> servos
"""
from machine import Pin, PWM
import time

from servo_translator import translate   # Lab 6
from gcode_parser import parse_file

# ---- Configuration ---------------------------------------------------------
GCODE_FILE = "circle.gcode"   # line.gcode, square.gcode, circle_and_square.gcode

SHOULDER_PIN = 0              # J1
ELBOW_PIN = 1                 # J2
WRIST_PIN = 2                 # J3
PWM_FREQ = 50

SHOULDER_OFFSET = 0           # small calibration offsets (degrees)
ELBOW_OFFSET = 0

WRIST_UP = 0
WRIST_DOWN = 30

MOVE_DELAY = 0.02             # seconds after each G1 move
PEN_DELAY = 0.5               # seconds to let the pen finish moving up/down


# ---- Servo setup / control -------------------------------------------------
def setup_servos():
    """Create the three PWM outputs and return them in a dict."""
    servos = {}
    for name, pin in (("shoulder", SHOULDER_PIN),
                      ("elbow", ELBOW_PIN),
                      ("wrist", WRIST_PIN)):
        pwm = PWM(Pin(pin), freq=PWM_FREQ)
        servos[name] = pwm
    return servos


def move(servo, deg):
    """Move a servo to an angle (always through translate())."""
    servo.duty_u16(translate(deg))


def disable_servos(servos):
    """Stop the PWM signal on every servo (M18)."""
    for servo in servos.values():
        servo.duty_u16(0)


# ---- Command interpreter ---------------------------------------------------
def execute_command(cmd, servos):
    """Run one parsed command. Returns False when the program should stop."""
    name = cmd["command"]
    params = cmd["params"]

    if name == "G1":
        if "S" in params:
            move(servos["shoulder"], params["S"] + SHOULDER_OFFSET)
        if "E" in params:
            move(servos["elbow"], params["E"] + ELBOW_OFFSET)
        time.sleep(MOVE_DELAY)
    elif name == "M3":                       # pen down
        move(servos["wrist"], WRIST_DOWN)
        time.sleep(PEN_DELAY)
    elif name == "M5":                       # pen up
        move(servos["wrist"], WRIST_UP)
        time.sleep(PEN_DELAY)
    elif name == "M18":                      # disable servos and stop
        print("Read stop code.")
        return False
    else:
        print("Parsing error: unknown command \"%s\"." % name)
    return True


def run(commands, servos):
    """Execute every command in order until done or M18 is reached."""
    for cmd in commands:
        if not execute_command(cmd, servos):
            break


# ---- Main ------------------------------------------------------------------
def main():
    servos = setup_servos()
    move(servos["wrist"], WRIST_UP)          # start with the pen lifted
    time.sleep(PEN_DELAY)
    try:
        run(parse_file(GCODE_FILE), servos)
    finally:
        disable_servos(servos)               # never leave servos stalled


if __name__ == "__main__":
    main()
