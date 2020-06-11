import argparse
import importlib
import json
import requests as r

parser = argparse.ArgumentParser(description='Set bintray info')
parser.add_argument('conanlib', type=str,
                    help='Name of conan class in conanfile.py')
parser.add_argument('username', type=str, help='Bintray username')
parser.add_argument('password', type=str, help='Bintray password')


def main(argvs):

    args = parser.parse_args(argvs)

    mod = importlib.import_module("conanfile")
    pkg = getattr(mod, args.conanlib)

    info = dict()
    info['desc'] = pkg.description
    info['licenses'] = [pkg.license]
    info['vcs_url'] = pkg.url
    info['website_url'] = pkg.homepage
    info['labels'] = list(pkg.topics)

    url = 'https://api.bintray.com/packages/sintef-ocean/conan/{}%3asintef' \
        .format(pkg.name)

    try:
        res = r.patch(url,
                      auth=(args.username, args.password),
                      data=json.dumps(info))

        if not res.ok:
            print("Could not set package info: {}".format(res.reason))
        else:
            print("Set package info: {}".format(res.reason))
    except Exception:
        print("WARNING failed to set package info")

    exit(0)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
