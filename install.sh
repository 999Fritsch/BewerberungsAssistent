#!/bin/bash

# Define the Streamlit configuration directory and file
STREAMLIT_CONFIG_DIR="$HOME/.streamlit"
CONFIG_FILE="$STREAMLIT_CONFIG_DIR/config.toml"

# Create the Streamlit configuration directory if it doesn't exist
mkdir -p "$STREAMLIT_CONFIG_DIR"

# Add the configuration to disable usage statistics
echo -e "\n[browser]\ngatherUsageStats = false" >> "$CONFIG_FILE"