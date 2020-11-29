"""The Producer"""

import sys
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    command = sys.argv[-1]
    if command == 'producer':
        from .producer import main
    elif command == 'consumer':
        from .consumer import main
    else:
        print(f"Usage: {sys.argv[-1]} producer/consumer")
        sys.exit(1)


    env_path = os.environ.get('CHECKWEB_ENV_PATH', '../local.env')
    load_dotenv(dotenv_path=env_path)

    try:
        main()
    except KeyboardInterrupt:
        print(f"{command}: Bye!")
