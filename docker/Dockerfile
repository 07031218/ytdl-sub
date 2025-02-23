FROM ghcr.io/linuxserver/baseimage-alpine:3.17

###############################################################################
# YTDL-SUB INSTALL

COPY root/ /
RUN mkdir -p /config && \
    apk update --no-cache && \
    apk upgrade --no-cache && apk add unzip && \
    apk add --no-cache --repository=http://dl-3.alpinelinux.org/alpine/edge/main/ \
      vim \
      g++ \
      nano \
      make \
      python3=~3.10 \
      py3-pip \
      fontconfig \
      py3-setuptools && \
    # Install edge ffmpeg, ensure it is properly installed
    apk add --no-cache --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
      "ffmpeg>5.1" && \
      ffmpeg -version && \
    # Install phantomjs if using x86_64, ensure it is properly installed
    if [[ $(uname -m) == "x86_64" ]]; then \
      cd /usr/share && \
      curl -L https://github.com/Overbryd/docker-phantomjs-alpine/releases/download/2.11/phantomjs-alpine-x86_64.tar.bz2 | tar xj && \
      ln -s /usr/share/phantomjs/phantomjs /usr/bin/phantomjs && \
      echo "Phantom JS version:" && \
      phantomjs --version && \
      cd -; \
    fi && \
    # Install ytdl-sub, ensure it is installed properly
    pip install --no-cache-dir ytdl_sub-*.whl && \
      ytdl-sub -h && \
    # Delete unneeded packages after install
    rm ytdl_sub-*.whl && \
    apk del \
      g++ \
      make \
      py3-setuptools && \
    if [[ $(uname -m) == "x86_64" ]]; then curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip && unzip rclone-current-linux-amd64.zip && \
    cd rclone-*-linux-amd64 && \
    cp rclone /usr/bin/ && chown root:root /usr/bin/rclone && chmod 755 /usr/bin/rclone && \
    cd .. && rm rclone-* -rf && \
    wget https://github.com/donwa/gclone/releases/download/v1.51.0-mod1.3.1/gclone_1.51.0-mod1.3.1_Linux_x86_64.gz -O gclone.gz && \
    gzip -d -c gclone.gz > /usr/bin/gclone && \
    rm gclone.gz && \
    chmod 0755 /usr/bin/gclone; \ 
    elif [[ $(uname -m) == "aarch64" ]]; then curl -O https://downloads.rclone.org/rclone-current-linux-arm64.zip && unzip rclone-current-linux-arm64.zip && \
    cd rclone-*-linux-arm64 && \
    cp rclone /usr/bin/ && chown root:root /usr/bin/rclone && chmod 755 /usr/bin/rclone && \
    cd .. && rm rclone-* -rf && \
    wget https://github.com/donwa/gclone/releases/download/v1.51.0-mod1.3.1/gclone_1.51.0-mod1.3.1_Linux_arm64.gz -O gclone.gz && \
    gzip -d -c gclone.gz > /usr/bin/gclone && \
    rm gclone.gz && \
    chmod 0755 /usr/bin/gclone; fi

###############################################################################
# CONTAINER CONFIGS

ENV EDITOR="nano" \
HOME="/config"

VOLUME /config
