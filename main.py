import requests
import termcolor
from termcolor import colored
import pyfiglet
import json

# Function to colorize text based on status code
def colored_status(text, status_code):
    if status_code == 400:
        return colored(text, "green")
    elif status_code == 404:
        return colored(text, "red")
    elif status_code == 302:  # Assuming 302 is a redirect status code
        return colored(text, "yellow")
    else:
        return text

    return colored(text, "white") # Default color

# Function to print colorized text
def colored_print(text, color="white"):
    print(colored(text, color))

# Banner text
banner = pyfiglet.figlet_format("ReConnect")
colored_print(colored_status(banner, 400))

# Initial URL and method input
url = input("Enter the URL to request: ")
method = input("Enter the HTTP method (GET, POST, PUT, etc.): ").upper()

# Main loop
while True:
    # Header manipulation loop
    headers = requests.structures.CaseInsensitiveDict()
    colored_print("Current headers:")
    for key, value in headers.items():
        colored_print(f"    {key}: {value}")

    while True:
        action = input(colored("Add, Modify, Delete, Next, or Quit (a/m/d/n/q)? ", "white")).lower()
        if action == "a":
            key = input(colored("Enter header key: ", "white"))
            value = input(colored("Enter header value: ", "white"))
            if key and value:
                headers[key] = value
            else:
                colored_print("Invalid header key or value", "red")
        elif action == "m":
            key = input(colored("Enter header key to modify: ", "white"))
            if key in headers:
                value = input(colored("Enter new header value: ", "white"))
                if value:
                    headers[key] = value
                else:
                    colored_print("Invalid header value", "red")
            else:
                colored_print(f"Header {key} not found", "red")
        elif action == "d":
            key = input(colored("Enter header key to delete: ", "white"))
            if key in headers:
                del headers[key]
            else:
                colored_print(f"Header {key} not found", "red")
        elif action == "n":
            break
        elif action == "q":
            exit()
        else:
            colored_print("Invalid action", "red")

        colored_print("Current headers:")
        for key, value in headers.items():
            colored_print(f"    {key}: {value}")

    # Prompt for URL and method
    url = input(colored(f"Enter the URL to request (current: {url}): ", "white")) or url
    method = input(colored(f"Enter the HTTP method (GET, POST, PUT, etc.) (current: {method}): ", "white")).upper() or method

    # Try making the request
    try:
        response = requests.request(method, url, headers=headers)
        status_code = response.status_code
        colored_status_text = colored_status(f"Status: {status_code}", status_code)
        colored_print(colored_status_text)

        # Try to decode the content as JSON
        try:
            beautified_content = json.dumps(response.json(), indent=4)
        except:
            beautified_content = response.text

        colored_print(f"StatusCode        : {status_code}")
        colored_print(f"StatusDescription : {response.reason}")
        colored_print(f"Content           : {response.text}")
        colored_print("RawContent        :")
        try:
            for chunk in response.iter_content(chunk_size=1024):
                colored_print(chunk.decode('utf-8', 'ignore'))
        except Exception as e:
            colored_print(f"Error reading raw content: {e}", "red")
        colored_print(f"RawContentLength  : {len(response.content)}")
        colored_print("Headers           :")
        for key, value in response.headers.items():
            colored_print(f"    {key}: {value}")

    # Handle exceptions
    except requests.exceptions.RequestException as e:
        colored_print(f"Request failed: {e}", "red")
    except json.JSONDecodeError as e:
        colored_print(f"JSONDecodeError: {e}", "red")
        beautified_content = response.text #If JSON decoding fails, use raw text
    except Exception as e:
        colored_print(f"An error occurred: {e}", "red")
    # Save the output to a file
    else:
        download = input(colored("Do you want to download the output to a file? (y/n): ", "white"))
        filename = ""
        content_to_save = ""

        if download.lower() == "y":
            filename = input(colored("Enter the filename to save as: ", "white"))
            content_to_save = response.text

        alter_response = input(colored("Do you want to alter the response before saving? (y/n): ", "white"))
        if alter_response.lower() == "y":
            content_to_save = input(colored("Enter the altered response: ", "white"))

        if filename:
            with open(filename, "w") as f:
                f.write(f"URL: {url}\n")
                f.write(f"Method: {method}\n")
                f.write(f"Status Code: {status_code}\n")
                f.write(f"Status Description: {response.reason}\n")
                f.write("Headers:\n")
                for key, value in response.headers.items():
                    f.write(f"    {key}: {value}\n")
                f.write(f"Content:\n{content_to_save}\n")
                f.write(f"RawContentLength: {len(response.content)}\n")

            colored_print(f"Output saved to {filename}", "green")
