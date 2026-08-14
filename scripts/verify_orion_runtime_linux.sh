#!/bin/sh
set -eu

if [ "$(uname -s)" != "Linux" ]; then
  echo "FAIL: supported deployment verification requires Linux" >&2
  exit 2
fi
command -v docker >/dev/null 2>&1 || {
  echo "FAIL: docker is required" >&2
  exit 2
}
docker buildx version >/dev/null 2>&1 || {
  echo "FAIL: docker buildx is required for reproducible image export" >&2
  exit 2
}

image_a="orion-runtime:verification-a"
image_b="orion-runtime:verification-b"
container="orion-runtime-verification"
port="${ORION_VERIFY_PORT:-18080}"
secret="${ORION_VERIFY_SECRET:-runtime-verification-secret}"
builder="${ORION_VERIFY_BUILDER:-orion-runtime-repro}"
source_date_epoch="${ORION_SOURCE_DATE_EPOCH:-1784905790}"
export_dir="$(mktemp -d)"

cleanup() {
  docker rm -f "$container" >/dev/null 2>&1 || true
  rm -rf "$export_dir"
}
trap cleanup EXIT INT TERM

if ! docker buildx inspect "$builder" >/dev/null 2>&1; then
  docker buildx create --driver docker-container --name "$builder" >/dev/null
fi
docker buildx inspect "$builder" --bootstrap >/dev/null

build_reproducible_image() {
  image="$1"
  archive="$2"
  docker buildx build \
    --builder "$builder" \
    --no-cache \
    --pull=false \
    --build-arg "SOURCE_DATE_EPOCH=$source_date_epoch" \
    --output "type=oci,name=$image,dest=$archive,rewrite-timestamp=true" \
    .
  docker load -i "$archive" >/dev/null
}

wait_until_ready() {
  target_port="$1"
  for _attempt in $(seq 1 60); do
    if python3 - "$target_port" <<'PY'
import sys
import urllib.error
import urllib.request

try:
    with urllib.request.urlopen(
        f"http://127.0.0.1:{sys.argv[1]}/health",
        timeout=1,
    ) as response:
        if response.status == 200:
            raise SystemExit(0)
except (OSError, urllib.error.URLError):
    pass
raise SystemExit(1)
PY
    then
      return 0
    fi
    sleep 1
  done
  return 1
}

build_reproducible_image "$image_a" "$export_dir/image-a.tar"
build_reproducible_image "$image_b" "$export_dir/image-b.tar"

layers_a="$(docker image inspect "$image_a" --format '{{json .RootFS.Layers}}')"
layers_b="$(docker image inspect "$image_b" --format '{{json .RootFS.Layers}}')"
[ "$layers_a" = "$layers_b" ] || {
  echo "FAIL: independently built image root filesystems differ" >&2
  exit 1
}

docker run --rm "$image_a" python3 -c '
from orion_runtime.isolation import install_worker_network_isolation, assert_network_isolated
install_worker_network_isolation()
assert_network_isolated()
'

docker run -d --name "$container" \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=128m \
  --memory 1536m \
  --pids-limit 32 \
  --ulimit nofile=64:64 \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  -e "ORION_SERVICE_CREDENTIALS_JSON={\"verification\":\"$secret\"}" \
  -p "127.0.0.1:$port:8080" \
  "$image_a" >/dev/null

[ "$(docker inspect "$container" --format '{{.Config.User}}')" = "orion:orion" ]
[ "$(docker inspect "$container" --format '{{.HostConfig.ReadonlyRootfs}}')" = "true" ]

wait_until_ready "$port" || {
  docker logs "$container" >&2
  echo "FAIL: readiness did not become healthy" >&2
  exit 1
}

PYTHONPATH=src python3 - "$port" "$secret" <<'PY'
import sys
import urllib.request
from orion_runtime.canonical import canonical_bytes, parse_json_bytes
from orion_runtime.constants import API_VERSION, MEDIA_TYPE
from orion_runtime.fixtures import canary_envelope

body = canonical_bytes(canary_envelope())
request = urllib.request.Request(
    f"http://127.0.0.1:{sys.argv[1]}/orientation/v1/requests",
    data=body,
    method="POST",
    headers={
        "Authorization": f"Bearer {sys.argv[2]}",
        "Content-Type": MEDIA_TYPE,
        "Accept": MEDIA_TYPE,
        "ORION-API-Version": API_VERSION,
    },
)
with urllib.request.urlopen(request, timeout=30) as response:
    result = parse_json_bytes(response.read())
    assert response.status == 200
    assert result["terminal_stop"] == "at_slice_iv_certified"
    assert result["artifact_manifest"]["artifact_count"] == 22
PY

docker restart "$container" >/dev/null
wait_until_ready "$port" || {
  docker logs "$container" >&2
  echo "FAIL: readiness did not recover after restart" >&2
  exit 1
}

echo "PASS: Linux image, immutable build layers, non-root/read-only service,"
echo "worker syscall isolation, resource configuration, authenticated execution,"
echo "readiness, and restart"
