import PythonTools.Constants
from prompt_toolkit import PromptSession

def print_help_message():

    print("This is a help message.")

def main():

    known_responses = { "help" : print_help_message,
                        "h" : print_help_message,
                        "quit" : exit,
                        "q" : exit,
                        "exit" : exit,
                      }

    # Create prompt object.
    session = PromptSession()

    while True:

        # Do multiple input calls.
        user_choice = session.prompt("Loewner > ")

        if user_choice in known_responses:

            known_responses[user_choice]()

if __name__ == "__main__":
    main()

