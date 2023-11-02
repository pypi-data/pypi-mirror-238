import promptlayer
import os
# promptlayer.api_key = os.environ.get("PROMPTLAYER_API_KEY")

# # Swap out your 'import openai'
# openai = promptlayer.openai
# openai.api_key = os.environ.get("OPENAI_API_KEY")

# # Do something fun 🚀
# openai.ChatCompletion.create(
#   engine="gpt-3.5-turbo", 
#   prompt="Say \"hello world\".", 
#   pl_tags=["name-guessing", "pipeline-2"]
# )

import litellm

response = litellm.completion(
	model="gpt-3.5-turbo",
	messages=[
		{"role" : "system", "content" : ""},
		{"role" : "user", "content" : "Say \"hello world\"."},
	],
)

print(response)
