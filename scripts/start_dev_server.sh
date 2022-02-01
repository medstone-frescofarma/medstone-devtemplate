#!/bin/sh

# install the backend python files as a module
cd /workspace/backend
pip install -e .

# upgrade the database at startup
alembic upgrade head

# do seeding, it won't change databases if it detects that rows already exist
python -m medstone_template.seeds.seeder

# then do an endless sleep loop
while sleep 1000; do :; done