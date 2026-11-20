# homelab-hermes (Spoke 2)

Assistente pessoal multi-spoke do **HomeServer** baseado em **Hermes Agent v0.23.3** (Web UI + WhatsApp + API interna `:8642`), implantado no namespace `spoke-hermes` via **K3s + FluxCD + SOPS/Age**.

## Integrações MCP Configuradas

| Servidor MCP | Namespace Destino | Finalidade |
|---|---|---|
| `media` (`arr-mcp`) | `spoke-mediaserver` | Consultas, pedidos, downloads, legendas, fila qBit e gerenciamento de mídia com preview/confirmação. |
| `observability` (`prometheus-mcp`) | `platform-observability` | Consulta somente leitura de saúde dos nós, uso de disco/RAM e alertas ativos no Prometheus do Hub. |

## Estrutura

- `profile/`: Identidade (`SOUL.md`), instruções de runtime do assistente (`AGENT_INSTRUCTIONS.md`), configuração única (`hermes.yaml`), skills (`skills/`) e plugin `advanced-delegation`.
- `docker/hermes-whatsapp/`: Imagem opcional construída sobre `nousresearch/hermes-agent:v0.23.3` aplicando o fix reproduzível de versão do WhatsApp Web (`patch_whatsapp_bridge.py`).
- `kubernetes/`: Manifestos declarativos (`Namespace`, `ResourceQuota`, `PVC`, `ConfigMap` gerado, `Deployment`, `Service`, `Ingress`, `NetworkPolicy`).
- `secrets/`: Template `hermes-secrets.example.yaml` para criptografia SOPS/Age.

## Validação Local

```bash
node scripts/validate.mjs
```
