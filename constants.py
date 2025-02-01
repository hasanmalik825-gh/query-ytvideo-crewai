import os

IP_WHITELIST = os.environ.get("IP_WHITELIST") or ["127.0.0.1"]
PORT = os.getenv("PORT") or 8000
# set env OPENAI_MODEL_NAME with any openai model and OPENAI_API_KEY with openai api.
