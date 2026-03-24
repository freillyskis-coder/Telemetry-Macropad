code.py
# --- Imports ---
import board
import busio
import time
import neopixel
import digitalio
import math
from adafruit_mpu6050 import MPU6050
from adafruit_ssd1306 import SSD1306_I2C
# --- I2C Setup ---
i2c = busio.I2C(board.SCL, board.SDA)

# --- OLED Setup ---
oled = SSD1306_I2C(128, 32, i2c)

# --- Accelerometer Setup ---
mpu = MPU6050(i2c)

# --- LED Setup ---
pixels = neopixel.NeoPixel(board.D2, 4, brightness=0.3, auto_write=False)

# --- Button Setup ---
btn_mode = digitalio.DigitalInOut(board.D3)
btn_mode.direction = digitalio.Direction.INPUT
btn_mode.pull = digitalio.Pull.UP

btn_cal = digitalio.DigitalInOut(board.D4)
btn_cal.direction = digitalio.Direction.INPUT
btn_cal.pull = digitalio.Pull.UP

btn_max = digitalio.DigitalInOut(board.D5)
btn_max.direction = digitalio.Direction.INPUT
btn_max.pull = digitalio.Pull.UP
# --- State Variables ---

# Display modes: 0 = traction circle, 1 = acceleration numbers
display_mode = 0

# Units: 0 = g's, 1 = m/s²
units = 0

# Brightness levels (0.1 to 1.0)
brightness_levels = [0.1, 0.3, 0.6, 1.0]
brightness_index = 1

# Acceleration tracking
max_accel = 0.0
frozen_max = False
zero_offset = [0.0, 0.0, 0.0]

# Button timing (for long press detection)
LONG_PRESS_TIME = 0.8
btn_mode_held = False
btn_cal_held = False
btn_max_held = False
btn_mode_press_time = 0
btn_cal_press_time = 0
btn_max_press_time = 0
# --- LED Position Map ---
# Matches KiCad wiring: D1=top, D2=left, D3=bottom, D4=right
LED_TOP = 0
LED_BOTTOM = 2
LED_LEFT = 1
LED_RIGHT = 3
# --- Acceleration to Color ---
def accel_to_color(strength, is_max):
    if is_max:
        return (128, 0, 128)  # Purple for max
    elif strength > 0.75:
        return (255, 0, 0)    # Red
    elif strength > 0.5:
        return (255, 165, 0)  # Orange/Yellow
    elif strength > 0.25:
        return (0, 255, 0)    # Green
    else:
        return (0, 0, 0)      # Off
# --- Update LEDs ---
def update_leds(x, y, max_accel):
    # Turn all LEDs off to start
    pixels.fill((0, 0, 0))
    
    # Calculate total acceleration strength (0.0 to 1.0)
    total = max_accel if max_accel > 0 else 1.0
    
    # Forward/backward (Y axis)
    if y > 0.1:
        strength = min(y / total, 1.0)
        is_max = (y >= max_accel)
        pixels[LED_TOP] = accel_to_color(strength, is_max)
    elif y < -0.1:
        strength = min(abs(y) / total, 1.0)
        is_max = (abs(y) >= max_accel)
        pixels[LED_BOTTOM] = accel_to_color(strength, is_max)
    
    # Left/right (X axis)
    if x > 0.1:
        strength = min(x / total, 1.0)
        is_max = (x >= max_accel)
        pixels[LED_RIGHT] = accel_to_color(strength, is_max)
    elif x < -0.1:
        strength = min(abs(x) / total, 1.0)
        is_max = (abs(x) >= max_accel)
        pixels[LED_LEFT] = accel_to_color(strength, is_max)
    
    pixels.show()
