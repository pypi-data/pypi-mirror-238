import customtkinter as ctk
from TeXtation.gui_utils import convert_prompt, copy_to_clipboard, ask_api_key
import tkinter as tk


def main():
    # Set the theme of CTk
    ctk.set_appearance_mode("Dark")  # Other options: "Light", "System"
    ctk.set_default_color_theme("green")  # You can also create a custom theme dictionary

    root = ctk.CTk()
    root.title("TeXtation")

    # Set the window size to be a little wider
    root.geometry("250x450")  # Width x Height in pixels

    # Input text widget
    label_input = ctk.CTkLabel(root, text="Enter your prompt:")
    label_input.pack(pady=10, padx=10)
    text_input = ctk.CTkTextbox(root, height=100, corner_radius=10)
    text_input.pack(pady=10, padx=10)

    # Output text widget
    label_output = ctk.CTkLabel(root, text="LaTeX Output:")
    label_output.pack(pady=10, padx=10)
    text_output = ctk.CTkTextbox(root, height=100, corner_radius=10)
    text_output.pack(pady=10, padx=10)

    # Button to trigger conversion
    convert_button = ctk.CTkButton(root, text="Convert", command=lambda: convert_prompt(text_input, text_output))
    convert_button.pack(pady=10, padx=10)

    # Button to copy output to clipboard
    copy_button = ctk.CTkButton(root, text="Copy to Clipboard",fg_color= 'gray', command=lambda: copy_to_clipboard(text_output, root))
    copy_button.pack(pady=10, padx=10)

    # Menu bar - using standard Tkinter Menu but customizing colors
    menubar = tk.Menu(root, bg="white")

    # Adding a "Settings" dropdown menu with customized colors
    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(label="API Key", command=lambda: ask_api_key())  # Function needs to be defined
    menubar.add_cascade(label="Settings", menu=settings_menu, background="black", foreground="white")

    # Configure the root menu to use this menu bar
    root.config(menu=menubar)

    root.mainloop()


if __name__ == "__main__":
    main()
