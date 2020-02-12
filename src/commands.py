import os
import io
import argparse
import re


def echo(args, input_text=""):
    """
    prints arguments
    :param args: arguments
    :param input_text: not used
    :return: arguments separated by space
    """
    return " ".join(args) + "\n"


def cat(args, input_text=""):
    """
    print file(s) content
    :param args: files
    :param input_text: printed text if args=[]
    :return: files content
    """
    if args == []:
        return input_text
    else:
        answer = ""
        for file in args:
            with open(file, "r") as input:
                answer += input.read()
        return answer


def wc(args, input_text=""):
    """
    prints lines number, words number and bytes number of the file
    :param args: files
    :param input_text: used if files=[]
    :return: lines words bytes filename
    """

    def simple_wc(file):
        with open(file, "r") as input:
            lines = input.readlines()
            lines_num = len(lines)
            words_num = sum([len(line.split()) for line in lines])
            size = os.stat(file).st_size
            return str(lines_num) + " " + str(words_num) + " " + str(size) + " " + file + "\n"

    if args == []:
        with io.StringIO(input_text) as input:
            lines = input.readlines()
            lines_num = len(lines)
            words_num = sum([len(line.split()) for line in lines])
            size = len(input_text.encode("utf-8"))
            return str(lines_num) + " " + str(words_num) + " " + str(size) + "\n"

    else:
        answer = ""
        for file in args:
            answer += simple_wc(file)
        return answer


def grep(args, input_text=""):
    """
    searches all lines in file(s) which contain a match to a regular expression
    options:
    -i: case ignoring
    -w: search only matches that form whole word
    -A n: prints n lines after line with found match
    :param args: keys, pattern, filenames
    :param input_text: used as search area if no filenames was provided
    :return: result string
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="case ignoring", action="store_true", default=False)
    parser.add_argument("-w", help="full words only", action="store_true", default=False)
    parser.add_argument("-A", help="prints n lines after matching line", type=int, default=0)
    parser.add_argument("regexp", help="regular expression", type=str)
    parser.add_argument("files", help="file", type=str, nargs="*")
    args = parser.parse_args(args)
    regexp = args.regexp
    files = args.files
    if files == []:
        texts = [input_text.split("\n")]
    else:
        texts = []
        for file in files:
            f = open(file, "r")
            texts.append(f.read().split('\n'))

    def find_in_string(s):
        """
        searches match in string accordingly to all options
        """
        ms = re.findall(regexp, s, flags=re.IGNORECASE if args.i else 0)
        return any([ms != []] if not args.w else [m.find(' ') == -1 for m in ms])

    def matching(text):
        """
        returns output for one text (from one file)
        """
        ans = []
        for i, line in enumerate(text):
            if find_in_string(line):
                if args.A == 0:
                    ans.append(line + "\n")
                else:
                    ans.append("\n".join(text[i:i + args.A + 1]) + "\n\n")
        return ans

    if len(texts) == 1:
        return "".join(matching(texts[0]))
    else:
        ans = ""
        for text, file in zip(texts, files):
            m = matching(text)
            if not m:
                continue
            ans += file + ":\n" + "".join(m)
        return ans


def pwd(args, input_text=""):
    """
    prints current directory
    :param args: not used
    :param input_text: not used
    :return: path to current directory
    """
    return os.path.abspath(os.getcwd()) + "\n"


def exit_(args, input_text=""):
    """
    exit programm
    :param args: not used
    :param input_text: not used
    :return: exits
    """
    exit(0)
