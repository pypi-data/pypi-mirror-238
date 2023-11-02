# parse the output of test-images

import re

# WIP - not git added 

def read_test(f):
    result = []
    for line in f:
        pass


def read_tests(filenames):
    result = []
    for filename in filenames:
        paths = [ "/root/nbhosting/sctipts/tests", "."]
        for path in paths:
            fullname = os.path.join(path, filename)
            try:
                with open(fullname) as f:
                    result += read_test(f)
                break
            except:
                pass
        print("input {filename} not found".format(**locals()))
    return result
