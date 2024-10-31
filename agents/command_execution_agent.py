# agents/command_execution_agent.py

import subprocess
from agents.agent import Agent

class CommandExecutionAgent(Agent):
    def __init__(self):
        self.allowed_commands = {
            'list_files': ['ls', '-la'],
            'disk_usage': ['df', '-h'],
            'current_directory': ['pwd']
        }

    def handle(self, user_input):
        # Identify the command from the user input
        command_key = self.identify_command(user_input)
        if command_key:
            command = self.allowed_commands[command_key]
            try:
                result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
                return f"Command output:\n{result}"
            except subprocess.CalledProcessError as e:
                return f"An error occurred while executing the command: {e.output}"
        else:
            return "Sorry, I cannot execute that command."

    def identify_command(self, user_input):
        # Simple keyword matching to identify the command
        user_input_lower = user_input.lower()
        if 'list files' in user_input_lower:
            return 'list_files'
        elif 'disk usage' in user_input_lower:
            return 'disk_usage'
        elif 'current directory' in user_input_lower:
            return 'current_directory'
        else:
            return None