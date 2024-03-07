from optparse import OptionParser
from os.path import isfile

from PIL import Image

import pytesseract


def screenverifier(screenpath, args):
    text = pytesseract.image_to_string(Image.open(screenpath))
    missing = []

    for arg in args:
        if arg not in text:
            missing.append(arg)
    
    if missing:
        raise Exception(f"Below sentences are missing: {missing}")


def main():
    usage = "python3 screenverifier.py --screenpath <path to file with screenshot> 'text1' 'text2' ... 'textN'"

    parser = OptionParser(usage)
    parser.add_option("-s", "--screenpath", dest="screenpath", help="screenpath")

    (options, args) = parser.parse_args()

    if not options.screenpath:
        parser.error('screenpath is missing')
    if not len(args):
        parser.error('no text specified')
    
    if not isfile(options.screenpath):
        print("Input file does not exist")
        exit(-1)
    
    screenverifier(options.screenpath, args)

if __name__ == "__main__":
    main()