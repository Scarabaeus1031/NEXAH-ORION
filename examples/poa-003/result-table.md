<!-- poa-003:representation-id=poa-003-markdown-table -->
<!-- poa-003:result-id=result-001 -->
<!-- poa-003:result-sha256=6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3 -->
<!-- poa-003:authority=non-authoritative -->

# POA-003 Representation B — Tabular Result

This deterministic table presents the immutable Result identified below. It is
a non-authoritative Representation. It does not validate the source, recommend,
approve, decide, or change the Result.

| Binding | Value |
| --- | --- |
| Result | `result-001` |
| Result SHA-256 | `6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3` |
| Media | `text/markdown` |
| Authority | `non-authoritative` |

## Result paths

Values are JSON literals so that strings and numbers remain distinguishable.

| Result path | JSON value |
| --- | --- |
| `/id` | `"result-001"` |
| `/status` | `"complete"` |
| `/expression_ref` | `"expression-001"` |
| `/expression_sha256` | `"cc57e561e0e209d4cca504f63d044bb012a740ac6479da71fd4dacc0247a9667"` |
| `/processor` | `"poa-001-compare"` |
| `/processor_sha256` | `"05e122b25d0cfb5f2ec05ec3d88ed9305013fb30f85ea77210380e885704b262"` |
| `/comparison/field` | `"declared_value"` |
| `/comparison/sources/0/record_ref` | `"record-a"` |
| `/comparison/sources/0/value` | `2` |
| `/comparison/sources/1/record_ref` | `"record-b"` |
| `/comparison/sources/1/value` | `5` |
| `/comparison/signed_difference` | `3` |
| `/evidence/0/record_ref` | `"record-a"` |
| `/evidence/0/value` | `"supplied-record-a"` |
| `/evidence/1/record_ref` | `"record-b"` |
| `/evidence/1/value` | `"supplied-record-b"` |
| `/uncertainty/records/0/record_ref` | `"record-a"` |
| `/uncertainty/records/0/value` | `"none-declared"` |
| `/uncertainty/records/1/record_ref` | `"record-b"` |
| `/uncertainty/records/1/value` | `"none-declared"` |
| `/uncertainty/limitation` | `"The supplied values are not independently validated."` |
| `/prohibited_implications/0` | `"preference"` |
| `/prohibited_implications/1` | `"recommendation"` |
| `/prohibited_implications/2` | `"domain-validity"` |

## Declared mapping loss

- JSON nesting is flattened into explicit Result paths.
- The SVG's spatial relation and arrow are not reproduced.
- No value, evidence item, uncertainty statement, limitation, or prohibited
  implication is intentionally omitted.

The immutable Result, not this table, remains the semantic source.
