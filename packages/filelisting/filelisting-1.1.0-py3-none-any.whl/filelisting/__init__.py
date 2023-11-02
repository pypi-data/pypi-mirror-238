import os as _os

import aaronparse.parser as _parser
import aaronparse.process_namespace as _pn


def main(args=None):
    parser = _parser.by_func(run)
    ns = parser.parse_args()
    fi = _pn.by_func(run, namespace=ns)
    if len(vars(ns)):
        raise ValueError
    files = fi.exec(run)
    for file in files:
        print(file)

def run(*targets):
    ans = list()
    for target in targets:
        if _os.path.isfile(target):
            ans.append(target)
            continue
        for (root, dirnames, filenames) in _os.walk(target):
            for filename in filenames:
                file = _os.path.join(root, filename)
                ans.append(file)
    return ans  
    
if __name__ == '__main__':
    main() 