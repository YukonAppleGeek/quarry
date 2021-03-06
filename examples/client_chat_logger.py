"""
Chat logger example client

Stays in game and prints player chat to console.
"""

from twisted.internet import reactor, defer
from quarry.net.client import ClientFactory, SpawningClientProtocol
from quarry.auth import ProfileCLI


class ChatLoggerProtocol(SpawningClientProtocol):
    def packet_chat_message(self, buff):
        p_text = buff.unpack_chat()

        # 1.7.x
        if self.protocol_version <= 5:
            pass
        # 1.8.x
        else:
            p_position = buff.unpack('B')

        self.logger.info(":: %s" % p_text)


class ChatLoggerFactory(ClientFactory):
    protocol = ChatLoggerProtocol


@defer.inlineCallbacks
def run(args):
    # Log in
    profile = yield ProfileCLI.make_profile(args)

    # Create factory
    factory = ChatLoggerFactory(profile)

    # Connect!
    yield factory.connect(args.host, args.port)


def main(argv):
    parser = ProfileCLI.make_parser()
    parser.add_argument("host")
    parser.add_argument("-p", "--port", default=25565, type=int)
    args = parser.parse_args(argv)

    run(args)
    reactor.run()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])