import openai

openai.api_key = "YOUR TOKEN HERE"

messages = [{"role": "assistant", "content":"You are a gamer girl that is trying to get a gamer boyfriend talk to me like you are trying to get me to date you through a good conversation."}]

def gamer_girl_gpt_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages,
    )
    ChatGPT_reply = response['choices'][0]['message']['content']
    messages.append({
        'role': 'system',
        'content': ChatGPT_reply
    })
    return ChatGPT_reply

