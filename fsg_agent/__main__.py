from .fsg_agent import FSGAgent

################################################################################
#
# Runs from top
#
# python3 -m fsg_agent
#
################################################################################

if __name__ == "__main__":
    FSGAgent("127.0.0.1", 8080, "/ws")
