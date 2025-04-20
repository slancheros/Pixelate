import gradio as gr
from PIL import Image, ImageDraw, ImageFont

def full_pixel_art_process_custom_grid(
    image_path,
    output_path,
    grid_width=32,
    grid_height=32,
    pixel_size=32,
    num_colors=8,
    add_grid=True
):
    image = Image.open(image_path)
    image_small = image.resize((grid_width, grid_height), resample=Image.Resampling.BILINEAR)
    image_small = image_small.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    pixelated_image = image_small.resize(
        (grid_width * pixel_size, grid_height * pixel_size),
        resample=Image.Resampling.NEAREST
    )

    if add_grid:
        draw = ImageDraw.Draw(pixelated_image)
        font_size = max(10, pixel_size // 3)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        for x in range(0, grid_width * pixel_size, pixel_size):
            draw.line((x, 0, x, grid_height * pixel_size), fill="gray", width=1)
            draw.text((x + 2, 2), str(x // pixel_size), fill="black", font=font)

        for y in range(0, grid_height * pixel_size, pixel_size):
            draw.line((0, y, grid_width * pixel_size, y), fill="gray", width=1)
            draw.text((2, y + 2), str(y // pixel_size), fill="black", font=font)

    pixelated_image.save(output_path)
    return output_path

def process_image(image, grid_width, grid_height, pixel_size, num_colors):
    output_path = "output.png"
    return full_pixel_art_process_custom_grid(
        image_path=image,
        output_path=output_path,
        grid_width=grid_width,
        grid_height=grid_height,
        pixel_size=pixel_size,
        num_colors=num_colors,
        add_grid=True
    )[0]

demo = gr.Interface(
    fn=process_image,
    inputs=[
        gr.Image(type="filepath", label="Upload Image"),
        gr.Slider(8, 100, value=32, step=1, label="Grid Width"),
        gr.Slider(8, 100, value=32, step=1, label="Grid Height"),
        gr.Slider(4, 64, value=32, step=1, label="Pixel Size"),
        gr.Slider(2, 32, value=8, step=1, label="Number of Colors")
    ],
    outputs=gr.Image(type="filepath", label="Pixel Art Output"),
    title=" Pixel Art Grid Generator",
    description="Create pixel art images with a custom grid, number of colors, and cell size."
)

demo.launch()
