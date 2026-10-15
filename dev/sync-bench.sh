#!/usr/bin/env bash
# Copy this app (uae_hr) into every Python container of a local frappe_docker stack (compose project
# $PROJECT, default "fa")
# (backend + 3 workers each have their OWN app tree), then migrate the dev site.
#
#   dev/sync-bench.sh            # sync + migrate test_site
#   dev/sync-bench.sh --install  # first time: pip install -e, add to apps.txt, install-app
#   dev/sync-bench.sh --no-migrate
#
# Lost on `docker compose -p $PROJECT down` (containers are recreated from the image); rerun --install.
set -euo pipefail
APP=uae_hr
SRC="$(cd "$(dirname "$0")/.." && pwd)"
SITE="${SITE:-test_site}"
BENCH=/home/frappe/frappe-bench
PROJECT="${PROJECT:-fa}"
CONTAINERS=("$PROJECT-backend-1" "$PROJECT-queue-short-1" "$PROJECT-queue-long-1" "$PROJECT-scheduler-1")
MODE="${1:-}"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
# tracked tree if git, else everything minus caches; COPYFILE_DISABLE stops macOS ._ files
export COPYFILE_DISABLE=1
if git -C "$SRC" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # tracked + untracked, minus paths deleted on disk but still in the index
  (cd "$SRC" && git ls-files -z --cached --others --exclude-standard | while IFS= read -r -d "" f; do [ -e "$f" ] && printf "%s\0" "$f"; done | tar --null --no-xattrs --no-mac-metadata -T - -cf "$TMP/app.tar")
else
  (cd "$SRC" && tar --no-xattrs --no-mac-metadata --exclude="__pycache__" --exclude="*.pyc" --exclude=".git" -cf "$TMP/app.tar" .)
fi

for c in "${CONTAINERS[@]}"; do
  docker exec -u root "$c" bash -c "rm -rf $BENCH/apps/$APP && mkdir -p $BENCH/apps/$APP"
  docker cp "$TMP/app.tar" "$c:/tmp/$APP.tar"
  docker exec -u root "$c" bash -c "tar -xf /tmp/$APP.tar -C $BENCH/apps/$APP && rm /tmp/$APP.tar && chown -R frappe:frappe $BENCH/apps/$APP"
  if [[ "$MODE" == "--install" ]]; then
    docker exec "$c" bash -lc "cd $BENCH && env/bin/pip install -q -e apps/$APP && { grep -qx $APP sites/apps.txt || echo $APP >> sites/apps.txt; }"
  fi
  echo "synced -> $c"
done

if [[ "$MODE" == "--install" ]]; then
  docker exec "$PROJECT-backend-1" bash -lc "cd $BENCH && bench --site $SITE install-app $APP"
elif [[ "$MODE" != "--no-migrate" ]]; then
  docker exec "$PROJECT-backend-1" bash -lc "cd $BENCH && bench --site $SITE migrate --skip-search-index"
fi
docker exec "$PROJECT-backend-1" bash -lc "cd $BENCH && bench --site $SITE clear-cache" >/dev/null
docker restart "${CONTAINERS[@]}" >/dev/null
echo "done: $APP on $SITE"
