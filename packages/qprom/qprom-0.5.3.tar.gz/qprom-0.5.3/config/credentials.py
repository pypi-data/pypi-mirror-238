# Function to update the credentials file
import configparser
import os


def update_credentials(path, api_key):
    # Ensure the directory exists, if not create it
    os.makedirs(os.path.dirname(path), exist_ok=True)

    config = configparser.ConfigParser()
    config.read(path)
    if 'default' not in config.sections():
        config.add_section('default')
    config.set('default', 'openai_api_key', api_key)
    with open(path, 'w') as configfile:
        config.write(configfile)


def get_api_key():
    # Create a config parser
    config = configparser.ConfigParser()

    # Get the path to the credentials file
    credential_path = os.path.join(os.path.expanduser('~'), '.qprom', 'credentials.ini')

    # Read the credentials file
    config.read(credential_path)

    # Check if the API key exists
    if config.has_option('default', 'openai_api_key'):
        api_key = config.get('default', 'openai_api_key')
    else:
        print('OpenAI API key not found.')
        api_key = input('Please enter your OpenAI API key: ')
        update_credentials(credential_path, api_key)

    return api_key
