import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Azure OpenAI client setup
def get_azure_openai_client():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    
    if not endpoint or not key:
        raise RuntimeError("Azure OpenAI credentials not set.")
    
    client = AzureOpenAI(
        api_key=key,
        azure_endpoint=endpoint,
        api_version=api_version
    )
    return client, deployment
