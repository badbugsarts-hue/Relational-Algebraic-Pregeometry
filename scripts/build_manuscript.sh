#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/build_manuscript.sh [--source REPO_RELATIVE_TEX] --output OUTPUT_DIR

Compiles a TeX source inside the immutable PROV-002 linux/amd64 image.
The canonical manuscript source is verified against both its SHA-256 and Git blob ID.
Build output must be outside verification/data/pregeometry/.
EOF
}

repo_root="$(git rev-parse --show-toplevel)"
environment_lock="${repo_root}/environment/texlive.lock.json"
source_lock="${repo_root}/environment/manuscript-source.lock.json"
source_rel=""
output_dir=""

if command -v python3 >/dev/null 2>&1; then
  python_cmd="python3"
elif command -v python >/dev/null 2>&1; then
  python_cmd="python"
else
  printf '%s\n' 'Python 3 is required to read and emit PROV-002 records.' >&2
  exit 69
fi

while (($#)); do
  case "$1" in
    --source)
      source_rel="${2:?missing value for --source}"
      shift 2
      ;;
    --output)
      output_dir="${2:?missing value for --output}"
      shift 2
      ;;
    --environment-lock)
      environment_lock="${2:?missing value for --environment-lock}"
      shift 2
      ;;
    --source-lock)
      source_lock="${2:?missing value for --source-lock}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 64
      ;;
  esac
done

if [[ -z "${output_dir}" ]]; then
  printf '%s\n' '--output is required' >&2
  exit 64
fi

if [[ ! -f "${environment_lock}" ]]; then
  printf 'Environment lock does not exist: %s\n' "${environment_lock}" >&2
  exit 66
fi
if [[ ! -f "${source_lock}" ]]; then
  printf 'Source lock does not exist: %s\n' "${source_lock}" >&2
  exit 66
fi

read_lock() {
  "${python_cmd}" - "$1" "$2" <<'PY'
import json
import sys

value = json.load(open(sys.argv[1], encoding="utf-8"))
for part in sys.argv[2].split("."):
    value = value[part]
print(value)
PY
}

canonical_source="$(read_lock "${source_lock}" path)"
if [[ -z "${source_rel}" ]]; then
  source_rel="${canonical_source}"
fi

