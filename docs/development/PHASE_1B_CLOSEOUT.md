# Phase 1B Closeout: erste ausführbare ORION-Baseline

- Datum: 2026-07-19
- Repository-Version: `0.3.0-dev.0`
- Branch: `main`
- Status: erste reviewbare Entwicklungsbaseline; kein Production Release
- Tag: keiner

## Repository-Zustand

Vor diesem Closeout besaß das ORION-Repository noch keinen Commit. Der
Commit-Kandidat besteht ausschließlich aus ORION-eigenen Text-, Python-, Shell-
und YAML-Dateien. Keine Commit-Datei überschreitet 1 MiB.

Die unabhängigen Repositories und lokalen Quellen sind nicht Bestandteil der
Baseline:

- NEXAH Core ist nur als ignorierter Symlink unter `.workspace/repositories/`
  lokal verbunden.
- NEXAH Library und Builder Hub sind nicht vendored.
- Ollama, sein Modell-Store und seine Binärdateien liegen vollständig außerhalb
  dieses Repositories.
- Architekturvisualisierungen und Kontaktbögen bleiben unter dem ignorierten
  Verzeichnis `source_material/`.

## Implementierter Scope

- stabile Architektur-, Governance-, ADR-, Workspace- und Release-Dokumentation
- unveränderliche Phase-1A-Verträge
- `ReasoningBackend`-Port und unverändertes `FakeBackend`
- deterministischer Phase-1A-Executor und unabhängige Validation
- lokales, Loopback-beschränktes `OllamaBackend`
- provider-neutrale Backend-, Timeout-, Unavailable- und Responsefehler
- Unit-, Grenz-, Konfigurations-, Timeout- und Malformed-Response-Tests
- opt-in Integrationstest gegen die extern verwaltete lokale Ollama-Runtime

## Ausgeschlossener Scope

- keine Änderung an NEXAH Core, Library oder Builder Hub
- keine Kernel- oder Library-Schreiboperation
- keine weitere Provider- oder Modellruntime
- kein Runtime-Lifecycle-Management
- kein Streaming, Tool Calling, Vision oder Embedding
- kein Retrieval, Vector Store oder Prompt-Repository
- keine Persistenz, Run-Datenbank oder Replay-Infrastruktur
- kein produktives Release, kein stabiler SemVer-Tag

## Repository-Hygiene

Die Commit-Kandidaten wurden auf Secrets, Credential-Werte, private Schlüssel,
eingebettete Zugangsdaten, maschinenspezifische absolute Pfade, Modellgewichte,
Binärdateien und große Dateien geprüft. Es wurden keine solchen Inhalte gefunden.
Generische Begriffe wie `credentials` im Validierungscode und in `.gitignore`
enthalten keine Credential-Werte.

`.gitignore` schließt mindestens folgende Klassen aus:

- `.workspace/` und `source_material/`
- Runs, Outputs, Coverage, Logs und temporäre Integrationsausgaben
- Python-, Test-, Typecheck- und Linter-Caches
- virtuelle Umgebungen und lokale Python-Versionsdateien
- Modell-Stores sowie GGUF-, GGML-, Safetensors-, ONNX- und weitere Gewichtstypen
- Secret-Verzeichnisse, Environment-Dateien, Tokens und Key-Dateien
- macOS-, Windows- und IDE-Metadaten
- temporäre Dateien und Editor-Swap-Dateien

Konkrete `git check-ignore`-Proben für jede dieser Klassen waren erfolgreich.

## Runtime- und Modell-Kompatibilitätsbaseline

| Bestandteil | Verifizierter Wert |
|---|---|
| Runtime | Ollama `0.32.1` |
| Endpoint | `http://127.0.0.1:11434` |
| Modell | `llama3.1:8b` |
| Digest | `46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e` |
| Format | GGUF |
| Parameter | 8.0B |
| Quantisierung | Q4_K_M |
| Fähigkeiten laut Runtime | Completion, Tools |

Ollama ist eine extern verwaltete Runtime. ORION installiert, startet, stoppt oder
überwacht den Dienst nicht. Ist er nicht erreichbar, meldet der Adapter einen
provider-neutralen `ReasoningBackendUnavailableError`. Der Integrationstest wird
in diesem Fall nicht ausgeführt und darf das Runtime-Verhalten nicht verändern.

## Verifikationsergebnisse

