---
name: media-management
description: Fluxo conversacional para consultar catálogo/fila, adicionar filmes ou séries, escolher releases, gerenciar legendas e confirmar exclusões com segurança via arr-mcp.
version: 2.0.0
---

# Operação de Mídia via `arr-mcp`

## 1. Consultas e Diagnóstico
- Use `get_stack_health` e `diagnose_media` para investigar problemas ou conferir status dos serviços.
- Para listar torrents no qBittorrent, use `get_queue` com `detail: full` sem restringir `kind` a apenas Arr; sempre respeite a paginação (`offset` e `total`) antes de resumir totais.
- Consulte `search_media`, `get_library`, `get_requests`, `get_subtitles`, `get_calendar` e `get_history` diretamente quando solicitado.

## 2. Pedidos, Releases e Downloads (Confirmação Fluida na Conversa)
1. Identifique título, ano e se já existe no Jellyfin ou no Radarr/Sonarr (`search_media`, `get_library`).
2. Ao buscar releases (`get_releases`), destaque título, tamanho, seeds, resolução e indícios de idioma de áudio/legenda (informando quando o idioma vem apenas do nome do release).
3. Para ações de escrita do `arr-mcp` (`add_media`, `request_media`, `grab_release`, `respond_to_request`, `trigger_search`), execute primeiro a chamada sem `confirm` (gerando o preview e o token de confirmação do servidor) **ou** apresente os parâmetros selecionados em linguagem natural e aguarde o "ok" de Guilherme antes de enviar a confirmação final.
4. Nunca declare mídia disponível para assistir sem antes consultar `get_library` / Jellyfin e confirmar a presença do item.

## 3. Exclusões de Mídia (`delete_media` / `delete_episode_files`)
1. Sempre liste explicitamente qual filme, temporada ou episódios serão removidos e se isso apaga arquivos do disco.
2. Nunca envie o `confirm` destrutivo sem uma confirmação explícita e específica de Guilherme na conversa referente àquele alvo.
