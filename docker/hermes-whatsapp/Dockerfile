FROM nousresearch/hermes-agent:v0.23.2@sha256:d6746a084e9341baada483e3d6210444d3c1aeb7c130f0915150065fb2851459

COPY patch_whatsapp_bridge.py /tmp/patch_whatsapp_bridge.py

# Aplica o patch versionado que consulta dinamicamente a client_revision atual
# do WhatsApp Web em sw.js, evitando erro 405 sem precisar de proxy intermediario.
RUN set -eu; \
    BRIDGE="/opt/hermes/scripts/whatsapp-bridge/bridge.js"; \
    if [ -f "$BRIDGE" ]; then \
      python3 /tmp/patch_whatsapp_bridge.py --source "$BRIDGE" --output "${BRIDGE}.patched"; \
      mv "${BRIDGE}.patched" "$BRIDGE"; \
    fi; \
    rm -f /tmp/patch_whatsapp_bridge.py
