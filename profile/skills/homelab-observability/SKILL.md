---
name: homelab-observability
description: Consultar métricas do Proxmox, nós K3s, uso de espaço em disco (/mnt/storage, /mnt/transcode), RAM e alertas ativos via MCP de observabilidade.
version: 1.0.0
---

# Observabilidade do HomeServer via `prometheus-mcp`

Use as ferramentas do servidor MCP `observability` (somente leitura) para responder perguntas sobre a infraestrutura:

1. **Saúde dos nós e serviços:** Verifique `up{job="nodes"}` (`172.28.64.100:9100` = `homelab-hub`, `172.28.64.200:9100` = `homelab-k3s`) e `ALERTS{alertstate="firing"}`.
2. **Espaço no HD de 18 TB e no disco de transcode:** Consulte `node_filesystem_avail_bytes{mountpoint=~"/|/mnt/storage|/mnt/transcode"}` e `node_filesystem_size_bytes`.
3. **Pressão de memória:** Consulte `node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes` e o uso por namespace/pod via métricas do `kube-state-metrics`.

Apresente os números em **GB/TB e percentuais** de forma simples e direta para o usuário.
