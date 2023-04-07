FROM debian:bullseye
LABEL maintainer="Anonymous"
LABEL org.opencontainers.image.authors="Anonymous"
LABEL description="A dockerfile that allows to run the FSynth experiments"
LABEL version="1.0"
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8 TERM='xterm-256color'
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get --yes --no-install-recommends update && \
    apt-get --yes --no-install-recommends upgrade && \
    apt-get --yes --no-install-recommends install locales software-properties-common gpg-agent build-essential

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen en_US.UTF-8 && dpkg-reconfigure locales

RUN apt-get --yes --no-install-recommends update && \
    apt-get --yes --no-install-recommends install openjdk-17-jdk git python3 python3-pip python3-setuptools python3-wheel pkg-config curl unzip && \
    apt-get --purge remove -y .\*-doc$ && \
    apt-get clean

WORKDIR /home

ENV PYTHONPATH "$PYTHONPATH:."

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Install custom Gradle
RUN cd /tmp && \
    curl -O https://downloads.gradle-dn.com/distributions/gradle-7.3.3-bin.zip && \
    unzip gradle-7.3.3-bin.zip && \
    mkdir -p /opt/gradle && \
    cp -pvr gradle-7.3.3/* /opt/gradle && \
    rm -vrf gradle-7.3.3 gradle-7.3.3-bin.zip

ADD project /home/project

WORKDIR /home/project

ENV PATH "/opt/gradle/bin:${PATH}"

# Build Project
RUN mv -v /home/project/bin/testfiles / && \
    rm -vrf /home/project/bin && \
    ls -A && \
    gradle --version && \
    gradle wrapper && \
    ./gradlew deployJar

RUN printf "#!/bin/bash\n\njava -jar /home/project/bin/fsynth.jar \$@\n" > /usr/bin/fsynth && \
    chmod +x /usr/bin/fsynth && \
    mkdir -p /home/repairer

# Clean up build dependencies \
RUN apt-get --purge remove -y curl unzip

RUN java --version && fsynth --help

#RUN mv -v /home/project/bin/testfiles /

VOLUME /home/repairer

WORKDIR /home/repairer

ENTRYPOINT bash
