FROM nousresearch/hermes-agent:v0.23.3@sha256:3e9fe4c6ef36490f43aa0d0d80f9df64e9c92a576eee3042f1a97c8813c05355

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
