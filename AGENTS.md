# homelab-hermes — Guia do Agente de Engenharia (Spoke 2)

> [!IMPORTANT]
> Este `AGENTS.md` destina-se **exclusivamente a agentes de engenharia de software** que mantêm este repositório. As instruções conversacionais de runtime do próprio bot Hermes ficam isoladas em `profile/AGENT_INSTRUCTIONS.md` (montadas como `AGENTS.md` apenas dentro do container).

## Papel Arquitetural

Este repositório define o **Spoke de Assistente Pessoal Multi-Spoke (`spoke-hermes`)** rodando no cluster **K3s (`VM 200`)** via FluxCD:
- Consome múltiplos Spokes exclusivamente via **endpoints MCP internos** (`ClusterIP` + `NetworkPolicy`):
  - `media`: `http://arr-mcp.spoke-mediaserver.svc.cluster.local:6060/mcp`
  - `observability`: `http://prometheus-mcp.platform-observability.svc.cluster.local:8080/mcp`
- Expõe a Web UI em `:9119` (`hermes.greis.dev.br`) e o `api_server` interno em ClusterIP `:8642` consumido exclusivamente pelo `spoke-dashboard` (`API_SERVER_KEY` via `secrets/hermes-api.sops.yaml` e `NetworkPolicy` restrita).
- Conecta-se diretamente via HTTPS `443` à OpenAI API (`gpt-6.2-sol` como modelo primário) e WhatsApp Web (conforme `kubernetes/network-policy.yaml`), sem proxies MITM no Hub.

## Regras do Repositório

1. **Proibido adicionar SSH, Docker socket ou exec root no agente:** Toda ação em outros Spokes ocorre exclusivamente via contratos MCP declarados em `profile/hermes.yaml` e liberados via `NetworkPolicy` no respectivo Spoke.
2. **Configuração unificada:** Não reintroduzir múltiplas pilhas de overlays Docker Compose nem plugins de bloqueio acoplados ao runtime interno de terceiros.
3. **Como plugar um novo Spoke no Hermes:**
   - Adicione a entrada em `mcp_servers:` dentro de `profile/hermes.yaml` e o toolset em `platform_toolsets.{cli,whatsapp,api_server}`.
   - Libere o tráfego de saída correspondente em `kubernetes/network-policy.yaml` (e o ingresso no Spoke destino).
   - Documente o fluxo em `profile/skills/<dominio>/SKILL.md`.
4. **Higiene e segredos:** Segredos (`OPENAI_API_KEY`, tokens MCP, `API_SERVER_KEY`) ficam apenas em `secrets/*.sops.yaml`. Nunca criar `.artifacts/`, `.runtime/`, `.worktrees/` ou `backup/`.

## Validação Local

```bash
node scripts/validate.mjs
```
