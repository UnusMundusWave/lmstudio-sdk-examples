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
holidays_folder = "holidays"
vehicles_folder = "vehicles"
animals_folder = "animals"
other_folder = "other"

# Create folders if they don't exist
for folder in [source_folder, holidays_folder, vehicles_folder, other_folder, animals_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def list_images_to_process() -> str:
    """Lists the name of the next image to process"""
    try:
        images = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        if images:
            first_image = images[0]
            print(f"{Fore.GREEN}First image found in '{source_folder}': {first_image}{Style.RESET_ALL}")
            return first_image
        else:
            print(f"{Fore.YELLOW}No images found in '{source_folder}'.{Style.RESET_ALL}")
            return "There are no more images to process"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Folder '{source_folder}' not found.{Style.RESET_ALL}")
        return ""
    except Exception as e:
        print(f"{Fore.RED}An error occurred while listing images: {e}{Style.RESET_ALL}")
        return ""

def move_image_to_holidays(image_name: str) -> str:
    """Sorts and moves an image to the 'holidays' folder."""
    try:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(holidays_folder, image_name)
        shutil.move(source_path, destination_path)
        print(f"{Fore.GREEN}Image '{image_name}' moved to '{holidays_folder}'.{Style.RESET_ALL}")
        return "retrieve the next image to sort"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while moving the image: {e}{Style.RESET_ALL}")
        return "operation error"
    
def move_image_to_animals(image_name: str) -> str:
    """Sorts and moves an image to the 'animals' folder."""
    try:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(animals_folder, image_name)
        shutil.move(source_path, destination_path)
        print(f"{Fore.GREEN}Image '{image_name}' moved to '{animals_folder}'.{Style.RESET_ALL}")        
        return "retrieve the next image to sort"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while moving the image: {e}{Style.RESET_ALL}")
        return "operation error"

def move_image_to_vehicles(image_name: str) -> str:
    """Sorts and moves an image to the 'vehicles' folder."""
    try:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(vehicles_folder, image_name)
        shutil.move(source_path, destination_path)
        print(f"{Fore.GREEN}Image '{image_name}' moved to '{vehicles_folder}'.{Style.RESET_ALL}")
        return "retrieve the next image to sort"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while moving the image: {e}{Style.RESET_ALL}")
        return "operation error"

def move_image_to_other(image_name: str) -> str:
    """Sorts and moves an image to the 'other' folder."""
    try:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(other_folder, image_name)
        shutil.move(source_path, destination_path)
        print(f"{Fore.GREEN}Image '{image_name}' moved to '{other_folder}'.{Style.RESET_ALL}")
        return "retrieve the next image to sort"
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while moving the image: {e}{Style.RESET_ALL}")
        return "operation error"

def get_image_description(image_name: str) -> str:
    """
    Provides a description of the specified image
    """
    try:
        source_path = os.path.join(source_folder, image_name)
        image_handle = lms.prepare_image(source_path)
        chat = lms.Chat()
        chat.add_user_message("describe the image in 3 sentences", images=[image_handle])
        prediction = image_model.respond(chat)

        
        if not isinstance(prediction, str):
            prediction = str(prediction)
        return prediction
        
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{image_name}' not found in '{source_folder}'.{Style.RESET_ALL}")
        return "File not found"
    except Exception as e:
        print(f"{Fore.RED}An error occurred while describing the image: {e}{Style.RESET_ALL}")
        return "retry with another image"
       

def format_message(message):
    try:
        msg_str = str(message)
        
        # Function to decode Unicode escape sequences
        def decode_unicode(text):
            try:
                return bytes(text, 'utf-8').decode('unicode_escape')
            except:
                return text
        
        # Handle assistant messages
        if hasattr(message, 'role') and message.role == 'assistant':
            print(f"{Fore.CYAN}Assistant:{Style.RESET_ALL}")
            
            # Extract and display all text and tool names
            if hasattr(message, 'content') and isinstance(message.content, list):
                for item in message.content:
                    item_str = str(item)
                    
                    # Extract text content from text parts
                    if "ChatMessagePartTextData" in item_str:
                        if '"text":' in item_str:
                            text_start = item_str.find('"text": "') + 9
                            if text_start > 8:
                                # Handle escaped quotes in the text
                                text_content = ""
                                in_quotes = True
                                i = text_start
                                while i < len(item_str) and in_quotes:
                                    if item_str[i:i+2] == '\\"':
                                        text_content += '"'
                                        i += 2
                                    elif item_str[i] == '"' and (i == 0 or item_str[i-1] != '\\'):
                                        in_quotes = False
                                    else:
                                        text_content += item_str[i]
                                        i += 1
                                
                                # Clean up the text and decode Unicode
                                text_content = text_content.replace('\\n', '\n')
                                text_content = decode_unicode(text_content)
                                if text_content.strip():  # Only print non-empty texts
                                    print(f"{text_content}")
                    
                    # Extract tool names from tool call requests
                    elif "ChatMessagePartToolCallRequestData" in item_str:
                        if '"name":' in item_str:
                            name_start = item_str.find('"name": "') + 9
                            name_end = item_str.find('"', name_start)
                            if name_start > 8 and name_end > name_start:
                                tool_name = item_str[name_start:name_end]
                                tool_name = decode_unicode(tool_name)
                                print(f"{Fore.BLUE}Calling tool: {tool_name}{Style.RESET_ALL}")
        
        # Handle tool messages
        elif hasattr(message, 'role') and message.role == 'tool':
            print(f"{Fore.YELLOW}Tool result:{Style.RESET_ALL}")
            
            # Extract and display all content values
            if hasattr(message, 'content') and isinstance(message.content, list):
                for item in message.content:
                    item_str = str(item)
                    
                    if "ChatMessagePartToolCallResultData" in item_str:
                        if '"content":' in item_str:
                            content_start = item_str.find('"content": "') + 12
                            if content_start > 11:
                                # Extract content with proper handling of quotes
                                content_value = ""
                                in_quotes = True
                                i = content_start
                                while i < len(item_str) and in_quotes:
                                    if item_str[i:i+2] == '\\"':
                                        content_value += '"'
                                        i += 2
                                    elif item_str[i] == '"' and (i == 0 or item_str[i-1] != '\\'):
                                        in_quotes = False
                                    else:
                                        content_value += item_str[i]
                                        i += 1
                                
                                # Clean up the content and decode Unicode
                                content_value = content_value.replace('\\n', '\n')
                                content_value = decode_unicode(content_value)
                                content_value = content_value.strip('\"')
                                print(f"{content_value}")
        
        # Handle string messages
        elif isinstance(message, str):
            print(decode_unicode(message))
            
    except Exception as e:
        print(f"{Fore.RED}Error in format_message: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    return None


# Definition of the agent

model = lms.llm("gemma-3-4b-it")
client = lms.get_default_client()
image_model = client.llm.load_new_instance("gemma-3-4b-it")

prompt = """organize images into folders based on their categories (holidays, vehicles, animals, other)
do not invent names for images, use the existing ones provided by the tool list_images_to_process
before calling a tool, explain your thinking.
at the end of the process, give an evaluation about each tools used."""
tools = [
    list_images_to_process,
    move_image_to_holidays,
    move_image_to_vehicles,
    move_image_to_other,
    move_image_to_animals,
    get_image_description
]
try:    
    result = model.act(
        prompt,
        tools,
        on_message=format_message
    )
    print(f"\n{Fore.GREEN}Final result: {result}{Style.RESET_ALL}")
    model.unload()
    image_model.unload()
    
except Exception as e:
    print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Try using a different model or updating the LMStudio SDK.{Style.RESET_ALL}")

print(f"\n{Fore.MAGENTA}=== CALCULATION COMPLETE ==={Style.RESET_ALL}")
