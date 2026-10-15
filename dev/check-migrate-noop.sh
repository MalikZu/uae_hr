#!/usr/bin/env bash
# Migrate twice and prove the second run changed nothing uae_hr owns.
#   SITE=test_site dev/check-migrate-noop.sh
set -euo pipefail
SITE="${SITE:-test_site}"
PROJECT="${PROJECT:-fa}"
C="$PROJECT-backend-1"
BENCH=/home/frappe/frappe-bench
run() { docker exec "$C" bash -lc "cd $BENCH && $*"; }
run "bench --site $SITE migrate --skip-search-index" >/dev/null
a=$(run "bench --site $SITE execute uae_hr.setup.snapshot.fingerprint" | tail -1)
run "bench --site $SITE migrate --skip-search-index" >/dev/null
b=$(run "bench --site $SITE execute uae_hr.setup.snapshot.fingerprint" | tail -1)
echo "after migrate 1: $a"
echo "after migrate 2: $b"
[[ "${a%% *}" == "${b%% *}" ]] && echo "OK: second migrate is a no-op" || { echo "FAIL: second migrate changed something"; exit 1; }
