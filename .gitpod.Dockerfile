FROM gitpod/workspace-full

USER gitpod

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt