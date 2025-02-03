#!/bin/bash

# Set the directory where your message history is stored
message_history_directory="$HOME/chatgpt_message_history"

# Check if the directory exists
if [ -d "$message_history_directory" ]; then
  echo "Deleting message history from $message_history_directory..."
  
  # Delete all files in the message history directory
  rm -rf "$message_history_directory"/*
  
  echo "Message history deleted successfully."
else
  echo "Directory not found. Please check the path and try again."
fi
