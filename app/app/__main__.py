from argparse import ArgumentParser
from os import getenv
from app import Server


def create_args_parser():
    parser = ArgumentParser()
    parser.set_defaults(func=lambda x: parser.print_help())

    parser.add_argument('-b', '--broker-url',
                        default=getenv('BROKER_URL', 'localhost:5672'),
                        required=True)
    parser.add_argument('-s', '--subscribe-address',
                        default=getenv('SUBSCRIBE_ADDRESS', None),
                        required=True)
    parser.add_argument('-p', '--publish-address',
                        default=getenv('PUBLISH_ADDRESS', 'events'),
                        required=True)
    parser.add_argument('-ps', '--publish-subject',
                        default=getenv('PUBLISH_SUBJECT', None),
                        required=True)

    return parser


def parse_args(parser, argv=None):
    if argv is None:
        return parser.parse_args()
    else:
        return parser.parse_args(argv=argv)


def main(argv=None):
    parser = create_args_parser()
    args = parse_args(parser, argv=argv)
    server = Server(
        args.broker_url,
        args.subscribe_address,
        args.publish_address,
        args.publish_subject
    )
    try:
        server.run()
    except KeyboardInterrupt:
        pass
