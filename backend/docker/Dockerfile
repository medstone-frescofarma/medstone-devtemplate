FROM python:3.7-slim-buster
LABEL author="Koen Vijverberg <koen@vijverb.nl>"

# Install some basic utilities
RUN apt-get update && apt-get install -y wget curl ca-certificates sudo git bzip2 libx11-6 build-essential && rm -rf /var/lib/apt/lists/*

# setup flask application directory
RUN mkdir /app
WORKDIR /app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory
ENV HOME=/home/user
RUN chmod 777 /home/user
ENV PATH "$PATH:/home/user/.local/bin"

# install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# copy the source directory over to the docker container
COPY ./medstone_backend ./medstone_backend

# install the app as a module (in dev mode)
COPY ./setup.py .
RUN pip install -e .

COPY ./migrations ./migrations
COPY ./alembic.ini .

CMD ["uvicorn", "medstone_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
