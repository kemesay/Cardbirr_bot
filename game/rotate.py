from PIL import Image, ImageDraw
import math

# Set animation parameters
duration = 10  # Duration in seconds
frames_per_second = 5
total_frames = duration * frames_per_second
radius = 40  # Radius of the spinning circle
center = (100, 100)  # Center coordinates of the image

# Define four colors and their respective names
colors = [
    {"name": "Red", "color": (255, 0, 0)},
    {"name": "Green", "color": (0, 255, 0)},
    {"name": "Blue", "color": (0, 0, 255)},
    {"name": "Yellow", "color": (255, 255, 0)}
]

# Create a list to store the frames
frames = []

# Create a function to generate each frame
def create_frame(frame_num):
    frame = Image.new("RGBA", (200, 200), (255, 255, 255, 255))  # Create a transparent image
    draw = ImageDraw.Draw(frame)
    
    angle = (frame_num / total_frames) * 360  # Calculate the angle for rotation
    color_index = frame_num % len(colors)  # Cycle through the color list
    
    # Calculate the position of the circle
    x = center[0] + int(radius * math.cos(math.radians(angle)))
    y = center[1] + int(radius * math.sin(math.radians(angle)))
    
    # Draw the circle with the current color
    draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=colors[color_index]["color"])
    
    # Write the color name outside the circle within its color-bound
    text = colors[color_index]["name"]
    text_width, text_height = draw.textsize(text)
    text_x = x - text_width / 2
    text_y = y - text_height / 2
    draw.text((text_x, text_y), text, fill=(255, 255, 255))
    
    return frame

# Create the frames
for frame_num in range(total_frames):
    frame = create_frame(frame_num)
    frames.append(frame)

# Save the frames as an animated GIF
frames[0].save("colorful_spinning_circle.gif", save_all=True, append_images=frames[1:], duration=int(1000 / frames_per_second), loop=0)
