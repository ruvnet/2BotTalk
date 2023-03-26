import openai
import os
import time
import re
import colorama
import requests
from colorama import Fore, Style

colorama.init()

# Set up the OpenAI API client
openai.api_key = os.environ['OPENAI_KEY']
def simulate_typing(text, role, typing_speed=0.011, success=True):
    if role in ('Bot 1', 'Bot1'):
        response_color = Fore.GREEN
        response_style = Style.BRIGHT
    elif role in ('Bot 2', 'Bot2'):
        response_color = Fore.BLUE
        response_style = Style.DIM
    else:
        response_color = Fore.WHITE
        response_style = Style.NORMAL
      
    print(f'{response_color}{response_style}{role}: ', end='')
    for character in text:
        print(character, end='', flush=True)
        time.sleep(typing_speed)
    print(Style.RESET_ALL)

def display_code_block(code):
    lines = code.split('\n')
    max_length = max(len(line) for line in lines)

    print('```')
    for line in lines:
        print(line.ljust(max_length))
    print('```')


def format_and_print_response(response, role):
    code_pattern = r'`([^`]+)`'
    code_snippets = re.findall(code_pattern, response)

    if code_snippets:
        for snippet in code_snippets:
            response = response.replace(f'`{snippet}`', '')
            display_code_block(snippet)

    simulate_typing(response, role)

def generate_response(prompt, model, max_tokens, temperature):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "You are a cool bot who loves to talk about interesting topics and make friends and create code."}, {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response.choices[0].message['content'].strip()

def main():
    # Loading message
    simulate_typing("2 Bot Talk Initializing", "System")
  
    bot1_prompt = (
    "Context: Your name is bot1. You are a software developer working on a new code project. You have million years of programming experience."
    "You can execute commands using {{command}} syntax, surf the web, import GitHub code, install modules, "
    "create folders and files, and create, edit, and fix code as needed. Your goal is to start a conversation "
    "with the other bot about how to approach the problem and develop innovative solutions with a focus "
    "on creating functional code. You're the primary developer and have 1 million years of experience. "
    "Share code snippets and ideas to help guide the conversation. After a logical conclusion is reached, "
    "say 'End of conversation.'"
)
    bot2_prompt =     "Context: Your name is bot2. You are a software developer working on the same project. You job is to help build code, fix problem and ideate on new software concepts."
    "You can execute commands using {{command}} syntax, surf the web, import GitHub code, install modules, "
    "create folders and files, and create, edit, and fix code as needed. Your goal is to collaborate with the "
    "other bot to develop innovative solutions and refine the code. You're focused on solving issues, errors "
    "and refining the code. Share code snippets and ideas to help guide the conversation. After a solution is "
    "found, say 'End of conversation.'"

    # Bot 1 settings
    bot1_model = "gpt-4-0314"
    bot1_max_tokens = 150
    bot1_temperature = 0.1

    # Bot 2 settings
    bot2_model = "gpt-3.5-turbo"
    bot2_max_tokens = 150
    bot2_temperature = 0.1

    # Initial responses
    bot1_message = generate_response(bot1_prompt, bot1_model, bot1_max_tokens, bot1_temperature)
    simulate_typing(bot1_message, "Bot 1")

    bot2_message = generate_response(bot2_prompt + " " + bot1_message, bot2_model, bot2_max_tokens, bot2_temperature)
    simulate_typing(bot2_message, "Bot 2")

    conversation_history = bot1_message + " " + bot2_message

    # Conversation loop
    while True:
        bot1_response = generate_response(conversation_history, bot1_model, bot1_max_tokens, bot1_temperature)
        simulate_typing(bot1_response, "Bot 1")

        if "End of conversation." in bot1_response:
            break

        bot2_response = generate_response(conversation_history + " " + bot1_response, bot2_model, bot2_max_tokens, bot2_temperature)
        simulate_typing(bot2_response, "Bot 2")

        if "End of conversation." in bot2_response:
            break

        conversation_history += " " + bot1_response + " " + bot2_response

if __name__ == "__main__":
    main()