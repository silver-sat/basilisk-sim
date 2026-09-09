FROM mcr.microsoft.com/devcontainers/python:3.12

RUN pip install --no-cache-dir "bsk[all,examples]" jupyter matplotlib \
 && bskLargeData

RUN BSK_VERSION="$(python -c 'import importlib.metadata as m; print(m.version("bsk"))')" \
 && git clone -q --depth 1 --filter=blob:none --sparse \
      --branch "v${BSK_VERSION}" https://github.com/AVSLab/basilisk.git /tmp/bsksrc \
 && git -C /tmp/bsksrc sparse-checkout set examples \
 && mv /tmp/bsksrc/examples /opt/examples \
 && rm -rf /tmp/bsksrc \
 && test "$(ls /opt/examples/*.py | wc -l)" -gt 50 \
 && chmod -R a+rX /opt/examples

ENV BSK_EXAMPLES=/opt/examples
