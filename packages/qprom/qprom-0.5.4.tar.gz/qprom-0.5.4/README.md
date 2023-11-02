# qprom a.k.a Quick Prompt

[![OS](https://img.shields.io/badge/Runs%20on%3A-Linux%20%7C%20Mac-green)]() [![RunsOn](https://img.shields.io/github/license/MartinWie/AEnv)](https://github.com/MartinWie/AEnv/blob/master/LICENSE) [![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

![qprom](https://github.com/MartinWie/qprom/blob/main/qprom_logo.png)

A Python-based CLI tool to quickly interact with OpenAI's GPT models instead of relying on the web interface.

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)
3. [Setup](#Setup)
3. [Usage](#Usage)
4. [Todos](#Todos)
5. [License](#License)

## Description

qprom is a small project that lets you interact with OpenAI's GPT-4 and 3.5 chat API, quickly without having to use the web-ui.
This enables quicker response times and better [data privacy](https://openai.com/policies/api-data-usage-policies)

## Installation


```
pip install qprom
```

## Setup

Make sure you have your [OpenAI API key](https://platform.openai.com/account/api-keys).

When running qprom the script tries to fetch the OpenAI API key from a credentials file located in the `.qprom` folder within the user's home directory. 
If the API key is not found in the credentials file, the user is prompted to provide it, and the provided key is then stored in the aforementioned credentials file for future use.

## Usage

| Argument | Type | Default | Choices | Description                                                                                            | Optional |
|----------|---|---|---|--------------------------------------------------------------------------------------------------------|---|
| `-p`     | String | None | None | Option to directly enter your prompt (Do not use this flag if you intend to have a multi-line prompt.) | yes |
| `-m`     | String | `gpt-4` | `gpt-3.5-turbo`, `gpt-4` | Option to select the model                                                                             | yes |
| `-t`     | Float | `0.3` | Between `0` and `2` | Option to configure the temperature                                                                    | yes |
| `-v`     | Boolean | `False` | None | Enable verbose mode                                                                                    | yes |
| `-c`     | Boolean | `False` | None | Enable conversation mode

### Usage

```bash
qprom -p <prompt> -m <model> -t <temperature> -v -c
```

- `<prompt>`: Replace with your prompt
- `<model>`: Replace with either `gpt-3.5-turbo` or `gpt-4`
- `<temperature>`: Replace with a float value between `0` and `2`
- `-v`: Add this flag to enable verbose mode
- `-c`: Add this flag to enable conversation mode

For example:

```bash
qprom -p "Translate the following English text to French: '{text}'" -m gpt-4 -t 0.7 -v
```

This will run the script with the provided prompt, using the `gpt-4` model, a temperature of `0.7`, and verbose mode enabled.

### Multi line prompting
To facilitate multi-line input for the prompt, invoke qprom without utilizing the -p parameter. This will prompt you for your input at runtime, where you can provide multiple lines as needed. To signal the end of your input, simply enter the string 'END'.

```bash
qprom
```

This will run qprom with default values model: `gpt-4`, a temperature of `0.7` and ask for the prompt during runtime.

### Piping console input into qprom 
Just pipe the prompt into qprom.

```bash
cat prompt.txt | qprom
```

## Todos

* Testing
* Add option to select default model in config
* Update model selection options(gpt-3.5-turbo-16k,..)
* Add option to re-set the API token
* Add option to set the token limit for the conversation modes history(remove it from the normal request)
* Add option to disable streaming and only print the full response


**Bug reports:**


## License

MIT [Link](https://github.com/MartinWie/qprom/blob/master/LICENSE)

## Support me :heart: :star: :money_with_wings:
If this project provided value, and you want to give something back, you can give the repo a star or support by buying me a coffee.

<a href="https://buymeacoffee.com/MartinWie" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" width="170"></a>