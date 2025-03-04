# LM Studio SDK Examples

This repository contains three Python examples demonstrating the use of the LM Studio SDK. Each script showcases different capabilities of the SDK, including:

-   **`act.py`**:  Using tools to solve a number game.
-   **`ChatWeb.py`**:  Creating a web-aware chatbot that can analyze and discuss webpage content.
-   **`3Agents.py`**:  Simulating a debate between three agents with different viewpoints, moderated by a supervisor.

## Prerequisites

Before running these examples, ensure you have the following:

*   **LM Studio:**  Installed and running.
*   **Python 3.6+:**  Python version 3.6 or higher.
*   **LM Studio SDK:** Install the SDK with `pip install lmstudio`.
*   **Colorama:** Install with `pip install colorama`.
*   **Requests:** Install with `pip install requests`.
*   **BeautifulSoup4:** Install with `pip install beautifulsoup4`.
*   **Numpy:** Install with `pip install numpy`.

## Example Scripts

### 1. `act.py`

This script demonstrates how to use the `act` function of the LM Studio SDK to solve a number game. It defines several mathematical functions (addition, subtraction, multiplication, division) and uses the LM Studio model to find a combination of these functions that results in a target number.

**How to Run:**

```bash
python act.py
```

**Key Features:**

*   Uses the `lms.llm().act()` function to perform actions based on a prompt and available tools.
*   Defines custom functions (tools) that the model can use.
*   Formats messages for better readability using `colorama`.

### 2. `ChatWeb.py`

This script creates a web-aware chatbot that can fetch content from a URL, create embeddings, and answer questions about the webpage's content.

**How to Run:**

```bash
python ChatWeb.py
```

**Key Features:**

*   Fetches and parses webpage content using `requests` and `BeautifulSoup4`.
*   Splits text into chunks and creates embeddings using an embedding model (if available).
*   Finds relevant chunks based on user queries using embedding similarity.
*   Uses `lms.Chat` to manage the chat session and `lms.llm().respond()` to get responses from the LM Studio model.

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

*   Creates three `lms.Chat` instances, each with a different system prompt defining the agent's role.
*   Simulates a debate by having the agents respond to each other's messages.
*   Uses a supervisor agent to evaluate the debate and provide guidance.

## Troubleshooting

*   **Model Initialization Errors:** Ensure that LM Studio is running and that the specified model is loaded.
*   **Embedding Model Errors:** If you encounter errors related to the embedding model, make sure you have installed one.
*   **Performance Issues:**  Larger models may require more resources.  Adjust model settings in LM Studio if needed.
