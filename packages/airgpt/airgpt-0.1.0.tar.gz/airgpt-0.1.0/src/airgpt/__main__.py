from openai.error import RateLimitError, ServiceUnavailableError
import backoff
import openai
import os
import platform
import subprocess
from dotenv import load_dotenv


# A '.env' file with the following setting is needed:
# OPENAI_API_KEY=<your_open_ai_key>
load_dotenv()

# Set up the OpenAI API client
openai.api_key = os.getenv('OPENAI_API_KEY')

TEST = False
SLEEP_TIME = 5


def fatal_code(e):
    return 400 <= e.response.status_code < 500


def execute_command(cmd):
    """
    Execute the given command and display the results.
    """
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            shell=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'Command failed with error: {e.returncode}')
        print(e.stderr)


@backoff.on_exception(backoff.expo, (RateLimitError, ServiceUnavailableError), max_tries=3, max_time=600, giveup=fatal_code)
def get_command(user_input):
    print(f'Input: {user_input}\n')
    os_name = platform.system()
    prompt_text = f'Provide the terminal command for {os_name}: {user_input}, and keep only the command part.'

    # Set up the model and prompt
    model_engine = 'gpt-3.5-turbo'
    messages = [{'role': 'user', 'content': prompt_text}]
    # Generate a response
    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
    )

    # print(f'API response: {completion.choices[0]}')
    response = completion.choices[0]['message']['content']
    answer = response.strip()
    print(f'Got answer: {answer}\n')
    return answer


def main():
    continue_loop = True
    while continue_loop:
        # Get the user prompt, e.g.,
        # user_input = 'list all files in the current directory'
        # user_input = 'find the location of application "python"'
        # user_input = 'what's the current time'
        # user_input = 'find a csv file'
        user_input = input('[airgpt] How can I help you? ')
        if user_input == '' or user_input == 'q' or user_input == 'quit':
            continue_loop = False
        else:
            cmd = get_command(user_input)
            execute_command(cmd)


if __name__ == '__main__':
    main()
