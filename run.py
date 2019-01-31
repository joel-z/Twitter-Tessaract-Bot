import sys
import os
from src.main import main

if __name__ == "__main__":
    print("PUMP IT MCAFEE!")
    print("-" * 50)
    try:
        main()
    except:
        import traceback

        traceback.print_exc()
        print("-" * 50)
        print("WOOPS, something wrong happend... save this blob of text and send it to support please :)")
        raw_input("Press any key to continue...")
