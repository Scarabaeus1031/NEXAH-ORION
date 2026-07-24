# Schemas

Reserved for optional machine-readable transport encodings of ORION-owned
public contracts.

The frozen Version 1.0 public specifications live in
`docs/architecture/contracts/`; their executable, transport-independent Python
binding lives in `src/orion/public_contracts/`. No JSON Schema, protocol schema,
or other transport encoding has been approved. Adding one requires:

1. its repository and contract owner are confirmed;
2. an ADR defines its authority and compatibility surface;
3. producer and consumers are named;
4. versioning and migration behavior are documented.

This directory must not redefine the public contract suite. Existing Core types
remain owned by the frozen NEXAH Core and are not copied here.
