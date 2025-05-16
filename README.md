# ProofAI

The official Python SDK for Agent Hub. This package provides a runtime context stub for agent developers to interact with platform APIs such as environment variables, user context, message reporting, and agent invocation.

## Installation

```bash
pip install proofai
```

## SDK Usage

```python
# Import the ProofAI SDK
import proofai

# Access environment variables
env_vars = proofai.get_env_vars()

# Access user variables
user_vars = proofai.get_user_vars()

# Get chat history
history = proofai.get_chat_history()

# Send a message
proofai.send_message("Hello from my agent!")

# Call another agent
proofai.call_agent("other-agent-id", {"prompt": "Process this data"})
```

## Command-line Usage

The ProofAI package includes a command-line interface for common tasks.

### Creating Projects

You can create project templates for agents, models, and datasets:

```bash
# Create an agent project
proofai create-agent "My New Agent"

# Create a model project
proofai create-model "My New Model"

# Create a dataset project
proofai create-dataset "My New Dataset"
```

This will create a directory with the appropriate structure:

- For agents: Contains `metadata.json` and `main.py`
- For models/datasets: Contains `metadata.json`

### Uploading Resources

To upload an agent, model, or dataset to the ProofAI platform:

1. Navigate to your project directory (created with the commands above or manually)
2. Make sure you have a `metadata.json` file with at least a `type` field:

```json
{
  "type": "AGENT",
  "name": "My Agent",
  "description": "This is my agent",
  "tags": ["example", "demo"],
  "author": "Your Name"
}
```

3. Run the upload command:

```bash
proofai upload
```

This will:

- Validate your metadata.json file
- Zip the contents of your current directory
- Upload to the appropriate endpoint based on the resource type
- Return the resource ID and job ID for tracking

### Environment Configuration

You can set the API endpoint using the `PROOFAI_API_URL` environment variable:

```bash
export PROOFAI_API_URL="https://your-proofai-server.com"
```

If not set, it defaults to "http://localhost:3000".
