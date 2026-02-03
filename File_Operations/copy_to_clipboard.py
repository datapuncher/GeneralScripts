#!/usr/bin/python

# Test module pyperclip by copying the file(name) to the ciplboard
import pyperclip

file_name = input("Please enter the file: ")

def copy_file_to_clipboard(file_name):
    try:
        with open(file_name, 'r') as f:
            file_content = f.read()
            pyperclip.copy(file_name)
            print(f"Contents of '{file_name}' copied to clipboard.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        printf(f"An error has occured: {e}")

copy_file_to_clipboard(file_name)
