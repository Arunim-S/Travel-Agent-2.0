import os
from langchain_openai import AzureChatOpenAI

# Langchain Credentials
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "evaluators"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__3ef32ca832884d959bc1f43ee0dc1dbd"

# Credentials
OPENAI_API_KEY = "6e9d4795bb89425286669b5952afe2fe"
OPENAI_DEPLOYMENT_NAME = "GPT4Turbo"
MODEL_NAME = "GPT4Turbo"
END_POINT = "https://danielingitaraj-gpt4turbo.openai.azure.com/"
VERSION = "2024-02-01"

llm = AzureChatOpenAI(
openai_api_key=OPENAI_API_KEY,
deployment_name=OPENAI_DEPLOYMENT_NAME,
model_name=MODEL_NAME,
api_version=VERSION,
azure_endpoint=END_POINT,
temperature=0
)