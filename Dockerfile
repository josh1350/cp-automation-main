FROM --platform=linux/amd64 python:3.11.3-slim-buster AS base

ENV PATH "/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM base AS builder

RUN python -m venv /opt/venv
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base

ENV ALLURE_RELEASE 2.23.0
ENV ALLURE_REPO https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline
ENV ROOT_DIR /tests
ENV PATH "/opt/venv/bin:$PATH"
ENV DISPLAY :0
ENV JAVA_HOME "/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH $JAVA_HOME/bin:$PATH

RUN useradd agent
WORKDIR $ROOT_DIR
RUN chown -R agent:agent $ROOT_DIR

COPY --chown=agent:agent --from=builder /opt/venv /opt/venv

RUN apt-get update --yes --quiet \
    && apt-get install --yes --quiet --no-install-recommends \
    libxpm4 \
    libxrender1 \
    libgtk2.0-0 \
    libnss3 \
    libgconf-2-4 \
    xvfb \
    xfonts-cyrillic \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-base \
    xfonts-scalable \
    imagemagick \
    x11-apps \
    openjdk-11-jdk \
    curl \
    unzip \
    wget \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libxtst6 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    chromium \
    chromium-common \
    chromium-driver\
    libatomic1 \
    libc6 \
    libglib2.0-0 \
    libstdc++6 \
    libx11-6 \
    libxnvctrl0 \
    x11-utils \
    zlib1g \
    fonts-noto-color-emoji

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.bashrc

RUN curl -o allure-commandline-${ALLURE_RELEASE}.zip -Ls ${ALLURE_REPO}/${ALLURE_RELEASE}/allure-commandline-${ALLURE_RELEASE}.zip && \
    unzip -q allure-commandline-${ALLURE_RELEASE}.zip -d /opt/ && ln -s /opt/allure-${ALLURE_RELEASE}/bin/allure /usr/bin/allure && allure --version
RUN rm allure-commandline-${ALLURE_RELEASE}.zip
#
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#    dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
#RUN rm google-chrome-stable_current_amd64.deb
#
#RUN wget -O chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
#    unzip chromedriver.zip chromedriver -d /usr/local/bin/
#RUN rm chromedriver.zip


RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --chown=agent:agent . .

USER agent

RUN set -xe; python setup.py install

# Run virtual frame buffer
RUN Xvfb -ac -listen tcp :1 -screen 0 1920x1080x24 -ac -nolisten unix &> xvfb.log &
ENV DISPLAY :0.0