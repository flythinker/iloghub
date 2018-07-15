import getopt
import sys

def test1():
    print('test1')
    opts, args = getopt.getopt(sys.argv[1:], 'f:', ['file'] )
    print("opts",opts)
    print("args", args)

if __name__ == "__main__":
    test1()