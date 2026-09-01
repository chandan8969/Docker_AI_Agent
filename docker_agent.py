from langchain_ollama import ChatOllama
import subprocess # Python module that allows Python to execute commands/programs from the operating system.
from langchain_core.tools import tool #This is the LangChain module containing functionality related to tools. Here tool is
                                      # tool is decorator
from langchain.agents import create_agent

SYSTEM_PROMPT = """

You are DockerGPT — a senior Docker and container infrastructure expert with 10+ years of hands-on experience.

You help developers and DevOps engineers debug Docker issues, understand concepts, and fix problems FAST.

## YOUR BEHAVIOR RULES
- Answer in 2 to 5 lines maximum — no essays, no padding
- Never hallucinate — if you don't know, say "I'm not sure, check the official Docker docs"
- Never loop your reasoning — think once, respond directly
- Always be specific — give exact commands, not vague suggestions
- Use code blocks for all commands and config snippets

## WHAT YOU CAN DO
1. ERROR DIAGNOSIS   → Identify what the error means in plain English
2. ROOT CAUSE       → Explain exactly why it happened
3. FIX              → Give the exact command or config change to resolve it
4. BEST PRACTICE    → If relevant, mention the right way to avoid it next time

## RESPONSE FORMAT
Always respond in this structure:

🔴 Error    : [what the error is]
🟡 Cause    : [why it happened]
🟢 Fix      : [exact command or config to resolve it]
💡 Tip      : [one-line best practice to avoid it — optional]

## YOUR EXPERTISE COVERS
- Docker CLI commands and flags
- Dockerfile writing and optimization
- Docker Compose (v2 and v3)
- Docker networking (bridge, host, overlay)
- Docker volumes and bind mounts
- Docker image layers and caching
- Container resource limits (CPU, memory)
- Docker registry (push, pull, login)
- Multi-stage builds
- Docker security best practices
- Container health checks
- Docker logs and debugging
- Common errors: permission denied, port conflicts, OOM kills, image not found, network issues

"""

@tool  # tool is decorator which basically make function as tool
def show_running_container():

    """""Tool1-Show all currently running Docker containers."""""

          
 # by using the run() function/mention you can all the different command of your system
    result = subprocess.run(["docker","ps"], capture_output= True, text= True)

    # Capture the output produced by the command instead of simply displaying it on the terminal.
    # Without it, the Docker output would normally go directly to the terminal.
    # Return the command output as normal text (str).Without text=True, the output may be returned as bytes.

    return result.stdout

@tool
def show_container_log(container_name):

      """ Tool2-Show Docker logs for a specified container."""
     
      result = subprocess.run(["docker","logs", container_name],capture_output= True, text= True)
      return result.stdout

@tool
def show_all_containers():
    """Tool3-Show all containers including stopped ones."""
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True)
    return result.stdout
@tool
def show_container_stats():
    """Show live CPU, memory, network usage of all running containers."""
    result = subprocess.run(["docker", "stats", "--no-stream"], capture_output=True, text=True)
    return result.stdout

@tool
def inspect_container(container_name: str):
    """Show detailed low-level information about a container."""
    result = subprocess.run(["docker", "inspect", container_name], capture_output=True, text=True)
    return result.stdout

@tool
def show_disk_usage():
    """Show Docker disk usage for images, containers and volumes."""
    result = subprocess.run(["docker", "system", "df"], capture_output=True, text=True)
    return result.stdout
#-------------------------------------------
# TOOLS — ACT (fix and manage containers)
#-------------------------------------------

@tool
def start_container(container_name: str):
    """Start a stopped Docker container."""
    result = subprocess.run(["docker", "start", container_name], capture_output=True, text=True)
    return result.stdout

@tool
def stop_container(container_name: str):
    """Stop a running Docker container."""
    result = subprocess.run(["docker", "stop", container_name], capture_output=True, text=True)
    return result.stdout

@tool
def restart_container(container_name: str):
    """Restart a Docker container."""
    result = subprocess.run(["docker", "restart", container_name], capture_output=True, text=True)
    return result.stdout

@tool
def remove_container(container_name: str):
    """Remove a stopped Docker container."""
    result = subprocess.run(["docker", "rm", container_name], capture_output=True, text=True)
    return result.stdout

# ------------------------------
# TOOLS — IMAGES
# ------------------------------

@tool
def show_all_images():
    """List all Docker images on the system."""
    result = subprocess.run(["docker", "images"], capture_output=True, text=True)
    return result.stdout

@tool
def pull_image(image_name: str):
    """Pull a Docker image from Docker Hub."""
    result = subprocess.run(["docker", "pull", image_name], capture_output=True, text=True)
    return result.stdout

@tool
def remove_image(image_name: str):
    """Remove a Docker image from the system."""
    result = subprocess.run(["docker", "rmi", image_name], capture_output=True, text=True)
    return result.stdout

#------------------------------------
# TOOLS — CLEANUP
#-------------------------------------

@tool
def prune_stopped_containers():
    """Remove all stopped Docker containers."""
    result = subprocess.run(["docker", "container", "prune", "-f"], capture_output=True, text=True)
    return result.stdout

@tool
def prune_unused_images():
    """Remove all unused and dangling Docker images."""
    result = subprocess.run(["docker", "image", "prune", "-f"], capture_output=True, text=True)
    return result.stdout

model = ChatOllama(model = "gemma4",  temperature = 0.8) # temperature basically used to control the randomless response of agent
                                                    # its value should between 0.1 to 1.
tools = [show_running_container,
         show_container_log,
         show_all_containers,
         show_container_stats,
         inspect_container,
         show_disk_usage,
         start_container,
         stop_container,
         restart_container,
         remove_container,
         show_all_images,
         pull_image,
         remove_image,
         prune_stopped_containers,
         prune_unused_images]

agents = create_agent(model,tools)
while True:
    user_input = input("enter the docker questions \n")
    if user_input.lower() == "exit":
            print("Exiting...")
            break
    response = agents.invoke({"messages":[{"role":"system","content":SYSTEM_PROMPT,"role":"user","content": user_input}]})

    print("Answer:\n")
    print(response["messages"][-1].content)