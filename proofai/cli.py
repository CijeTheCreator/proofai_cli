#!/usr/bin/env python
# proofai/cli.py

import os
import sys
import json
import zipfile
import argparse
import requests
import getpass
import datetime
from pathlib import Path

def validate_metadata():
    """Check if metadata.json exists and is valid."""
    metadata_path = Path("metadata.json")
    
    if not metadata_path.exists():
        print("Error: metadata.json not found in current directory")
        return None
    
    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            
        if "type" not in metadata:
            print("Error: metadata.json does not contain a 'type' field")
            return None
            
        resource_type = metadata["type"].upper()
        if resource_type not in ["AGENT", "DATASET", "MODEL"]:
            print(f"Error: Invalid resource type '{resource_type}'. Must be AGENT, DATASET, or MODEL")
            return None
            
        return metadata
        
    except json.JSONDecodeError:
        print("Error: metadata.json contains invalid JSON")
        return None

def create_zip_archive(output_path="resource.zip"):
    """Create a zip archive of the current directory."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("."):
            # Skip the zip file itself and any hidden directories
            if output_path in root or "/.git" in root or "/__pycache__" in root or "/venv" in root:
                continue
                
            for file in files:
                # Skip the zip file itself and any hidden files
                if file == output_path or file.startswith("."):
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ".")
                zipf.write(file_path, arcname)
    
    return output_path

def upload_resource(resource_type, zip_path):
    """Upload the zipped resource to the appropriate endpoint."""
    base_url = os.environ.get("PROOFAI_API_URL", "http://localhost:3000")
    
    endpoint_map = {
        "AGENT": f"{base_url}/api/agents",
        "MODEL": f"{base_url}/api/models",
        "DATASET": f"{base_url}/api/datasets"
    }
    
    endpoint = endpoint_map.get(resource_type)
    if not endpoint:
        print(f"Error: Unknown resource type '{resource_type}'")
        return False
    
    try:
        # Create multipart form data with the zip file
        with open(zip_path, "rb") as f:
            files = {"file": (os.path.basename(zip_path), f, "application/zip")}
            
            print(f"Uploading {resource_type} to {endpoint}...")
            response = requests.post(endpoint, files=files)
            
        if response.status_code >= 200 and response.status_code < 300:
            result = response.json()
            print(f"Success! {resource_type} upload completed.")
            print(f"Resource ID: {result.get('agentId') or result.get('modelId') or result.get('datasetId')}")
            print(f"Job ID: {result.get('jobId')}")
            return True
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(response.text)
            return False
            
    except requests.RequestException as e:
        print(f"Error during upload: {str(e)}")
        return False
    finally:
        # Clean up the zip file
        if os.path.exists(zip_path):
            os.remove(zip_path)

def create_resource_project(resource_type, name):
    """Create a project structure for a resource."""
    # Sanitize the name for folder creation
    folder_name = name.replace(" ", "_").lower()
    resource_dir = Path(folder_name)
    
    # Check if directory already exists
    if resource_dir.exists():
        print(f"Error: Directory '{folder_name}' already exists")
        return False
        
    # Create the directory
    resource_dir.mkdir(parents=True)
    
    # Get author information (username)
    author = getpass.getuser()
    
    # Create metadata.json
    metadata = {
        "name": name,
        "author": author,
        "description": f"A ProofAI {resource_type.lower()}",
        "tags": [],
        "type": resource_type.upper(),
        "created_at": datetime.datetime.now().isoformat()
    }
    
    metadata_path = resource_dir / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    # If it's an agent, create main.py
    if resource_type.upper() == "AGENT":
        main_py_path = resource_dir / "main.py"
        with open(main_py_path, "w") as f:
            f.write("import proofai\n\n# Type your agent code here\n\n")
    
    print(f"\nCreated {resource_type.lower()} project in '{folder_name}/' directory")
    print(f"- metadata.json: Basic {resource_type.lower()} information")
    
    if resource_type.upper() == "AGENT":
        print("- main.py: Agent implementation file")
    
    print(f"\nNext steps:")
    print(f"1. cd {folder_name}")
    print(f"2. Edit the files to implement your {resource_type.lower()}")
    print("3. Run 'proofai upload' to upload your project")
    
    return True

def upload_command():
    """Handle the upload command."""
    metadata = validate_metadata()
    if not metadata:
        return 1
        
    resource_type = metadata["type"].upper()
    print(f"Detected resource type: {resource_type}")
    
    zip_path = create_zip_archive()
    print(f"Created archive: {zip_path}")
    
    success = upload_resource(resource_type, zip_path)
    return 0 if success else 1

def create_agent_command(name):
    """Create a new agent project."""
    return 0 if create_resource_project("AGENT", name) else 1

def create_model_command(name):
    """Create a new model project."""
    return 0 if create_resource_project("MODEL", name) else 1

def create_dataset_command(name):
    """Create a new dataset project."""
    return 0 if create_resource_project("DATASET", name) else 1

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="ProofAI CLI tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload a resource to ProofAI")
    
    # Create agent command
    create_agent_parser = subparsers.add_parser("create-agent", help="Create a new agent project structure")
    create_agent_parser.add_argument("name", help="Name of the agent")
    
    # Create model command
    create_model_parser = subparsers.add_parser("create-model", help="Create a new model project structure")
    create_model_parser.add_argument("name", help="Name of the model")
    
    # Create dataset command
    create_dataset_parser = subparsers.add_parser("create-dataset", help="Create a new dataset project structure")
    create_dataset_parser.add_argument("name", help="Name of the dataset")
    
    args = parser.parse_args()
    
    if args.command == "upload":
        return upload_command()
    elif args.command == "create-agent":
        return create_agent_command(args.name)
    elif args.command == "create-model":
        return create_model_command(args.name)
    elif args.command == "create-dataset":
        return create_dataset_command(args.name)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
