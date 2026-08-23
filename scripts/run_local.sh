#!/bin/bash
# 本地起音调训练器（给 preview_start / 手动调试用）。
# 固定 ADMIN_CODE，否则 server.py 每次重启都会随机生成一个新的管理员口令。
cd "$(dirname "$0")/.." || exit 1
export PORT="${PORT:-8765}"
export ADMIN_CODE="${ADMIN_CODE:-localdev}"
exec python3 server.py
