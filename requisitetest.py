try:
    import sys
    from colorama import Fore, Style
    import atexit
    import argparse
    import random
except KeyboardInterrupt:
    print('[!] Exiting.')
    sys.exit()
except:
    print('[!] Missing requirements. Try running python3 -m pip install -r requirements.txt')
    sys.exit()