case "${source_rel}" in
  /*|*..*|*\\*|*$'\n'*|*$'\r'*)
    printf 'Source must be a normalized repository-relative path: %s\n' "${source_rel}" >&2
    exit 64
    ;;
esac

source_abs="${repo_root}/${source_rel}"
if [[ ! -f "${source_abs}" ]]; then
  printf 'Source does not exist: %s\n' "${source_abs}" >&2
  exit 66
fi

mkdir -p "${output_dir}"
output_abs="$(cd "${output_dir}" && pwd -P)"
forbidden_abs="$(cd "${repo_root}/verification/data/pregeometry" && pwd -P)"
case "${output_abs}/" in
  "${forbidden_abs}/"*)
    printf 'Build outputs are forbidden under %s\n' "${forbidden_abs}" >&2
    exit 73
    ;;
esac

if [[ "${source_rel}" == "${canonical_source}" ]]; then
  expected_blob_sha256="$(read_lock "${source_lock}" git_blob_sha256)"
  expected_blob="$(read_lock "${source_lock}" git_blob_sha1)"
  actual_blob="$(git -C "${repo_root}" hash-object -- "${source_rel}")"
  actual_blob_sha256="$(
    git -C "${repo_root}" cat-file blob "${actual_blob}" | sha256sum | awk '{print $1}'
  )"
  if [[ "${actual_blob_sha256}" != "${expected_blob_sha256}" || "${actual_blob}" != "${expected_blob}" ]]; then
    printf 'Canonical source lock mismatch: blob_sha256=%s blob=%s\n' \
      "${actual_blob_sha256}" "${actual_blob}" >&2
    exit 65
  fi
else
  actual_blob="$(git -C "${repo_root}" hash-object -- "${source_rel}")"
  actual_blob_sha256="$(
    git -C "${repo_root}" cat-file blob "${actual_blob}" | sha256sum | awk '{print $1}'
  )"
fi

image_ref="$(read_lock "${environment_lock}" image_reference)"
platform_manifest="$(read_lock "${environment_lock}" platform_manifest_digest)"
locked_arch="$(read_lock "${environment_lock}" architecture)"
locked_os="$(read_lock "${environment_lock}" os)"
if [[ "${locked_arch}" != "amd64" || "${locked_os}" != "linux" ]]; then
  printf 'Unsupported lock platform: %s/%s\n' "${locked_os}" "${locked_arch}" >&2
  exit 65
fi
if [[ ! "${platform_manifest}" =~ ^sha256:[0-9a-f]{64}$ ]]; then
  printf 'Malformed platform manifest digest: %s\n' "${platform_manifest}" >&2
  exit 65
fi
if [[ "${image_ref}" != *@${platform_manifest} ]]; then
  printf 'Image reference does not match the locked platform manifest.\n' >&2
  exit 65
fi

environment_lock_sha256="$(sha256sum "${environment_lock}" | awk '{print $1}')"
source_lock_sha256="$(sha256sum "${source_lock}" | awk '{print $1}')"

if ! command -v docker >/dev/null 2>&1; then
  printf '%s\n' '[BLOCKED] Docker is required for the pinned PROV-002 build.' >&2
  exit 69
fi

docker pull --platform linux/amd64 "${image_ref}" >"${output_abs}/docker-pull.log" 2>&1

set +e
docker run --rm \
  --platform linux/amd64 \
  --network none \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --mount "type=bind,src=${repo_root},dst=/repo,readonly" \
  --mount "type=bind,src=${output_abs},dst=/out" \
  --env "SOURCE_REL=${source_rel}" \
  --workdir /out \
  "${image_ref}" \
  sh -ceu '
    cp "/repo/${SOURCE_REL}" /out/input.tex
    pdftex --version | head -n 1 > /out/tex-engine.txt
    latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
      -jobname=artifact input.tex
  ' >"${output_abs}/build.log" 2>&1
build_exit=$?
set -e

"${python_cmd}" - \
  "${output_abs}" \
  "${source_rel}" \
  "${image_ref}" \
  "${build_exit}" \
  "${actual_blob}" \
  "${actual_blob_sha256}" \
  "${environment_lock_sha256}" \
  "${source_lock_sha256}" <<'PY'
import hashlib
import json
import pathlib
import re
import sys

out = pathlib.Path(sys.argv[1])
log = (out / "build.log").read_text(encoding="utf-8", errors="replace")
engine_file = out / "tex-engine.txt"
report = {
    "schema_version": 1,
    "status": "passed" if int(sys.argv[4]) == 0 else "failed",
    "environment_qualified": True,
    "source": sys.argv[2],
    "image_reference": sys.argv[3],
    "exit_code": int(sys.argv[4]),
    "source_git_blob_sha1": sys.argv[5],
    "source_git_blob_sha256": sys.argv[6],
    "environment_lock_sha256": sys.argv[7],
    "source_lock_sha256": sys.argv[8],
    "tex_engine": engine_file.read_text(encoding="utf-8").strip()
        if engine_file.exists() else None,
    "pages": max((int(v) for v in re.findall(r"Output written on .*?\\((\\d+) pages?", log)), default=None),
    "latex_warnings": len(re.findall(r"LaTeX Warning:", log)),
    "undefined_references": len(re.findall(r"undefined references?", log, flags=re.I)),
    "undefined_citations": len(re.findall(r"undefined citations?", log, flags=re.I)),
    "overfull_boxes": len(re.findall(r"Overfull \\\\[hv]box", log)),
}
for name in ("input.tex", "build.log", "artifact.pdf"):
    artifact = out / name
    report[f"{name}_sha256"] = (
        hashlib.sha256(artifact.read_bytes()).hexdigest()
        if artifact.exists()
        else None
    )
(out / "report.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
PY

exit "${build_exit}"