# --- Button Handler ---
def check_buttons():
    global display_mode, units, brightness_index, max_accel, frozen_max, zero_offset
    global btn_mode_held, btn_cal_held, btn_max_held
    global btn_mode_press_time, btn_cal_press_time, btn_max_press_time

    current_time = time.monotonic()

    # --- Button 1 (Mode) ---
    if not btn_mode.value:  # Button is pressed
        if not btn_mode_held:
            btn_mode_held = True
            btn_mode_press_time = current_time
    else:  # Button is released
        if btn_mode_held:
            held_duration = current_time - btn_mode_press_time
            if held_duration >= LONG_PRESS_TIME:
                # Long press - cycle brightness
                brightness_index = (brightness_index + 1) % len(brightness_levels)
                pixels.brightness = brightness_levels[brightness_index]
            else:
                # Short press - cycle display mode
                display_mode = (display_mode + 1) % 2
            btn_mode_held = False

    # --- Button 2 (Calibration) ---
    if not btn_cal.value:
        if not btn_cal_held:
            btn_cal_held = True
            btn_cal_press_time = current_time
    else:
        if btn_cal_held:
            held_duration = current_time - btn_cal_press_time
            if held_duration >= LONG_PRESS_TIME:
                # Long press - switch units
                units = (units + 1) % 2
            else:
                # Short press - zero calibration
                x, y, z = mpu.acceleration
                zero_offset[0] = x
                zero_offset[1] = y
                zero_offset[2] = z
            btn_cal_held = False

    # --- Button 3 (Max) ---
    if not btn_max.value:
        if not btn_max_held:
            btn_max_held = True
            btn_max_press_time = current_time
    else:
        if btn_max_held:
            held_duration = current_time - btn_max_press_time
            if held_duration >= LONG_PRESS_TIME:
                # Long press - reset max acceleration
                max_accel = 0.0
                frozen_max = False
            else:
                # Short press - freeze/unfreeze max
                frozen_max = not frozen_max
            btn_max_held = False
# --- Draw Acceleration Numbers ---
def draw_numbers(x, y, z):
    oled.fill(0)  # Clear screen
    
    if units == 0:  # g's
        oled.text("X: {:.2f}g".format(x), 0, 0, 1)
        oled.text("Y: {:.2f}g".format(y), 0, 11, 1)
        oled.text("Z: {:.2f}g".format(z), 0, 22, 1)
    else:  # m/s²
        oled.text("X: {:.2f}m/s2".format(x), 0, 0, 1)
        oled.text("Y: {:.2f}m/s2".format(y), 0, 11, 1)
        oled.text("Z: {:.2f}m/s2".format(z), 0, 22, 1)
    
    oled.show()

# --- Draw Traction Circle ---
def draw_traction_circle(x, y, max_accel):
    oled.fill(0)  # Clear screen
    
    # Circle center and radius
    cx = 64
    cy = 16
    radius = 14
    
    # Draw the outer circle
    for angle in range(0, 360, 5):
        px = int(cx + radius * math.cos(math.radians(angle)))
        py = int(cy + radius * math.sin(math.radians(angle)))
        oled.pixel(px, py, 1)
    
    # Draw crosshairs
    oled.line(cx - radius, cy, cx + radius, cy, 1)  # Horizontal
    oled.line(cx, cy - radius, cx, cy + radius, 1)  # Vertical
    
    # Draw the dot representing current acceleration
    total = max_accel if max_accel > 0 else 1.0
    dot_x = int(cx + (x / total) * radius)
    dot_y = int(cy - (y / total) * radius)
    
    # Keep dot inside circle
    dot_x = max(cx - radius, min(cx + radius, dot_x))
    dot_y = max(cy - radius, min(cy + radius, dot_y))
    
    # Draw dot as a small cross
    oled.pixel(dot_x, dot_y, 1)
    oled.pixel(dot_x + 1, dot_y, 1)
    oled.pixel(dot_x - 1, dot_y, 1)
    oled.pixel(dot_x, dot_y + 1, 1)
    oled.pixel(dot_x, dot_y - 1, 1)
    
    # Show max acceleration value at bottom
    oled.text("Max:{:.2f}g".format(max_accel), 0, 25, 1)
    
    oled.show()
# --- Main Loop ---
while True:
    # --- Read Accelerometer ---
    x_raw, y_raw, z_raw = mpu.acceleration  # Always in m/s²
    
    # Apply zero offset
    x_raw -= zero_offset[0]
    y_raw -= zero_offset[1]
    z_raw -= zero_offset[2]
    
    # Convert units
    if units == 0:  # g's
        x = x_raw / 9.81
        y = y_raw / 9.81
        z = z_raw / 9.81
    else:  # m/s²
        x = x_raw
        y = y_raw
        z = z_raw
    
    # --- Update Max Acceleration ---
    if not frozen_max:
        current_accel = (x**2 + y**2) ** 0.5
        if current_accel > max_accel:
            max_accel = current_accel
    
    # --- Update Display ---
    if display_mode == 0:
        draw_traction_circle(x, y, max_accel)
    else:
        draw_numbers(x, y, z)
    
    # --- Update LEDs ---
    update_leds(x, y, max_accel)
    
    # --- Check Buttons ---
    check_buttons()
    
    # --- Small delay ---
    time.sleep(0.05)