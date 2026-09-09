FROM mcr.microsoft.com/devcontainers/python:3.12
RUN pip install --no-cache-dir "bsk[all,examples]" jupyter matplotlib \
 && bskLargeData
ENV MPLBACKEND=Agg
WORKDIR /opt
RUN bskExamples && chmod -R a+rX /opt/examples
ENV BSK_EXAMPLES=/opt/examples
