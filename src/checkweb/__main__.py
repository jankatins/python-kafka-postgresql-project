"""The Producer"""

import sys

if __name__ == '__main__':
    command = sys.argv[-1]
    if command == 'producer':
        from .producer import main
    elif command == 'consumer':
        from .consumer import main
    else:
        print(f"Usage: {sys.argv[-1]} producer/consumer")
        sys.exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print(f"{command}: Bye!")
