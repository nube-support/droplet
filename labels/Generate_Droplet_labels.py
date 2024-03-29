from datetime import datetime
import barcode, subprocess, os
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

# Get the directory of the current script and parent
script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)

dpi = 360


def generate_barcode(barcode_text):
    barcode_type = barcode.get_barcode_class('code128')  # Using Code 39 format
    bc = barcode_type(barcode_text, writer=ImageWriter())
    options = {"module_height": 10, "font_size": 10, "text_distance": 4, "quiet_zone": 0.9, "module_width": 0.2}

    label = bc.render(options)


    width, height = label.size

    left, top, right, bottom = 0, 10, width, height - 29
    label = label.crop((left, top, right, bottom))

    label.save(os.path.join(parent_directory, 'images', 'barcode_raw.png'))

    # Convert mm to pixels

    width_px = int((33 / 25.4) * dpi)
    height_px = int((12 / 25.4) * dpi)

    # Create blank image
    img = Image.new("RGB", (width_px, height_px), "white")

    # Assuming cropped_img is already defined and has size
    label_width, label_height = label.size

    # Calculate position to center
    x_offset = (width_px - label_width) // 2
    y_offset = (height_px - label_height) // 2

    # Paste cropped_img centered in img
    img.paste(label, (x_offset, y_offset))

    img.save(os.path.join(parent_directory, 'images', 'barcode.png'))


def generate_label(lines):
    width_mm, height_mm = 48, 12
    width_px = int((width_mm * dpi) / 25.4)
    height_px = int((height_mm * dpi) / 25.4)

    # Create a new white image
    img = Image.new('RGB', (width_px, height_px), 'white')
    draw = ImageDraw.Draw(img)

    # Load the image you want to add
    barcode = Image.open(os.path.join(parent_directory, 'images', 'barcode.png'))
    position = (0, 0)
    img.paste(barcode, position)

    # Define text and position
    number_of_lines = len(lines)
    size = height_px / (number_of_lines )

    font = ImageFont.truetype('DejaVuSansMono', int(size-10))
    font_size = size

    line_height = font_size  # Use font size as line height

    for i, line in enumerate(lines):
        offset = int(size / 2)
        x = 470
        y = i * line_height -2

        # Draw text
        draw.text((x, y), line, (0, 0, 0), font=font)  # Black text

    img.save(os.path.join(parent_directory, 'images', 'product_label.png'))

def main(make, model, variant, barcode_text, hardware_version, software_version, print_flag):
    model = f"MN:{make}-{model}-{variant}"
    hw = f"HW:V{hardware_version}"
    sw = f"SW:V{software_version}"
    today_date = datetime.today().strftime('%Y/%m/%d')
    lines = [model, hw, sw, today_date]

    generate_barcode(barcode_text)
    generate_label(lines)

if __name__ == '__main__':
    main()