''' IMPORTS '''
import time

''' MODULES '''
from modules.line_delay_animation import line_delay_animation
from modules.clear_screen import clear_screen
from modules.display_format import display_format

''' UTILITIES '''
def delay(s):
    time.sleep(s)

# UTILITY: Display formatted error message to the user
def error_message(message):
    print(f"ERROR: {message}.")
    delay(2)

# UTILITY: Display header for the interface /w appropriate formatting
def display_header(interface_name, space, is_odd):
    line_delay_animation("[ BANK MANAGEMENT SYSTEM ]", 0.1)
    if is_odd:
        print(((space - 1) * '-'), end='') # Output spacing
    else:
        print((space * '-'), end='')  # Output spacing
    line_delay_animation(f" {interface_name} {(space * '-')}", 0.1)

# UTILITY: Display the function in the main menu
def display_function(index, function_name):
    line_delay_animation(f"[{index}] {function_name}", 0.1)

# UTILITY: Prompt the user to press the Enter key to continue
def press_enter_to_continue():
    user_input = input("Press 'Enter' to continue...")

''' BASE CLASS '''
class Bank:
    # CONSTRUCTOR
    def __init__(self, account_holder, account_id, account_type, balance):
        self.account_holder = account_holder
        self.account_id = account_id
        self.account_type = account_type
        self.balance = balance

        # FUNCTION LIST
        self.function_list = {
            1: self.deposit,
            2: self.withdraw,
            3: self.display_account_details,
            4: self.edit_account_information
        }

        # COMMON DEPOSIT/WITHDRAWAL AMOUNT LIST
        self.denominations = {
            1: 500,
            2: 1000,
            3: 10000,
            4: "Custom amount",
            5: "Back"
        }

    # METHODS
    def deposit(self):
        while True:
            clear_screen()
            display_header("DEPOSIT", 9, True)
            # Display account holder's current balance
            print(f"Current Balance: ₱{self.balance}")
            delay(0.1)

            # Display common deposit/withdrawal amounts
            display_format('*', 26)
            for key, value in self.denominations.items():
                if key in [4, 5]:
                    print(f" [{key}] {value}")
                    delay(0.1)
                    continue
                print(f" [{key}] ₱{value}")
                delay(0.1)
            display_format('*', 26)

            try:
                # Prompt user to enter the amount to deposit
                deposit_input = int(input("Enter choice: ").strip())

                if deposit_input == 5:
                    return

                elif deposit_input not in self.denominations.keys():
                    error_message("Invalid choice, please enter a valid option[1-5]")

                else: break

            except ValueError:
                error_message("Invalid choice, please enter a number")

        # Set deposit value for pre-defined amounts
        deposit_amount = self.denominations[deposit_input]

        # If amount is not a digit, prompt user to enter a custom amount
        if not isinstance(deposit_amount, int):
            while True:
                try:
                    deposit_amount = int(input("Enter amount[₱]: ").strip())

                except ValueError:
                    error_message("Invalid choice, please enter a positive amount")

                else: break

        # Display transaction details
        print("[ DEPOSIT: Success ]")
        delay(0.1)
        display_format('*', 26)
        print(f"Amount: ₱{deposit_amount}")
        print(f"New Balance: ₱{self.balance}")





    def withdraw(self):
        clear_screen()
        display_header("WITHDRAW", 8, False)
        get_input = input("")

    def display_account_details(self):
        clear_screen()
        display_header("ACCOUNT DETAILS", 8, True)
        get_input = input("")

    def edit_account_information(self):
        clear_screen()
        display_header("EDIT ACCOUNT INFORMATION", 8, True)
        get_input = input("")

    def display_main_menu(self):
        while True: # Display menu interface
            clear_screen()
            display_header("MAIN MENU", 8, True)
            display_format('*', 26)
            display_function(1, "Deposit")
            display_function(2, "Withdraw")
            display_function(3, "Account Details")
            display_function(4, "Edit Information")
            display_function(5, "Exit")
            display_format('*', 26)

            try:
                # Prompt the user to enter a choice
                user_input = int(input("Enter a choice: ").strip())

                # Exit program
                if user_input == 5:
                    print("exiting system...")
                    time.sleep(2)

                # Invoke function
                if user_input in self.function_list:
                    self.function_list[user_input]()  # Call function
                    press_enter_to_continue()

                else:
                    error_message("Invalid choice, function does not exist")

            except ValueError:
                error_message("Invalid choice, please enter a number")

start_program = Bank("Adrian Tan", "117591120149", "Savings", 0)
start_program.display_main_menu()