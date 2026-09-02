from fastmcp import FastMCP
import subprocess

mcp = FastMCP("Dokcer MCP server")

@mcp.tool  # tool is decorator which basically make function as tool
def show_running_container():

    """""Tool1-Show all currently running Docker containers."""""
    result = subprocess.run(["docker","ps"], capture_output= True, text= True)
    return result.stdout

@mcp.tool
def show_container_log(container_name):

      """ Tool2-Show Docker logs for a specified container."""
     
      result = subprocess.run(["docker","logs", container_name],capture_output= True, text= True)
      return result.stdout

@mcp.tool
def show_all_containers():
    """Tool3-Show all containers including stopped ones."""
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True)
    return result.stdout
@mcp.tool
def show_container_stats():
    """Show live CPU, memory, network usage of all running containers."""
    result = subprocess.run(["docker", "stats", "--no-stream"], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def inspect_container(container_name: str):
    """Show detailed low-level information about a container."""
    result = subprocess.run(["docker", "inspect", container_name], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def show_disk_usage():
    """Show Docker disk usage for images, containers and volumes."""
    result = subprocess.run(["docker", "system", "df"], capture_output=True, text=True)
    return result.stdout
#-------------------------------------------
# TOOLS — ACT (fix and manage containers)
#-------------------------------------------

@mcp.tool
def start_container(container_name: str):
    """Start a stopped Docker container."""
    result = subprocess.run(["docker", "start", container_name], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def stop_container(container_name: str):
    """Stop a running Docker container."""
    result = subprocess.run(["docker", "stop", container_name], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def restart_container(container_name: str):
    """Restart a Docker container."""
    result = subprocess.run(["docker", "restart", container_name], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def remove_container(container_name: str):
    """Remove a stopped Docker container."""
    result = subprocess.run(["docker", "rm", container_name], capture_output=True, text=True)
    return result.stdout

# ------------------------------
# TOOLS — IMAGES
# ------------------------------

@mcp.tool
def show_all_images():
    """List all Docker images on the system."""
    result = subprocess.run(["docker", "images"], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def pull_image(image_name: str):
    """Pull a Docker image from Docker Hub."""
    result = subprocess.run(["docker", "pull", image_name], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def remove_image(image_name: str):
    """Remove a Docker image from the system."""
    result = subprocess.run(["docker", "rmi", image_name], capture_output=True, text=True)
    return result.stdout

#------------------------------------
# TOOLS — CLEANUP
#-------------------------------------

@mcp.tool
def prune_stopped_containers():
    """Remove all stopped Docker containers."""
    result = subprocess.run(["docker", "container", "prune", "-f"], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def prune_unused_images():
    """Remove all unused and dangling Docker images."""
    result = subprocess.run(["docker", "image", "prune", "-f"], capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
     mcp.run()