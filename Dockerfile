# Glama MCP release image for fcop-mcp (stdio).
# See docs/glama-directory.md for claim / deploy / release steps.

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        "fcop>=3.2.4,<3.3" \
        "fcop-mcp>=3.2.4,<3.3"

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import fcop_mcp; import fcop; print('ok')" || exit 1

ENTRYPOINT ["fcop-mcp"]
