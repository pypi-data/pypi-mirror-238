def get_multiline_input():
    print("Enter your prompt. Finish by typing 'END' on a new line:")
    lines = []
    while True:
        line = input()
        if line == 'END':
            break
        lines.append(line)
    return '\n'.join(lines)
