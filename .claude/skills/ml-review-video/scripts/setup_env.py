"""Explicit one-time credential installation; never prints contents or keys."""
import argparse
from pathlib import Path
from lib.credentials import copy_env_file, CredentialError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(copy_env_file(args.source, args.destination))
        return 0
    except CredentialError as error:
        print(str(error))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
