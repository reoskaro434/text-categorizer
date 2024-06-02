import win32clipboard
import time
def set_clipboard_text(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

def get_clipboard_text():
    win32clipboard.OpenClipboard()
    clipboard_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return clipboard_data

def format_to_latex(input_string):
    lines = input_string.split('\n')
    formatted_lines = ['\\begin{itemize}']
    for line in lines:
        if line.strip():  # Sprawdzenie, czy linia nie jest pusta
            category, number = line.split(':')
            number = number.split('%')[0]
            formatted_lines.append(f'    \\item {category.strip().capitalize()}:{number}\\%')
    formatted_lines.append('\\end{itemize}')

    return '\n'.join(formatted_lines)

# Przykładowe dane wejściowe
while True:

    input_data = get_clipboard_text()

    try:

        formatted = format_to_latex(input_data)
        set_clipboard_text(formatted)
        print(formatted)
    except Exception:
        print('save tags!')

    time.sleep(2)