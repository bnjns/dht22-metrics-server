FROM python:3.11.2-slim AS base

FROM base AS deps

WORKDIR /app
COPY Pipfile.lock ./
RUN python3 -m pip install --upgrade pip \
    && pip3 install pipenv \
    && pipenv requirements > requirements.txt


FROM base

ENV DEBIAN_FRONTEND=noninteractive

# Install the system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      bash \
      curl \
      gcc \
      make \
      libgpiod2 \
      python3-dev \
      python3-setuptools \
      swig \
      unzip \
    && pip3 install -U pip setuptools

# Install lgpio
RUN cd /tmp \
    && curl -O https://abyz.me.uk/lg/lg.zip \
    && unzip lg.zip \
    && cd lg \
    && make \
    && make install \
    && cd /tmp \
    && rm -rf lg.zip lg

WORKDIR /app

# Install python dependencies
COPY --from=deps /app/requirements.txt requirements.txt
RUN pip install -r requirements.txt && \
    rm requirements.txt

# Remove unneeded build tools
RUN apt-get remove -y \
    gcc \
    make \
    unzip

# Copy source
COPY src/server.py server.py
CMD ["python3", "server.py"]
