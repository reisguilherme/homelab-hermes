"""Prepare the pinned bridge's explicit native HTTPS proxy agent, offline only."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

SOURCE_SHA256 = "35933c7bab7efddb996ab13c1e8afb70c6ad40595f0d704a1ed1d6afce8d79c5"
IMPORT = "import { randomBytes, createHash } from 'crypto';"
LOGGER = "const logger = pino({ level: 'warn' });"
SOCKET = "  sock = makeWASocket({\n"
VERSION_ANCHOR = "const getWAVersion = createVersionResolver(fetchLatestBaileysVersion);"
VERSION = r"""const getWAVersion = createVersionResolver(() => new Promise((resolve, reject) => {
  // The pinned Baileys default can be rejected as client_too_old (405).
  // Use native HTTPS through the same agent; do not expand the egress allowlist.
  const fail = () => reject(new Error('wa_version_unavailable'));
  try {
    const request = httpsGet('https://web.whatsapp.com/sw.js', {
      agent: whatsappProxyAgent,
      signal: AbortSignal.timeout(10000),
      rejectUnauthorized: true,
      headers: {
        'sec-fetch-site': 'none',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
          + '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      },
    }, response => {
      response.on('error', fail);
      response.on('aborted', fail);
      if (response.statusCode !== 200) {
        response.destroy();
        fail();
        return;
      }
      const chunks = [];
      let bytes = 0;
      response.on('data', chunk => {
        bytes += chunk.length;
        if (bytes > 1024 * 1024) {
          response.destroy();
          fail();
          return;
        }
        chunks.push(chunk);
      });
      response.on('end', () => {
        const match = Buffer.concat(chunks).toString('utf8')
          .match(/\\?"client_revision\\?":\s*(\d+)(?=[,\s}])/);
        const revision = match ? Number(match[1]) : NaN;
        if (!Number.isSafeInteger(revision) || revision <= 0) {
          fail();
          return;
        }
        resolve({ version: [2, 3000, revision] });
      });
    });
    request.on('error', fail);
  } catch {
    fail();
  }
}));"""
AGENT = """// ws supplies createConnection, so an undefined agent bypasses Node's global
// environment proxy. Pass a native agent explicitly; TLS remains end to end.
const whatsappProxyAgent = (process.env.HTTPS_PROXY || process.env.https_proxy)
  ? new HttpsAgent({ proxyEnv: process.env })
  : undefined;

"""


def patched(source: bytes) -> bytes:
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise ValueError("bridge_source_pin_mismatch")
    text = source.decode("utf-8")
    for anchor in (IMPORT, LOGGER, SOCKET, VERSION_ANCHOR):
        if text.count(anchor) != 1:
            raise ValueError("bridge_patch_anchor_mismatch")
    text = text.replace(
        IMPORT, IMPORT + "\nimport { Agent as HttpsAgent, get as httpsGet } from 'node:https';", 1
    )
    text = text.replace(LOGGER, AGENT + LOGGER, 1)
    settings = (
        "    ...(whatsappProxyAgent ? { agent: whatsappProxyAgent, "
        "fetchAgent: whatsappProxyAgent } : {}),\n"
    )
    text = text.replace(SOCKET, SOCKET + settings, 1)
    text = text.replace(
        "fetchLatestBaileysVersion, downloadMediaMessage",
        "downloadMediaMessage", 1,
    )
    text = text.replace(VERSION_ANCHOR, VERSION, 1)
    return text.encode("utf-8")


def prepare(source: Path, output: Path) -> str:
    result = patched(source.read_bytes())
    with output.open("xb") as stream:
        stream.write(result)
    return hashlib.sha256(result).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print("patched_bridge_sha256=" + prepare(args.source, args.output))


if __name__ == "__main__":
    main()
