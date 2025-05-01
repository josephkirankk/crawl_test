import os
import litellm

# Set Azure OpenAI credentials
os.environ["AZURE_API_KEY"] = "957badf7e39643dca147a6b8d157f66d"
os.environ["AZURE_API_BASE"] = "https://pep-ee-pepgenxsbx-nonprod-eus2-openai.openai.azure.com"
os.environ["AZURE_API_VERSION"] = "2025-01-01-preview"

# Enable debug mode to see exactly what's happening
litellm._turn_on_debug()

# Test a simple completion
try:
    response = litellm.completion(
        model="azure/gpt-4.1",
        messages=[{"role": "user", "content": "Hello, how are you?"}]
    )
    print("Success! Response:", response)
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
    print("Please check your Azure OpenAI credentials and deployment name.") 