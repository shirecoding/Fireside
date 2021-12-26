#!/bin/bash

bash -c "cd templates/react-templates && npm run build"
./manage.py collectstatic --no-input
