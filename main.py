# main.py

import argparse
from ocw_oer_export import create_csv, create_json

def main():
    parser = argparse.ArgumentParser(description='OCW OER Export')

    parser.add_argument('--create_csv', action='store_true', help='Create CSV file')
    parser.add_argument('--create_json', action='store_true', help='Create JSON file')

    args = parser.parse_args()

    if args.create_csv:
        create_csv()
    elif args.create_json:
        create_json()
    else:
        print("Please specify either --create_csv or --create_json.")

if __name__ == "__main__":
    main()
