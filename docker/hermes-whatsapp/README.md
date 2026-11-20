# Imagem Hermes com Patch Reproduzível do Bridge WhatsApp

Esta imagem opcional parte de `nousresearch/hermes-agent:v0.23.3` fixada por digest e aplica `patch_whatsapp_bridge.py` em tempo de build, substituindo os antigos binds manuais em runtime e proxies CONNECT externos.

Como no novo desenho o namespace `spoke-hermes` possui saída HTTPS `443` direta via `NetworkPolicy` (bloqueando apenas IPs privados RFC1918/CGNAT não autorizados), o próprio bridge consulta `https://web.whatsapp.com/sw.js` diretamente sem intermediários.

```bash
docker build -t homeserver-hermes:v0.23.3-wa1 docker/hermes-whatsapp
```
