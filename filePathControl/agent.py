import os
from pathlib import Path
from typing import Optional
from google.adk.agents import Agent

def save_test_file(file_content: Optional[str] = None) -> dict:
    """Saves a test.txt file in the filePathControl directory.
    
    Args:
        file_content (Optional[str], optional): Content to write to the file. 
                                      Defaults to a sample message.
    
    Returns:
        dict: Status and result or error message.
    """
    try:
        # Get the current directory where this file is located
        current_dir = Path(__file__).parent.absolute()
        
        # Define the path for test.txt
        test_file_path = current_dir / "test.txt"
        
        # Use default content if none provided
        if not file_content:
            file_content = "This is a test file.\nCreated by filePathControl agent.py\n"
        
        # Write content to the file
        with open(test_file_path, 'w') as f:
            f.write(file_content)
        
        return {
            "status": "success",
            "message": f"Successfully saved test.txt at: {test_file_path}",
            "file_path": str(test_file_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error saving test.txt: {e}"
        }

def get_test_file_path() -> dict:
    """Returns the path to the test.txt file
    
    Returns:
        dict: Status and the file path or error message.
    """
    try:
        file_path = Path(__file__).parent.absolute() / "test.txt"
        return {
            "status": "success", 
            "file_path": str(file_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error getting file path: {e}"
        }

# Define the agent
root_agent = Agent(
    name="file_path_control_agent",
    model="gemini-2.0-flash",
    description="Agent to handle file path operations and save test files.",
    instruction="You are a helpful agent who can save test files and manage file paths.",
    tools=[save_test_file, get_test_file_path],
)

if __name__ == "__main__":
    # Test the agent functionality when run directly
    result = save_test_file()
    print(result)
