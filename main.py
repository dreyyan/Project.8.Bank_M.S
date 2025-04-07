 # # # # # # # # # # # # # # # # # # # # # # #
#        Project: Bank Management System      #
#         Author: dreyyan                     #
#       Language: Python                      #
#   Date Started: 03/22/2025                  #
#  Date Finished:                             #
 # # # # # # # # # # # # # # # # # # # # # # #

''' IMPORTS '''
import time
import json

''' MODULES '''
from modules.line_delay_animation import line_delay_animation
from modules.clear_screen import clear_screen
from modules.display_format import display_format

''' UTILITIES '''
# UTILITY: Simulate a time delay within specified seconds
def delay(s):
    time.sleep(s)

# UTILITY: Display formatted error message to the user
def error_message(message):
    print(f"ERROR: {message}.")
    delay(3)

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

# UTILITY: Print string input with proper spacing
def print_with_spacing(string_input, space):
    print((space * ' ') + string_input)
    delay(0.1)

''' BASE CLASS '''
class Bank:
    latest_account_id = 0 # To store the account id to be assigned for new users

    # CONSTRUCTOR
    def __init__(self, account_holder="N/A", account_id="", account_type="N/A", balance=0):
        self.account_holder = account_holder
        # Generate account ID if missing
        if account_id == "":
            Bank.latest_account_id += 1
            # Ensures 6-digit format
            self.account_id = str(Bank.latest_account_id).zfill(6)
        else:
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

    ''' METHODS: UTILITY '''
    # UTILITY: Display account's current balance
    def display_current_balance(self):
        print(f"* Current Balance: ₱{self.balance}")
        delay(0.1)

    def is_complete_information(self) -> bool:
        # If either information is incomplete, display an error
        if self.account_holder or self.account_id or self.account_type:
            error_message("Invalid Access: Please make sure to fill out all account information")
            return False
        else: return True

    ''' METHODS: OPERATIONS '''
    def deposit(self):
        if not self.is_complete_information(): # Check for complete information before proceeding
            return
        
        while True:
            clear_screen()
            display_header("WITHDRAW", 8, False)

            # Display account holder's current balance
            self.display_current_balance()
            # Display common deposit amounts
            display_format('=', 26)

            for key, value in self.denominations.items():
                if key in [4, 5]:
                    print(f" [{key}] {value}")
                    delay(0.1)
                    continue
                print(f" [{key}] ₱{value}")
                delay(0.1)
            display_format('=', 26)

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
                clear_screen()
                display_header("DEPOSIT", 9, True)
                try:
                    print(" NOTE: Amount <= ₱50,000 *")
                    display_format('=', 26)

                    # Display account holder's current balance
                    self.display_current_balance()
                    # Display common deposit amounts
                    display_format('=', 26)

                    # Prompt user to enter amount to deposit
                    deposit_amount = int(input("Enter amount[₱]: ").strip())

                    # ERROR: Negative deposit amount
                    if deposit_amount < 1:
                        error_message("Invalid amount, please enter a positive value")
                        continue

                    # ERROR: Greater than max deposit amount
                    elif deposit_amount > 50000:
                        error_message("Exceeded maximum deposit amount")
                        continue

                except ValueError:
                    error_message("Invalid choice, please enter a valid number")

                else: break

        # Add deposit amount to the current balance
        self.balance += deposit_amount

        # Display transaction details
        clear_screen()
        display_header("DEPOSIT", 9, True)
        print_with_spacing("[ DEPOSIT: Success ]", 3)
        delay(0.1)
        display_format('=', 26)
        print(f"Amount: ₱{deposit_amount}")
        delay(0.1)
        print(f"New Balance: ₱{self.balance}")
        delay(0.1)
        display_format('=', 26)

        # Return to menu
        press_enter_to_continue()

    def withdraw(self):
        if not self.is_complete_information(): # Check for complete information before proceeding
            return
        
        while True:
            clear_screen()
            display_header("WITHDRAW", 8, False)

            # ERROR: Insufficient balance to withdraw
            if self.balance == 0:
                error_message("No account balance..")
                add_to_balance_choice = input("Go to deposit[yes/no]?: ").strip()

                # Convert to lowercase for safety
                add_to_balance_choice = add_to_balance_choice.lower()

                # Redirect user to deposit
                if add_to_balance_choice in ["yes", 'y']:
                    self.deposit()
                    return # Return to menu after user deposits
                # Return to menu
                elif add_to_balance_choice in ["no", 'n']:
                    return
                else: # ERROR: Invalid user choice
                    error_message("Invalid choice, please enter 'yes' or 'no'")
                    continue


            # Display account holder's current balance
            self.display_current_balance()
            # Display common withdrawal amounts
            display_format('=', 26)

            for key, value in self.denominations.items():
                if key in [4, 5]:
                    print(f" [{key}] {value}")
                    delay(0.1)
                    continue
                print(f" [{key}] ₱{value}")
                delay(0.1)
            display_format('=', 26)

            try:
                # Prompt user to enter the amount to deposit
                withdrawal_input = int(input("Enter choice: ").strip())

                # Set withdrawal amount
                withdrawal_amount = self.denominations[withdrawal_input]

                if withdrawal_input == 5:
                    return

                # ERROR: Invalid key for withdrawal input
                elif withdrawal_input not in self.denominations.keys():
                    error_message("Invalid choice, please enter a valid option[1-5]")
                    continue

                elif withdrawal_input in [1, 2, 3]:
                    # ERROR: Withdrawal amount greater than the current balance
                    if withdrawal_amount > self.balance:
                        error_message("Withdrawal amount exceeds current balance")
                        continue

                else: break

            except ValueError:
                error_message("Invalid choice, please enter a number")
                continue

        # If amount is not a digit, prompt user to enter a custom amount
        if not isinstance(withdrawal_amount, int):
            while True:
                clear_screen()
                display_header("WITHDRAW", 8, False)
                try:
                    print("    NOTE: Amount > 0 *")
                    display_format('=', 26)

                    # Display account holder's current balance
                    self.display_current_balance()
                    # Display common deposit amounts
                    display_format('=', 26)

                    # Prompt user to enter amount to withdraw
                    withdrawal_amount = int(input("Enter amount[₱]: ").strip())

                    # ERROR: Negative withdrawal amount
                    if withdrawal_amount < 1:
                        error_message("Invalid amount, please enter a positive value")
                        continue

                    # ERROR: Withdrawal amount greater than current balance
                    elif withdrawal_amount > self.balance:
                        error_message("Withdrawal amount exceeds current balance")
                        continue

                except ValueError:
                    error_message("Invalid choice, please enter a valid number")
                    continue

                else: break

        # Add deposit amount to the current balance
        self.balance -= withdrawal_amount

        # Display transaction details
        clear_screen()
        display_header("WITHDRAW", 9, True)
        print_with_spacing("[ WITHDRAW: Success ]", 3)
        delay(0.1)
        display_format('=', 26)
        print(f"Amount: ₱{withdrawal_amount}")
        delay(0.1)
        print(f"New Balance: ₱{self.balance}")
        delay(0.1)
        display_format('=', 26)

        # Return to menu
        press_enter_to_continue()

    def display_account_details(self):
        clear_screen()
        display_header("ACCOUNT DETAILS", 5, True)
        display_format('=', 26)
        print(f"Account Holder: {self.account_holder}")
        delay(0.1)
        print(f"Account ID: {self.account_id}")
        delay(0.1)
        print(f"Account Type: {self.account_type}")
        delay(0.1)
        print(f"Balance: ₱{self.balance}")
        delay(0.1)
        display_format('=', 26)

        # Return to menu
        press_enter_to_continue()

    def edit_account_information(self):
        # Prompt user to enter name(account holder)
        while True:
            clear_screen()
            display_header("EDIT INFORMATION", 4, False)
            print(f"Current name: [{self.account_holder}]")
            print("Enter your name:")
            input_account_holder = input("↳ ").strip()

            # ERROR: Empty name input
            if input_account_holder == "":
                error_message("Account holder cannot be blank")

            # ERROR: Name contains digits
            elif any(c.isdigit() for c in input_account_holder):
                error_message("Name cannot contain digits")

            else: break

        # Set new name(account holder)
        self.account_holder = input_account_holder

        # Prompt user to select account type
        while True:
            clear_screen()
            display_header("EDIT INFORMATION", 4, False)

            line_delay_animation("[ Account Type ]", 0.02)
            line_delay_animation("1. Savings", 0.02)
            line_delay_animation("2. Checking", 0.02)
            line_delay_animation("3. Current", 0.02)
            display_format('=', 26)

            try:
                input_account_type = int(input("↳ ").strip())

                # ERROR: Out-of-range choice
                if input_account_type not in range(1, 4):
                    error_message("Out-of-bounds choice, please enter a digit between 1-3")
                else: break

            except ValueError:
                    error_message("Invalid choice, please enter a digit")

        clear_screen()
        display_header("EDIT INFORMATION", 4, False)

        print("* Congratulations! You have successfully filled out all information.")
        time.sleep(2)
        self.display_account_details() # Display account details after editing

    ''' METHODS: INTERFACE '''
    def display_main_menu(self):
        while True: # Display menu interface
            clear_screen()
            display_header("MAIN MENU", 8, True)
            display_format('=', 26)
            display_function(1, "Deposit")
            display_function(2, "Withdraw")
            display_function(3, "Account Details")
            display_function(4, "Edit Information")
            display_function(5, "Exit")
            display_format('=', 26)
            print(f"Balance: ₱{self.balance}")
            delay(0.1)
            display_format('=', 26)

            try:
                # Prompt the user to enter a choice
                user_input = int(input("Enter a choice: ").strip())

                # Exit program
                if user_input == 5:
                    print("exiting system...")
                    time.sleep(2)
                    exit(0)

                # Invoke function
                if user_input in self.function_list:
                    self.function_list[user_input]()  # Call function

                else:
                    error_message("Invalid choice, function does not exist")

            except ValueError:
                error_message("Invalid choice, please enter a number")

    def go_to_register_menu(self):
        while True:
            clear_screen()
            display_header("REGISTER", 8, False)
            display_format('=', 26)
            print("USERNAME ~ [5-20 chars.][no spaces]")
            print("PASSWORD ~ [5-20 chars.][one symbol]")
            display_format('=', 26)
            username = input("Username: ")

            if ' ' in username: # ERROR: Space character in username
                error_message("Username must not contain spaces")
            if len(username) < 5: # ERROR: Below minimum character limit
                error_message("Username must be at least 5 characters")
            elif len(username) > 20: # ERROR: Above maximum character limit
                error_message("Username must not exceed 20 characters")
            else: break


            get_input = input("")

    def go_to_login_menu(self):
        while True:
            clear_screen()
            display_header("LOGIN", 10, True)
            display_format('=', 26)
            username = input("Username: ").strip()

            get_input = input("")

start_program = Bank()
start_program.display_main_menu()
# start_program.go_to_register_menu()
# start_program.go_to_login_menu()