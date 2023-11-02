import sys
import openai
from arguments import get_args
from config.credentials import get_api_key
from gpt.request import openai_request, print_and_return_streamed_response
from gpt.util import prepend_conversation_history
from qprom.utils import get_multiline_input


def main():
    openai.api_key = get_api_key()

    args = get_args()

    model = args.m
    temperature = args.t
    verbose = args.v
    input_string = args.p
    conversation_mode = args.c

    # Check if stdin has data
    if not sys.stdin.isatty():
        input_string = sys.stdin.read().strip()

    if verbose:
        print(f"Selected model: {model}")
        print(f"Selected temperature: {temperature}")
        print(f"Conversation mode enabled: {conversation_mode}")
        print(f"Prompt: {input_string}")
        print("Response:")

    first_loop = True

    # Initialize the list to store conversation strings
    conversation_history = []

    while first_loop or conversation_mode:
        try:
            if input_string is None:
                input_string = get_multiline_input(first_loop)

            # Check if we need to prepend history
            if conversation_history:
                input_string = prepend_conversation_history(conversation_history, input_string, 6500)

            # Store the current input with the label
            conversation_history.append(f"Human input: {input_string}")

            response = openai_request(input_string, model, temperature)
            answer = print_and_return_streamed_response(response)

            # Store the answer with the label
            conversation_history.append(f"OpenAI answer: {answer}")

            first_loop = False
            input_string = None

        except KeyboardInterrupt:
            # Handle KeyboardInterrupt's gracefully by exiting the while loop
            break


if __name__ == "__main__":
    main()
