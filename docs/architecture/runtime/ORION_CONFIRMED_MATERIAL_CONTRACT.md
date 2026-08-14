# ORION Version 1.1 — Confirmed Material Contract

Status: Normative, frozen for Runtime API 1.0
Schema: `orion.confirmed-material/1.0`
Contract version: `1.0.0`

## 1. Purpose

This contract is the only Confirmed Material wire format accepted by Runtime
API 1.0. It replaces implicit dependence on NEXAHEDRON's internal
`orion.confirmed-local-source/0.1-alpha` shape.

It does not change the frozen ORION Core. It defines a lossless transport
binding to the existing frozen `ConfirmedMarkdownSource`.

## 2. Exact schema

The top-level object MUST contain exactly:

```text
schema_version
orientation_object_id
orientation_object_version
source
confirmation
```

`schema_version` MUST equal `orion.confirmed-material/1.0`.

`source` MUST contain exactly:

```text
entry_id
source_owner
source_ref
source_version
fragment_ref
media_type
grammar
grammar_version
content
integrity_sha256
```

`confirmation` MUST contain exactly:

```text
confirmed_by
confirmed_revision
confirmation_id
```

Unknown, missing, duplicate, or `null` fields are rejected.

## 3. Field rules

| Field | Normative rule |
|---|---|
| `orientation_object_id` | Non-empty UTF-8 text; exact match to the contained Orientation Request object identity |
| `orientation_object_version` | Non-empty UTF-8 text; exact match to the contained Orientation Request object version |
| `source.entry_id` | Non-empty stable source identity |
| `source.source_owner` | Non-empty Human or Library source-owner identity |
| `source.source_ref` | Non-empty source reference; transported, not dereferenced by Runtime |
| `source.source_version` | `sha256:` followed by `source.integrity_sha256` |
| `source.fragment_ref` | Exactly `whole` |
| `source.media_type` | Exactly `text/markdown;charset=utf-8` |
| `source.grammar` | Exactly `CommonMark` |
| `source.grammar_version` | Exactly `0.31.2` |
| `source.content` | Human-confirmed Markdown text satisfying Section 4 |
| `source.integrity_sha256` | Lowercase SHA-256 of the exact UTF-8 content bytes |
| `confirmation.confirmed_by` | Non-empty Human authority identity |
| `confirmation.confirmed_revision` | Integer from 1 through 2,147,483,647 |
| `confirmation.confirmation_id` | Deterministic identity defined in Section 5 |

No field grants ORION authority over the Human or source.

## 4. Accepted content

Content MUST:

- encode strictly as UTF-8;
- contain no UTF-8 BOM;
- contain no U+0000;
- contain no isolated Unicode surrogate;
- use LF only; CR and CRLF are rejected;
- contain at most `262,144` UTF-8 bytes;
- contain at most `8,192` physical lines;
- remain one whole document boundary.

The empty string is accepted by the frozen Markdown profile and produces the
document root. Whitespace-only input is accepted only if the frozen source
constructor accepts it.

Unsupported CommonMark constructs and extensions follow the frozen Markdown
Structural Representation Profile v1 rejection rules. Runtime and Gateway
perform no repair.

## 5. Integrity and confirmation identity

`source.integrity_sha256` is:

```text
SHA-256(UTF-8(source.content))
```

`source.source_version` is:

```text
sha256:<source.integrity_sha256>
```

The confirmation identity basis contains exactly:

```text
orientation_object_id
orientation_object_version
source_id
source_revision
confirmed_by
confirmed_revision
boundary_ref
```

with these mappings:

```text
source_id       = source.entry_id
source_revision = source.source_version
boundary_ref    = "whole"
```

The basis is serialized using `ORION Canonical JSON 1.0`.

`confirmation.confirmation_id` is:

```text
confirmation-<first 16 lowercase hexadecimal characters of
SHA-256(canonical confirmation identity basis)>
```

This algorithm intentionally matches the frozen Core constructor. The older
NEXAHEDRON Alpha confirmation basis is not accepted on the Version 1.1 wire.

## 6. Canonical serialization

The complete artifact is serialized with `ORION Canonical JSON 1.0` as defined
by `ORION_IDENTITY_CONTRACT.md`.

Transport parsers MAY accept non-canonical JSON layout, but Gateway MUST
canonicalize only after rejecting duplicate keys, unknown fields, floats,
invalid UTF-8, and invalid values. Integrity fields are always checked against
canonical field meaning and exact source-content bytes.

## 7. Mapping into the frozen Core

Gateway validates this contract. The Core Invocation Adapter maps it exactly as
specified in `ORION_SLICE_EXECUTION_CONTRACT.md`.

After construction, these values MUST be equal:

| Wire artifact | Frozen Core artifact |
|---|---|
| `orientation_object_id` | `ConfirmedMarkdownSource.orientation_object_id` |
| `orientation_object_version` | `ConfirmedMarkdownSource.orientation_object_version` |
| `source.entry_id` | `source_id` |
| `source.source_owner` | `source_owner` |
| `source.source_ref` | `source_ref` |
| `source.source_version` | `source_revision` |
| `source.content` | `content` |
| `source.integrity_sha256` | `content_sha256` |
| `confirmation.confirmed_by` | `confirmed_by` |
| `confirmation.confirmed_revision` | `confirmed_revision` |
| `confirmation.confirmation_id` | `confirmation_id` |

There is no semantic conversion, normalization, or content transformation.

## 8. Post-projection admission bounds

An invocation is operationally admissible only when the frozen Projection
produces:

- no more than `128` declared elements including the document root;
- no more than `16,384` total final Relation Objects;
- an artifact chain whose canonical embedded response does not exceed
  `16,777,216` bytes.

These bounds do not change the Core result. Exceeding a bound discards the
isolated invocation and returns an operational limit error. No truncated
artifact is published.

## 9. Rejection rules

Gateway rejects the artifact with `422` when:

- schema or fields differ;
- an identity field is empty or malformed;
- request and material Orientation Object identities differ;
- source integrity or version differs;
- confirmation identity differs;
- encoding, newline, boundary, media type, grammar, or grammar version differs;
- content exceeds pre-execution limits;
- material is mutable, unconfirmed, or Alpha-shaped;
- Evidence is embedded in the material;
- executable instructions, credentials, or provider configuration appear as
  contract fields.

`413` is used only when the HTTP body exceeds the total request-body limit
before contract validation.

## 10. Authority

The Human Workspace owns confirmation. NEXAHEDRON constructs and freezes the
wire artifact. Gateway validates it. The Adapter maps it. The Core consumes the
resulting frozen source.

Runtime does not confirm material, inspect its meaning, or alter it.
