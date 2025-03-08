import lmstudio as lms
import os
import shutil
import subprocess
import json
import colorama
from colorama import Fore, Style
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import warnings
import io
from contextlib import redirect_stdout

# Initialize colorama
colorama.init()

# Folder configuration
source_folder = "source"
vacances_folder = "vacances"
voitures_folder = "voitures"
autres_folder = "autres"

# Create folders if they don't exist
for folder in [source_folder, vacances_folder, voitures_folder, autres_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def list_images_to_process() -> list:
    """Lists the names of images in the 'source' folder."""
    try:
        images = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        print(f"{Fore.GREEN}Images found in '{source_folder}': {images}{Style.RESET_ALL}")
        return images
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Folder '{source_folder}' not found.{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}An error occurred while listing images: {e}{Style.RESET_ALL}")
        return []

def move_image_to_holidays(image_name: str) -> str:
    """Moves an image to the 'vacances' folder."""
    try:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(vacances_folder, image_name)
        shutil.move(source_path, destination_path)
        print(f"{Fore.GREEN}Image '{image_name}' moved to '{vacances_folder}'.{Style.RESET_ALL}")
        return "operation OK"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while moving the image: {e}{Style.RESET_ALL}")
        return "operation error"

def move_image_to_cars(image_name: str) -> str:
    """Moves an image to the 'voitures' folder."""
    try:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(voitures_folder, image_name)
        shutil.move(source_path, destination_path)
        print(f"{Fore.GREEN}Image '{image_name}' moved to '{voitures_folder}'.{Style.RESET_ALL}")
        return "operation OK"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while moving the image: {e}{Style.RESET_ALL}")
        return "operation error"

def move_image_to_others(image_name: str) -> str:
    """Moves an image to the 'autres' folder."""
    try:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(autres_folder, image_name)
        shutil.move(source_path, destination_path)
        print(f"{Fore.GREEN}Image '{image_name}' moved to '{autres_folder}'.{Style.RESET_ALL}")
        return "operation OK"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while moving the image: {e}{Style.RESET_ALL}")
        return "operation error"

def get_image_description(image_name: str) -> str:
    """Provides a description of the image."""
    try:
        # Suppress specific warnings
        warnings.filterwarnings("ignore", category=FutureWarning, message="Importing from timm.models.layers is deprecated, please import via timm.layers")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")

        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Florence-2-large", 
            trust_remote_code=True,
            torch_dtype=dtype
        ).to(device)
        
        processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True)
        print("Model loaded successfully")

        image_path = os.path.join(source_folder, image_name)
        if not os.path.exists(image_path):
            print(f"{Fore.RED}Error: Image '{image_path}' not found.{Style.RESET_ALL}")
            return "Image not found"

        image = Image.open(image_path).convert("RGB")
        task = "<DETAILED_CAPTION>"
        inputs = processor(text=task, images=image, return_tensors="pt").to(device)

        for key in inputs:
            if isinstance(inputs[key], torch.Tensor):
                if key == "input_ids" or "attention_mask" in key or "position_ids" in key:
                    inputs[key] = inputs[key].to(device, dtype=torch.long)
                else:
                    inputs[key] = inputs[key].to(device, dtype=dtype)

        print("Generating caption...")
        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=750,  
                num_beams=3,
                do_sample=True,
                temperature=0.7, 
                top_p=0.9,
            )

        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        if "assistant:" in generated_text.lower():
            detailed_caption = generated_text.split("assistant:", 1)[1].strip()
        else:
            detailed_caption = generated_text.strip()

        print("\n" + "=" * 50)
        print("DETAILED_CAPTION:")
        print("=" * 50)
        print(detailed_caption)
        print("=" * 50)
        return detailed_caption

    except Exception as e:
        print(f"{Fore.RED}An error occurred while processing the image description: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return "operation error"


def format_message(message):
    """Format the message in a more readable way"""
    try:
        # Simple string representation for any message type
        if hasattr(message, 'role'):
            role = message.role
            if role == 'assistant':
                print(f"{Fore.CYAN}Assistant thinking:{Style.RESET_ALL}")
                # Try to get text content
                if hasattr(message, 'content') and len(message.content) > 0:
                    for item in message.content:
                        if hasattr(item, 'text') and item.text:
                            print(f"{item.text}\n")

            elif role == 'tool':
                print(f"{Fore.YELLOW}Tool result:{Style.RESET_ALL}")
                if hasattr(message, 'content') and len(message.content) > 0:
                    print(message.content[0].content)
        else:
            # Print any other message types in a simplified way
            print(f"{Fore.WHITE}Message: {message}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error formatting message: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Raw message: {str(message)[:100]}...{Style.RESET_ALL}")

    # Return None to prevent default printing
    return None


# Definition of the agent
model = lms.llm()

prompt = """You are an agent in charge of classifying images into the 3 following categories: holidays, cars, and others.
    You must process all available images using an image description to sort them.
    You will use tools to help you with this task.
    You have the following tools available:
    - "list_images_to_process": to list the images to be processed. No input required and returns a list of images.
    - "move_image_to_holidays": to move an image to the 'vacances' folder. Requires the image name as input and returns "operation OK".
    - "move_image_to_cars": to move an image to the 'voitures' folder. Requires the image name as input and returns "operation OK".
    - "move_image_to_others": to move an image to the 'autres' folder. Requires the image name as input and returns "operation OK".
    - "get_image_description": to get a description of an image. Requires the image name as input and returns a description.
    You must process all available images using the description to sort them.
    Show your reasoning for each image.
    """

tools = [
    list_images_to_process,
    move_image_to_holidays,
    move_image_to_cars,
    move_image_to_others,
    get_image_description
]
try:
    result = model.act(
        prompt,
        tools,
        on_message=format_message
    )
    print(f"\n{Fore.GREEN}Final result: {result}{Style.RESET_ALL}")
except Exception as e:
    print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Try using a different model or updating the LMStudio SDK.{Style.RESET_ALL}")

print(f"\n{Fore.MAGENTA}=== CALCULATION COMPLETE ==={Style.RESET_ALL}")