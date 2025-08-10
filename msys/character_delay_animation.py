import time
# UTILITY: display text with a typing effect
def character_delay_animation(stringInput, seconds):
    for char in stringInput:
        print(char, end="", flush=True)
        time.sleep(seconds)
    print()