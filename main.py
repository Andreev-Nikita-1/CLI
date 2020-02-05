from src.interpreter import perform
from src.parser import parse


def main():
    while True:
        print('$', end=' ')
        string = input()
        commands_parts = parse(string)
        output = perform(commands_parts)
        print(output)


if __name__ == "__main__":
    main()
