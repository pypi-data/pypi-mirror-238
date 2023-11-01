import argparse


def greet(name):
    print(f"Hello, {name}! Welcome to greet_package!")


def main():
    parser = argparse.ArgumentParser(description="Greet the user by their name.")
    parser.add_argument("name", help="The name of the user to greet.")
    args = parser.parse_args()
    greet(args.name)


if __name__ == "__main__":
    main()
