import torch
from diffusers import StableDiffusionPipeline
from IPython.display import display, Image, clear_output
import time
import ipywidgets as widgets
from tqdm.notebook import tqdm

# Load the Stable Diffusion model
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

def generate_image(prompt):
    with tqdm(total=100, desc="Generating image", bar_format='{l_bar}{bar}') as pbar:
        for _ in range(10):
            time.sleep(0.1)  # Simulate steps in generation process
            pbar.update(10)
        image = pipe(prompt).images[0]
    # Save the image
    image_path = f"generated_image_{int(time.time())}.png"
    image.save(image_path)
    # Display the image
    clear_output()
    display(Image(filename=image_path))

# User interaction with widgets
text_input = widgets.Text(description="Image description:")
generate_button = widgets.Button(description="Generate")

def on_button_click(b):
    generate_image(text_input.value)

generate_button.on_click(on_button_click)
display(text_input, generate_button)