| Prüfung | Ergebnis |
|---|---|
| `make test` | PASS: 12 Tests entdeckt, 11 bestanden, 1 opt-in Integrationstest erwartungsgemäß übersprungen |
| `make integration` | PASS: 1 realer End-to-End-Test gegen `llama3.1:8b` |
| `./scripts/check-workspace` | PASS |
| `./scripts/release-check --development` | PASS für `0.3.0-dev.0` |
| Markdown-Linkprüfung | PASS |
| Python-Syntax und Imports | PASS für 12 Python-Dateien |
| Provider-SDK-Importprüfung | PASS; keine Provider-SDKs oder Drittanbieter-HTTP-Clients |
| Netzwerk-Importgrenze | PASS; Netzwerkimporte nur im Ollama-Adapter |
| Secret- und Credential-Scan | PASS |
| Absolutpfadprüfung | PASS |
| Vendor- und Submodule-Prüfung | PASS; keine vendorten Repositories oder Submodule |

## Eingefrorene Phase-1A-Dateien

Die folgenden SHA-256-Prüfsummen wurden vor und nach Phase 1B identisch
verifiziert:

| Datei | SHA-256 |
|---|---|
| `src/orion/contracts.py` | `82e4dbc3c915cf6545bc410ce7aa00749ef86a52241e92ecf8f24de900c9ab13` |
| `src/orion/backend.py` | `6e8057112a116172136b02311a314dff76bd90818f1c9992d481ee68977ed6f1` |
| `src/orion/executor.py` | `12ed38214c12ba637d63f1f6fb81619f43e886ac5c6ff91cdfc8a1f2e4fb9fd4` |
| `src/orion/validation.py` | `47bfcce22f804c109f8b4a7428aa551c962ea6a2f78bf792daf30ff320860c66` |
| `src/orion/fake_backend.py` | `114fff63a1a8345c73028503b8086f149e8f2494c18aae604448e610fc46f736` |

## Reproduktionsbefehle

Standard- und Release-Prüfungen:

```bash
make test
./scripts/check-workspace
./scripts/release-check --development
```

Erreichbarkeit der externen Runtime prüfen und nur bei Erfolg integrieren:

```bash
curl --fail --silent --show-error --max-time 3 \
  http://127.0.0.1:11434/api/version
curl --fail --silent --show-error --max-time 3 \
  http://127.0.0.1:11434/api/tags
make integration
```

Frozen Checksums:

```bash
shasum -a 256 \
  src/orion/contracts.py \
  src/orion/backend.py \
  src/orion/executor.py \
  src/orion/validation.py \
  src/orion/fake_backend.py
```

Syntax und Imports ohne Bytecode-Ausgabe:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -c \
  'import ast; from pathlib import Path; files=sorted([*Path("src").rglob("*.py"), *Path("tests").rglob("*.py")]); [ast.parse(f.read_text(encoding="utf-8"), filename=str(f)) for f in files]; import orion; import orion.ollama_backend; print(f"checked {len(files)} Python files")'
```

Markdown-Links:

```bash
python3 -c 'from pathlib import Path; import re; root=Path(".").resolve(); bad=[]
for f in root.rglob("*.md"):
    if any(p in {".git", ".workspace", "source_material"} for p in f.parts): continue
    for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", f.read_text(encoding="utf-8")):
        target=target.split("#",1)[0]
        if target and "://" not in target and not target.startswith("mailto:") and not (f.parent/target).resolve().exists(): bad.append(f"{f}: {target}")
raise SystemExit("\n".join(bad) if bad else 0)'
```

Commit-Hygiene und staged Review:

```bash
git status --short --ignored
git diff --cached --check
git diff --cached --stat
git diff --cached --name-status
git diff --cached
```

## Bekannte Grenzen

- Ein echtes Backend beweist noch keine Cross-Provider-Modellunabhängigkeit.
- `backend_id` enthält den Modelltag, aber der eingefrorene `ReasoningResult`
  besitzt kein separates Modell-Digest-Feld.
- Modellantworten sind trotz Temperatur- und Seed-Konfiguration nicht als
  bitidentisch garantiert.
- Backendfehler werden kontrolliert typisiert, aber nicht als persistierte Runs
  aufgezeichnet.
- Der Integrationstest hängt bewusst von einer extern erreichbaren Runtime ab.

## Deferred Work

- llama.cpp als zweites Conformance-Backend
- Capability Negotiation und Routing
- persistente Run Records und Replay
- strukturierte NEXAH-Objektprojektionen
- Context Retrieval und kontrollierte Nachladung
- Builder-Hub- und Library-Integration
- produktive Release-, Packaging- und Deploymententscheidungen

Diese Punkte sind nicht Bestandteil der ersten ausführbaren Baseline.
