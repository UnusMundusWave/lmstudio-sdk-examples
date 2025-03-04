import lmstudio as lms
import time
import colorama
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup
import numpy as np

# Initialize colorama
colorama.init()

# Initialize LLM model
chat_model = lms.llm() # Initializes the language model from LM Studio.

# Try to initialize embedding model
try:
    embedding_model = lms.embedding_model("nomic-embed-text-v1.5") # Initializes the embedding model.
    embeddings_available = True
    print(f"{Fore.GREEN}Embedding model initialized successfully{Style.RESET_ALL}")
except Exception as e:
    embeddings_available = False
    print(f"{Fore.YELLOW}Unable to initialize embedding model: {str(e)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}You can install an embedding model with: lms get nomic-ai/nomic-embed-text-v1.5{Style.RESET_ALL}")

def fetch_webpage_content(url):
    """Fetch and parse webpage content using BeautifulSoup"""
    try:
        print(f"{Fore.CYAN}Retrieving page content: {url}{Style.RESET_ALL}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else "Untitled page"
        
        # Extract text from paragraphs, headers and other content elements
        content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'article', 'section'])
        content = ' '.join([elem.get_text().strip() for elem in content_elements])
        
        # Clean up content (remove extra spaces, newlines)
        content = ' '.join(content.split())
        
        print(f"{Fore.GREEN}Content retrieved: {len(content)} characters{Style.RESET_ALL}")
        return title, content
        
    except Exception as e:
        print(f"{Fore.RED}Error retrieving the page: {e}{Style.RESET_ALL}")
        return None, None

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks for embedding"""
    words = text.split()
    chunks = []
    
    if len(words) <= chunk_size:
        return [text]
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

def create_embeddings(chunks):
    """Create embeddings for each text chunk"""
    if not embeddings_available:
        return None
    
    embeddings = []
    try:
        for chunk in chunks:
            embedding = embedding_model.embed(chunk) # Generates the embedding for the chunk.
            embeddings.append(embedding)
        return embeddings
    except Exception as e:
        print(f"{Fore.YELLOW}Error creating embeddings: {str(e)}{Style.RESET_ALL}")
        return None

def find_relevant_chunks(query, chunks, embeddings, top_k=3):
    """Find the most relevant chunks to the query using embedding similarity"""
    if not embeddings_available or not embeddings:
        # If embeddings are not available, use the first chunks
        return chunks[:min(top_k, len(chunks))]
    
    try:
        # Create embedding for the query
        query_embedding = embedding_model.embed(query) # Generates the embedding for the query.
        
        # Calculate similarity with each chunk
        similarities = []
        for emb in embeddings:
            # Convert to numpy arrays
            query_array = np.array(query_embedding).reshape(1, -1)
            chunk_array = np.array(emb).reshape(1, -1)
            
            # Calculate cosine similarity
            dot_product = np.dot(query_array, chunk_array.T)[0][0]
            query_norm = np.linalg.norm(query_array)
            chunk_norm = np.linalg.norm(chunk_array)
            similarity = dot_product / (query_norm * chunk_norm)
            
            similarities.append(similarity)
        
        # Get top k chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [chunks[i] for i in top_indices]
    
    except Exception as e:
        print(f"{Fore.YELLOW}Error finding relevant chunks: {str(e)}{Style.RESET_ALL}")
        return chunks[:min(top_k, len(chunks))]

def chat_with_web_agent():
    """
    Interactive chat with a web-aware agent that can discuss webpage content.
    """
    print(Fore.GREEN + "=== CHAT WITH WEB AGENT ===" + Style.RESET_ALL)
    print(Fore.YELLOW + "To begin, enter a URL to analyze." + Style.RESET_ALL)
    print(Fore.YELLOW + "Type 'exit' to quit or 'new' to load a new URL." + Style.RESET_ALL)
    
    url = None
    title = None
    chunks = None
    embeddings = None
    web_chat = None
    
    while True:
        if not url:
            user_input = input(Fore.CYAN + "URL: " + Style.RESET_ALL)
            
            if user_input.lower() == "exit":
                print(Fore.GREEN + "\nThank you for using the web agent. Goodbye!" + Style.RESET_ALL)
                break
            
            if user_input.lower() == "new":
                continue
            
            # Try to fetch the webpage
            url = user_input
            title, content = fetch_webpage_content(url) # Fetches the content of the webpage.
            
            if not content:
                url = None
                continue
            
            # Create chunks and embeddings
            print(f"{Fore.CYAN}Preparing content for analysis...{Style.RESET_ALL}")
            chunks = chunk_text(content) # Divides the content into smaller chunks.
            print(f"{Fore.CYAN}Content divided into {len(chunks)} segments{Style.RESET_ALL}")
            
            if embeddings_available:
                print(f"{Fore.CYAN}Creating embeddings...{Style.RESET_ALL}")
                embeddings = create_embeddings(chunks) # Creates embeddings for each chunk.
                print(f"{Fore.CYAN}Embeddings created successfully{Style.RESET_ALL}")
            
            # Initialize the chat with context about the webpage
            system_prompt = f"""You are an intelligent web assistant that has analyzed the web page titled "{title}" at URL {url}. 
            You answer user questions about the content of this web page.
            Provide accurate and helpful information based solely on the available content.
            If you cannot find the information in the content, be honest about it."""
            
            web_chat = lms.Chat(system_prompt) # Initializes the chat session with a system prompt.
            
            # Welcome message
            print(f"{Fore.GREEN}Web page loaded: \"{title}\"{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Ask your questions about this page's content. Type 'new' to load a new URL or 'exit' to quit.{Style.RESET_ALL}")
            
        else:
            # Chat with the loaded webpage
            user_query = input(Fore.CYAN + "You: " + Style.RESET_ALL)
            
            if user_query.lower() == "exit":
                print(Fore.GREEN + "\nThank you for using the web agent. Goodbye!" + Style.RESET_ALL)
                break
            
            if user_query.lower() == "new":
                url = None
                title = None
                chunks = None
                embeddings = None
                web_chat = None
                print(Fore.YELLOW + "Enter a new URL to analyze:" + Style.RESET_ALL)
                continue
            
            # Find relevant chunks based on the query
            start_time = time.time()
            
            # Get relevant context based on the query
            relevant_chunks = find_relevant_chunks(user_query, chunks, embeddings) # Finds the most relevant chunks for the user query.
            relevant_context = "\n\n".join(relevant_chunks)
            
            # Create the prompt with the relevant context
            prompt = f"""To answer this question, use the following content extracted from the web page:
            
            {relevant_context}
            
            Question: {user_query}"""
            
            # Get the agent's response
            web_chat.add_user_message(prompt) # Adds the user's message to the chat session.
            response = chat_model.respond(web_chat) # Gets the response from the LM Studio model.
            web_chat.add_assistant_response(response) # Adds the assistant's response to the chat session.
            
            end_time = time.time()
            
            # Print the agent's response
            print(f"{Fore.BLUE}Web Agent: {Style.RESET_ALL}{response}\n")
            
            # Print the response time
            print(Fore.MAGENTA + f"Response time: {end_time - start_time:.2f} seconds" + Style.RESET_ALL + "\n")

if __name__ == "__main__":
    chat_with_web_agent()