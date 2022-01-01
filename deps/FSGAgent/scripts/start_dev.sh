#!/bin/bash

pkill -f 'python3 /deps/FSGAgent/bin/fsg_agent'

fsg_agent &
