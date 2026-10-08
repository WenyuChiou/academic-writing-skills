# Portable workspace adapter

`adapter.json` exposes the existing academic writing and paper review skills to
an explicitly configured local workspace consumer. Adapter version `1.0.0`
uses manifest schema `1`, plugin skill version `1.3.7`, and manuscript state
schema `1.1`. It needs no private checkout, host-specific path, network service,
or installed project overlay. No scientific rule or audit script is replaced.

The writing skill may propose manuscript changes. The paper review skill is
review-only. These modes describe authority boundaries; installing or verifying
a bundle does not authorize editing a manuscript or running its scripts.
Project overlays remain optional, explicitly supplied project inputs.

## Verify and package

With Python 3.10 or newer, from the repository or an extracted bundle root:

```sh
python scripts/build_adapter_bundle.py --check
python scripts/build_adapter_bundle.py --output ../academic-writing-adapter.zip
python scripts/build_adapter_bundle.py --root /path/to/extracted-bundle --check
```

`--check` is read-only and prints JSON with the manifest hash and verified file
count. `--output` verifies first, then creates a new archive. Its parent directory
must exist; an existing destination is never overwritten. `--check` and
`--output` are mutually exclusive. Exit code `0` means verification succeeded;
`2` means verification, path validation, or archive creation failed.

Archives contain only the declared public files and `adapter.json`, in sorted
order, with a fixed timestamp and regular-file permissions. ZIP storage is
uncompressed to avoid compression-library differences. Identical source bytes
produce identical archive bytes regardless of source timestamps and permissions.
The helper packages the same bytes that it hashed during verification.

## Manifest contract

`files` maps each repository-relative slash path to its lowercase SHA256 digest.
It includes the plugin metadata, license, this guide, build helper, and both
skills' complete `SKILL.md`, `scripts`, `references`, `assets`, and `agents`
trees, including nested reference material and binary example figures. Bytecode
and tool caches are excluded. The manifest itself is included in
the archive and identified by the verifier's `manifest_sha256`; it cannot contain
its own digest. Hashes cover exact bytes, including line endings.

`skills` lists each skill's `id`, `path`, and `mode`. `entrypoints.state_template`
names the existing state template; `entrypoints.initialize_state` names the
existing initializer. Initializer arguments are `output`, optional
`--project-id PROJECT_ID`, and optional `--title TITLE`. It prints the created
path, does not support JSON output, and refuses an existing output file.

Each `operations` member declares a `script`, `arguments.positional`,
`arguments.options`, `json_output`, and `success_exit_code`. Argument strings
document syntax; consumers must construct argument arrays using their own
explicitly supported operation handlers. They must never interpolate these
strings into a shell or execute an arbitrary command from a manifest.

| Operation | Positional arguments | Options | JSON output | Nonzero result |
| --- | --- | --- | --- | --- |
| `state` | `state` | `--project-root PROJECT_ROOT`, `--json` | `--json` | `2`: blocked |
| `consistency` | `state` | `--project-root PROJECT_ROOT`, `--json` | `--json` | `1`: findings |
| `prose` | `state` | `--project-root PROJECT_ROOT`, `--json` | `--json` | `1`: findings |
| `candidate` | `state candidate` | `--label LABEL`, `--json` | `--json` | `1`: findings/error |
| `docx` | one or more `docx` files | `--require-clean`, `--require-valid-comments`, `--json` | `--json` | `2`: blocked |
| `regression` | none | none | always; no `--json` flag | nonzero: failure |

State, consistency, and prose default the project root to the state file's
directory. Candidate input is a UTF-8 file containing the exact proposed text;
the label defaults to `candidate`. All six operations return `0` on success.
The regression script runs deterministic offline fixtures in a temporary
directory. Audit findings still require scientific and editorial judgment.

The bundle also includes the optional `audit_handoff.py RECORD --json` coverage
checker and its execution guide. It is not a seventh registered adapter operation;
consumers must explicitly support its CLI before invoking it. Complete coverage
and matching hashes do not establish prose quality, venue compliance, or truthful
review evidence. Existing six operation contracts are unchanged.

## Consumer and maintenance boundaries

Configure the bundle directory explicitly, verify it, then use the declared
relative paths under that directory. Verification rejects missing or modified
files, incomplete skill closure, unsafe paths, case collisions, symlinks, Windows
reparse points, hidden/secret files, and unsupported public file types. It never
executes a manifest operation. Hash verification establishes internal integrity,
not publisher authenticity: obtain the manifest and bundle from a trusted source.
Use a stable local bundle directory while checking and consuming it.

When public source bytes change, review the change and update their recorded
hashes. Keep `skill_version` aligned with `.claude-plugin/plugin.json`, and keep
the declared state schema aligned with the template. A plugin release remains a
separate workflow; adding this adapter does not bump the plugin version.

The adapter ships the current public skill tree without changing its scientific
content. After synchronizing a newer main branch, refresh the complete file map,
not only existing hashes: newly added references and binary assets are dependencies
too. Run the full repository tests as well as the verifier, then build, extract,
and verify a bundle before publishing the adapter update. Keep binary assets
marked `-text` in Git and text files normalized to LF so Windows checkouts preserve
the exact public bytes. These checks validate packaging and deterministic client
behavior; they do not constitute scientific validation or model evaluation.
