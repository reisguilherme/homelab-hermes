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
2. Ao buscar releases (`get_releases`), destaque título, tamanho, seeds, resolução, indícios de idioma de áudio/legenda (informando quando o idioma vem apenas do nome do release) e verifique `customFormatScore` e `rejections`.
3. **Antes de baixar uma troca/substituição de mídia já existente:** prefira uma release sem rejeições de perfil/Custom Format que supere a pontuação do arquivo atual no Radarr/Sonarr. Se a release escolhida tiver score menor ou rejeição (`Not a Custom Format upgrade` / perfil sem upgrade), **avise Guilherme antes do `grab_release`** que o Radarr/Sonarr recusará a importação automática enquanto o arquivo atual existir.
4. Para ações de escrita do `arr-mcp` (`add_media`, `request_media`, `grab_release`, `respond_to_request`, `trigger_search`), execute primeiro a chamada sem `confirm` (gerando o preview e o token de confirmação do servidor) **ou** apresente os parâmetros selecionados em linguagem natural e aguarde o "ok" de Guilherme antes de enviar a confirmação final.
5. Se `import_download` falhar por pontuação de Custom Format menor em uma troca já baixada, informe o score atual vs. novo e ofereça a saída explícita (remover o arquivo antigo mediante confirmação dedicada ou ajustar o perfil antes de reimportar).
6. Nunca declare mídia disponível para assistir sem antes consultar `get_library` / Jellyfin e confirmar a presença do item.

## 3. Exclusões de Mídia (`delete_media` / `delete_episode_files`)
1. Sempre liste explicitamente qual filme, temporada ou episódios serão removidos e se isso apaga arquivos do disco.
2. Nunca envie o `confirm` destrutivo sem uma confirmação explícita e específica de Guilherme na conversa referente àquele alvo.
