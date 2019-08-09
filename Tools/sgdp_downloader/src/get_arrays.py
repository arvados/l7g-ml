import argparse
import re
import sys


def get_arrays():

    # Settingx up inputs
    parser = argparse.ArgumentParser(prog="get_arrays",
                                     description="Get arrays of URLs and \
                                     filenames from listing of URLs.")
    parser.add_argument("url_list", metavar="URL_LIST", nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help="Input URL list file via stdin")
    parser.add_argument("-s", "--singletest", help="Generates a yml for a single \
                        step for CWL testing", action="store_true")
    parser.add_argument("-p", "--printsamples", help="Prints the first 5 items in \
                        the constructed arrays", action="store_true")
    parser.add_argument("-m", "--minitest", help="Generates a yml containing the \
                        first 5 items in arrays", action="store_true")
    parser.add_argument("-f", "--filenames", help="creates a txt of all filenames \
                        in a single file", action="store_true")

    args = parser.parse_args()
    url_list = args.url_list
    single_test = args.singletest
    print_samples = args.printsamples
    mini_test = args.minitest

    # Setting up arrays
    urls = []
    filenames = []

    # Setting up regex
    regex = r"filename\%3D(.*)&response-content-type"

    for line in url_list:
        line = line.strip()
        urls.append(line)

        matches = re.search(regex, line)
        if matches:
            for group in range(0, len(matches.groups())):
                group = group + 1
                filenames.append(matches.group(group))

    if print_samples:
        print(urls[0:5])
        print(filenames[0:5])

    if single_test:
        with open('../yml/single.yml', 'w') as file_handler:
            file_handler.write("filename: {}\n\n".format(filenames[0]))
            file_handler.write("url: {}\n".format(urls[0]))

    if filenames:
        with open('../yml/filenames.txt', 'w') as file_handler:
            for file in filenames:
                file_handler.write("{}\n".format(file))

    if mini_test:
        with open('../yml/mini.yml', 'w') as file_handler:
            file_handler.write("fn_list: {}\n\n".format(filenames[0:5]))
            file_handler.write("url_list: {}\n".format(urls[0:5]))

    with open('../yml/manifest.yml', 'w') as file_handler:
            file_handler.write("fn_list: {}\n\n".format(filenames))
            file_handler.write("url_list: {}\n".format(urls))

if __name__ == '__main__':
    get_arrays()
