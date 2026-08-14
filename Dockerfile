FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

LABEL org.opencontainers.image.title="ORION Runtime"
LABEL org.opencontainers.image.version="1.1.0"
LABEL org.opencontainers.image.revision="d34fbb2f99334534f4db89465a29f8bdb16d14d3"
LABEL org.opencontainers.image.description="Versioned deterministic Orientation Runtime"

RUN groupadd --system orion \
    && useradd --system --gid orion --home-dir /nonexistent --shell /usr/sbin/nologin orion \
    && touch --reference=/etc/passwd- /etc/passwd \
    && touch --reference=/etc/group- /etc/group \
    && touch --reference=/etc/shadow- /etc/shadow \
    && touch --reference=/etc/gshadow- /etc/gshadow

WORKDIR /app

COPY .dockerignore Dockerfile ./
COPY VERSION workspace.yaml pyproject.toml ./
COPY deploy ./deploy
COPY evaluation/phase_vii/corpus.json ./evaluation/phase_vii/corpus.json
COPY docs/architecture/contracts ./docs/architecture/contracts
COPY docs/architecture/operators ./docs/architecture/operators
COPY docs/architecture/runtime ./docs/architecture/runtime
COPY release ./release
COPY src ./src

ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ORION_BIND_HOST=0.0.0.0
ENV ORION_PORT=8080

USER orion:orion

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
  CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2).read()"]

CMD ["python3", "-m", "orion_runtime"]
