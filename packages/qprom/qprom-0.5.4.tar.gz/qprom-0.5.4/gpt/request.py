import sys

import openai
from gpt.util import get_token_amount_from_string


def openai_request(prompt: str, model: str, temperature: float):
    TOKEN_LIMIT = 6500
    if get_token_amount_from_string(prompt) > TOKEN_LIMIT:
        print(f"Token amount of {get_token_amount_from_string(prompt)} is to big. Stay below {TOKEN_LIMIT}!")
        return
    try:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            stream=True,
            messages=[
                {"role": "system",
                 "content": "Help answer user questions, provide solutions step by step."},
                {"role": "user", "content": prompt}
            ]
        )
        return response

    except openai.error.APIError as e:
        print("Error with the OpenAI API. Details:", e)
        return None

    except openai.error.RateLimitError as e:
        print("Rate limit exceeded. Please wait before making further requests. Details:", e)
        return None

    except openai.error.APIConnectionError as e:
        print("Connection error. Please check your internet connection. Details:", e)
        return None

    except openai.error.InvalidRequestError as e:
        print("Invalid request. Check your parameters. Details:", e)
        return None

    except openai.error.AuthenticationError as e:
        print("Authentication error. Please check your OpenAI API key. Details:", e)
        return None

    except openai.error.ServiceUnavailableError as e:
        print("OpenAI service is currently unavailable. Please try again later. Details:", e)
        return None

    except Exception as e:
        print("An unexpected error occurred:", e)
        return None


def print_and_return_streamed_response(response):
    # create variables to collect the stream of events
    collected_events = []
    final_output = ""
    # iterate through the stream of events
    for event in response:
        collected_events.append(event)  # save the event response
        if event['choices'][0]['delta'].get('content') is not None:
            event_text = event['choices'][0]['delta']['content']  # extract the text
            sys.stdout.write(event_text)
            sys.stdout.flush()  # ensures output is displayed immediately
            final_output += event_text
    return final_output