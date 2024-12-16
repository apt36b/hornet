#!/bin/bash

# Script to create a standalone binary using PyInstaller

# Set the entry point and project files
ENTRY_POINT="main.py"
INCLUDED_FILES=("main.py" "informations.py" "exceptions.py" "encrypt.py")
OUTPUT_NAME="hornet_tool"

# Ensure the required dependencies are installed
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || { echo "Dependency installation failed!"; exit 1; }
else
    echo "requirements.txt not found. Ensure dependencies are installed!"
    exit 1
fi

# Check if PyInstaller is installed
echo "Checking for PyInstaller..."
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing PyInstaller..."
    pip install pyinstaller || { echo "Failed to install PyInstaller!"; exit 1; }
fi

# Create the PyInstaller command
echo "Building the standalone binary..."
pyinstaller --onefile --name "$OUTPUT_NAME" "$ENTRY_POINT"

# Check if build succeeded
if [ $? -eq 0 ]; then
    echo "Build successful! Binary created: dist/$OUTPUT_NAME"
else
    echo "Build failed! Check the logs above for details."
    exit 1
fi

# Clean up build files if desired
echo "Cleaning up temporary build files..."
rm -rf build "$OUTPUT_NAME.spec"

# List the contents of the output directory
echo "Binary is ready in the dist/ directory:"
ls -lh dist/

echo "Standalone binary build completed successfully!"
