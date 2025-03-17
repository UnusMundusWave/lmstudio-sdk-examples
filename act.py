import math
import lmstudio as lms
import colorama
from colorama import Fore, Style
import json
import re

# Initialize colorama
colorama.init()

def addition(a: int, b: int) -> int:
    """Given two integer values a and b as input parameters, this function computes and returns their arithmetic sum (a + b) as an integer value."""
    return a + b

def substraction(a: int, b: int) -> int:
    """Given two integer values a and b as input parameters, this function computes and returns their arithmetic difference (a - b) as an integer value."""
    if a < b:
        raise ValueError("substraction result is negative")
    return a - b

def multiplication(a: int, b: int) -> int:
    """Given two integer values a and b as input parameters, this function computes and returns their arithmetic product (a * b) as an integer value."""
    return a * b

def division(a: int, b: int) -> int:
    """Given two integer values a and b as input parameters, this function computes and returns their arithmetic quotient (a / b) as an integer value. If b equals zero, a ValueError exception is raised to prevent division by zero. If the division does not result in an integer value, a ValueError exception is raised."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    if a % b != 0:
        raise ValueError("Division must result in an integer")
    return a // b

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

print(f"\n{Fore.MAGENTA}=== NUMBERS GAME CHALLENGE ==={Style.RESET_ALL}")
print(f"{Fore.BLUE}Target: 254, Using numbers: 25, 100, 1, 7, 5, 2, 8{Style.RESET_ALL}\n")

# Create model and set up functions
model = lms.llm()

try:
    # Use a more specific prompt that works better with the current model
    prompt = """
    The Numbers Game: I need to get exactly 254 using these numbers: 25, 100, 1, 7, 5, 2, and 8.
    I can use addition, substraction, multiplication, and division.
    Each number can only be used once, but I don't have to use all numbers.
    Think step by step and use tools to verify calculations.
    """
    
    result = model.act(
        prompt,
        [addition, substraction, multiplication, division],
        on_message=format_message
    )
    
    print(f"\n{Fore.GREEN}Final result: {result}{Style.RESET_ALL}")

except Exception as e:
    print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Try using a different model or updating the LMStudio SDK.{Style.RESET_ALL}")

print(f"\n{Fore.MAGENTA}=== CALCULATION COMPLETE ==={Style.RESET_ALL}")
