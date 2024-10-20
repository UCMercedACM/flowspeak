
API_KEY='AIzaSyDBecZvfdYJQP2oLX4kcRjPrbZK2_znXZk'


import google.generativeai as genai
import os

genai.configure(api_key=API_KEY)

import PIL.Image

from pathlib import Path

import os
from PIL import Image
import IPython.display as display
import ipywidgets as widgets
from pathlib import Path

# Initialize the model (already defined)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Answer the prompt"},
    ]
)

# Directory containing your PNG files
image_dir = Path("/content")

# Create a list of all .png images in the directory
image_files = list(image_dir.glob("*.png"))

# List to store the names (stems) of the selected images
selected_images = []

# Function to handle image selection when a button is clicked
def on_button_click(b):
    if b.description == "done":
        # Generate content using the selected images and pass it to the model
        generate_response()
    else:
        # Add the selected image's stem (filename without extension) to the list
        image_path = image_dir / b.description
        selected_images.append(image_path.stem)
        print(f"Selected images: {selected_images}")

# Function to generate content when "done" is pressed
def generate_response():
    # Concatenate the selected image names into a single string
    user_input = ", ".join(selected_images)
    print(user_input)
    
    # Send the message to the model with the selected images in a sentence
    response = chat.send_message(f"Assume the user is a non verbal person. Generate a sentence explaining what I am trying to say using the text. No more information is provided. Give me 3-5 options. Give the answer in first person. DO NOT UNDER ANY CIRCUMSTANCES MENTION THE USER IS NON VERBAL: {user_input}")
    
    # Print the model's response (alternatively, display it in Colab)
    print(response.text)

# Create buttons for each image file
buttons = []
for img_path in image_files:
    # Create a button with the image file's name as the label
    button = widgets.Button(description=img_path.name)
    button.on_click(on_button_click)
    buttons.append(button)

# Add a "done" button to trigger the content generation
done_button = widgets.Button(description="done")
done_button.on_click(on_button_click)
buttons.append(done_button)

# Display the buttons in the Colab interface
widgets.VBox(buttons)