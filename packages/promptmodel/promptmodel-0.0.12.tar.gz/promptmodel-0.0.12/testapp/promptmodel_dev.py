"""This single file is needed to build the Client development dashboard."""

from promptmodel import Client
from main import client as main_client
# Example imports
# from <dirname> import < objectname>

app = Client()

# Example usage
# This is needed to integrate your codebase with the prompt engineering dashboard
app.include(main_client)

app.register_sample(
	name="function_call_test/1",
	content={"user_message" : "What is the weather like in Boston?"}
)

from main import get_current_weather
get_current_weather_desc = {
	"name": "get_current_weather",
	"description": "Get the current weather in a given location",
	"parameters": {
	"type": "object",
	"properties": {
		"location": {
		"type": "string",
		"description": "The city and state, e.g. San Francisco, CA"
		},
		"unit": {
		"type": "string",
		"enum": ["celsius", "fahrenheit"]
		}
	},
	"required": ["location"]
	}
}

app.register_function(
	get_current_weather_desc,
 	get_current_weather
)