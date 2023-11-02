# test.py
import openai

if __name__ == "__main__":
    # res = PromptModel("type_parsing").stream_and_parse()

    # for chunk in res:
    #     print(chunk)
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        message=[
            { "role" : "system", "content" : "You are a helpfull assistant."},
            { "role" : "user", "content" : "hello?"}
        ]
    )
    print(res)