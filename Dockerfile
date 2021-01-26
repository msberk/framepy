FROM python:3.9-slim

RUN apt-get update\
    &&\
    apt-get install -y\
    curl\
    exiftran\
    fbi\
    imagemagick\
    git\
    && git clone https://github.com/andreafabrizi/Dropbox-Uploader.git /dropbox-uploader\
    && git -C /dropbox-uploader checkout 5f88da81b84cb0a7d6ae3cd06e86c352367a5df2\
    && chmod +x /dropbox-uploader/dropbox_uploader.sh\
    && cp /dropbox-uploader/dropbox_uploader.sh /usr/bin\
    && rm -rf /dropbox-uploader\
    && apt-get remove git -y\
    && apt-get autoremove -y\
    && rm -rf /var/lib/apt/lists/*\
    && ln -s /usr/local/bin/python /usr/bin/python3
