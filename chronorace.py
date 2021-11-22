import argparse
import json
from http_request import HTTPRequest
from race import Race


def run_race_requests(args):
    with open(args.configuration) as config_file:
        config = json.load(config_file)

    if 'requests' not in config:
        raise Exception('Need a requests array.')

    proxy = config.get('proxy', None)
    verify = config.get('verify_ssl', None)
    print_response = config.get('print_response', False)

    race = Race()
    for request in config['requests']:
        if 'file' not in request:
            raise Exception('File must be specified.')

        race.add_request(
            HTTPRequest(request['file'], request.get('replacements', []), request.get('secure', True)),
            request.get('delay', 0), proxy, verify, print_response)

    race.go(config.get('threads', 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__, description='A tool to perform timed race conditions.')
    subparsers = parser.add_subparsers()

    run_race = subparsers.add_parser('race')
    run_race.add_argument('-c', '--configuration', type=str, required=True, help='Path to configuration file.')
    run_race.set_defaults(func=run_race_requests)

    parsed_args = parser.parse_args()

    try:
        func = parsed_args.func
    except AttributeError:
        parser.error("Too few arguments.")

    func(parsed_args)
