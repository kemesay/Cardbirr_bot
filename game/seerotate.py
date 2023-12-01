from PIL import Image, ImageSequence
import time
import sys

# Load the animated GIF
animated_gif = Image.open("spinning_circle.gif")

# Get the individual frames of the animation
frames = [frame.copy() for frame in ImageSequence.Iterator(animated_gif)]

try:
    while True:
        for frame in frames:
            sys.stdout.write("\r")  # Move the cursor to the beginning of the line
            sys.stdout.flush()
            sys.stdout.buffer.write(frame.tobytes())  # Display the frame as bytes
            time.sleep(0.1)  # Adjust the sleep duration for the desired speed
except KeyboardInterrupt:
    sys.stdout.write("\nAnimation stopped.\n")
