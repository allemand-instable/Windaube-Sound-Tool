from interface import run

from logger import *

def main():
    program_log.info("Starting program")
    run()

# Définie la main
if __name__ == "__main__":
    # resetting the log
    
    try:
        main()
    except Exception as e:
        print("UUUHHHHHHH... an error occured, please check the log file")
        program_log.error('Error at %s', 'division', exc_info=e)