import sys
import openai
from arguments import get_args
from config.credentials import get_api_key
from gpt.request import openai_request, print_streamed_response
from qprom.utils import get_multiline_input


def main():
    openai.api_key = get_api_key()

    args = get_args()

    model = args.m
    temperature = args.t
    verbose = args.v
    input_string = args.p

    # Check if stdin has data
    if not sys.stdin.isatty():
        input_string = sys.stdin.read().strip()

    if input_string is None:
        input_string = get_multiline_input()

    if verbose:
        print(f"Selected model: {model}")
        print(f"Selected temperature: {temperature}")
        print(f"Prompt: {input_string}")
        print("Response:")

    response = openai_request(input_string, model, temperature)
    print_streamed_response(response)


if __name__ == "__main__":
    main()
