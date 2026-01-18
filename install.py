import sys
import subprocess
import platform
import os

def install_dependencies():
    """Installs dependencies from requirements.txt."""
    requirements_file = 'requirements.txt'
    
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.")
        sys.exit(1)

    print(f"Installing dependencies from {requirements_file}...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def check_os_specific_requirements():
    """Checks for OS-specific tools (like textutil for macOS)."""
    current_os = platform.system()
    print(f"\nDetected OS: {current_os}")

    if current_os == 'Darwin':  # macOS
        print("macOS detected.")
        print("Checking for 'textutil' (required for .doc support)...")
        try:
            subprocess.run(['textutil'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("'textutil' is available. Support for .doc files is enabled.")
        except FileNotFoundError:
            print("Warning: 'textutil' command not found. Reading .doc files might not work.")
            print("textutil is usually included with macOS. Please ensure it is in your PATH.")
    elif current_os == 'Windows':
        print("Windows detected.")
        print("Note: The current script uses 'textutil' for .doc files, which is macOS-specific.")
        print("You will be able to read .docx and .txt files, but .doc files may not be supported generically without additional tools.")
    else:
        print(f"{current_os} detected.")
        print("Note: .doc file support currently relies on macOS 'textutil'.")

def main():
    print("=== Affinity Score Installation ===")
    install_dependencies()
    check_os_specific_requirements()
    print("\nSetup complete! You can now run the calculator using:")
    print(f"python affinity_calculator.py")

if __name__ == "__main__":
    main()
