import configparser
import tkinter as tk
from tkinter import messagebox, simpledialog
from TeXtation.api_utils import get_latex_equation
import os

def convert_prompt(text_input_widget, text_output_widget):
    """
    Takes text from a Text widget, processes it to get a LaTeX equation,
    and then displays the LaTeX equation in another Text widget.

    :param text_input_widget: The Text widget from which to get the user input.
    :param text_output_widget: The Text widget where the LaTeX equation will be displayed.
    """
    # Extract the input prompt from the Text widget
    prompt = text_input_widget.get("1.0", tk.END).strip()

    # Get the LaTeX equation using the extracted prompt
    latex_equation = get_latex_equation(prompt)

    # Clear the output Text widget and insert the LaTeX equation
    text_output_widget.delete("1.0", tk.END)
    text_output_widget.insert(tk.END, latex_equation)


def copy_to_clipboard(output_widget, root):
    """
    Copies the text from the output Text widget to the system clipboard
    and optionally shows a success message.

    :param output_widget: The Text widget from which the text will be copied.
    :param root: The Tkinter root window, used to access the clipboard.
    """
    try:
        root.clipboard_clear()  # Clear the clipboard
        text_to_copy = output_widget.get("1.0", tk.END).strip()  # Get text from output
        root.clipboard_append(text_to_copy)  # Append text to the clipboard
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy: {e}")


def ask_api_key():
    """
    Prompts the user to enter their API Key in a dialog box. If provided,
    saves the API key in the 'config.ini' file under the 'API' section.
    """
    # Create a new Tk window and hide it
    root = tk.Tk()
    root.withdraw()

    # Prompt the user to input the API Key
    api_key = simpledialog.askstring("API Key", "Enter your API Key:", parent=root)

    if api_key:  # If the user provided an API key
        # Initialize the config parser
        config = configparser.ConfigParser()

        # Check if 'config.ini' exists, if not, create it with the default sections/values
        if not os.path.exists('../config.ini'):
            config['API'] = {'key': ''}
            with open('../config.ini', 'w') as configfile:
                config.write(configfile)

        # Read the current config
        config.read('config.ini')

        # Update the API section with the new key
        config['API']['key'] = api_key

        # Write the updated configuration back to 'config.ini'
        with open('../config.ini', 'w') as configfile:
            config.write(configfile)

    # Destroy the temporary window
    root.destroy()


