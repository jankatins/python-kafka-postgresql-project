"""The Producer"""

from .producer import main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Producer: Bye!")
