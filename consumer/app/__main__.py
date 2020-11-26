"""The Producer"""

from .consumer import main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Consumer: Bye!")
