# LM Studio SDK Examples

This repository contains four Python examples demonstrating the use of the LM Studio SDK. Each script showcases different capabilities of the SDK, including:

-   **`act.py`**: Using tools to solve a number game.
-   **`ChatWeb.py`**: Creating a web-aware chatbot that can analyze and discuss webpage content.
-   **`3Agents.py`**: Simulating a debate between three agents with different viewpoints, moderated by a supervisor.
-   **`sorting_agent.py`**: Sorting images into different folders based on their content.

## Prerequisites

Before running these examples, ensure you have the following:

*   **LM Studio:** Installed and running. 
*   **Python 3.6+:** Python version 3.6 or higher.
*   **LM Studio SDK:** Install the SDK with `pip install lmstudio`. 1.1.0 with image support 
*   **Colorama:** Install with `pip install colorama`.
*   **Requests:** Install with `pip install requests`.
*   **BeautifulSoup4:** Install with `pip install beautifulsoup4`.
*   **PIL:** Install with `pip install pillow`.
*   **Vision-capable Models:** For the sorting_agent.py example, ensure you have a vision-capable model like "gemma-3-4b-it" loaded in LM Studio.
*   **Image Files:** For the sorting_agent.py example, prepare a 'source' folder with various image files (.png, .jpg, .jpeg, etc.) for processing.

## Example Scripts

### 1. `act.py`

This script demonstrates how to use the `act` function of the LM Studio SDK to solve a number game. It defines several mathematical functions (addition, subtraction, multiplication, division) and uses the LM Studio model to find a combination of these functions that results in a target number.

**How to Run:**

```bash
python act.py
```

**Key Features:**

*   Uses the `lms.llm().act()` function to perform actions based on a prompt and available tools:

```python
model = lms.llm()
result = model.act(
    prompt,
    [addition, substraction, multiplication, division],
    on_message=format_message
)
```

*   Defines custom functions (tools) that the model can use:

```python
def addition(a: int, b: int) -> int:
    """Given two integer values a and b as input parameters, this function computes and returns their arithmetic sum (a + b) as an integer value."""
    return a + b
```

*   Formats messages for better readability using `colorama`.

### 2. `ChatWeb.py`

This script creates a web-aware chatbot that can fetch content from a URL, create embeddings, and answer questions about the webpage's content.

**How to Run:**

```bash
python ChatWeb.py
```

**Key Features:**

*   Fetches and parses webpage content using `requests` and `BeautifulSoup4`.
*   Initializes embedding models for semantic search:

```python
embedding_model = lms.embedding_model("nomic-embed-text-v1.5")
query_embedding = embedding_model.embed(query)
```

*   Creates chat sessions with context about webpages:

```python
system_prompt = f"""You are an intelligent web assistant that has analyzed the web page titled "{title}" at URL {url}."""
web_chat = lms.Chat(system_prompt)
response = chat_model.respond(web_chat)
```

**Note:** This script requires an embedding model. If one is not found, it will attempt to initialize `nomic-embed-text-v1.5`. You can install it using:

```bash
lms get nomic-ai/nomic-embed-text-v1.5
```

### 3. `3Agents.py`

This script simulates a debate between three agents: a pro-nuclear advocate, an anti-nuclear advocate, and a neutral supervisor. Each agent has a different viewpoint and responds to the others' arguments.

**How to Run:**

```bash
python 3Agents.py
```

**Key Features:**

*   Creates multiple model instances for different agents:

```python
pro_nuclear_model = lms.llm()
anti_nuclear_model = lms.llm()
supervisor_model = lms.llm()
```

*   Configures different chat personas with system prompts:

```python
pro_nuclear_chat = lms.Chat("Tu es un fervent défenseur de l'énergie nucléaire...")
anti_nuclear_chat = lms.Chat("Tu es un opposant convaincu à l'énergie nucléaire...")
```

*   Manages conversation flow between multiple agents:

```python
anti_nuclear_response = anti_nuclear_model.respond(anti_nuclear_chat)
anti_nuclear_chat.add_assistant_response(anti_nuclear_response)
```

### 4. `sorting_agent.py`

This script demonstrates how to create an agent that sorts images into different folders based on their content using the LM Studio SDK and vision capabilities. It processes images from a source folder and automatically categorizes them into different destination folders.

**How to Run:**

Before running this script, make sure you have a 'source' folder populated with images (e.g., `.png`, `.jpg`, `.jpeg`).

```bash
python sorting_agent.py
```

**Key Features:**

*   Uses the LM Studio SDK's image handling API to process visual content:

```python
def get_image_description(image_name: str) -> str:
    source_path = os.path.join(source_folder, image_name)
    image_handle = lms.prepare_image(source_path)
    chat = lms.Chat()
    chat.add_user_message("describe the image in 3 sentences", images=[image_handle])
    prediction = image_model.respond(chat)
    return prediction
```

*   Demonstrates how to properly prepare images for multimodal LLM processing using `lms.prepare_image()`, a key API function for passing images as input to models
  
*   Uses multimodal capabilities to analyze image content:

```python
model = lms.llm("gemma-3-4b-it")
client = lms.get_default_client()
image_model = client.llm.load_new_instance("gemma-3-4b-it")
```

*   Orchestrates a workflow with `act()` function to automate image classification and sorting:

```python
prompt = """organize images into folders based on their categories (holidays, vehicles, animals, other)
do not invent names for images, use the existing ones provided by the tool list_images_to_process
before calling a tool, explain your thinking.
at the end of the process, give an evaluation about each tools used."""

result = model.act(
    prompt,
    tools,
    on_message=format_message
)
```

*   Includes self-assessment capabilities where the agent evaluates the effectiveness of each tool it used during the sorting process

**Note:** This script requires a vision-capable LLM model, such as "gemma-3-4b-it" or equivalent. Make sure you have a suitable model loaded in LM Studio before running this example.
