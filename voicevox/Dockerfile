ARG BASE_TAG=nvidia-latest

FROM voicevox/voicevox_engine:${BASE_TAG}

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y --no-install-recommends curl
