# C40 Simplification Notes

DAAF remains bounded because it does not:
- redefine `C38` session or message identity,
- replace `C32` lifecycle and registration rules,
- replace `C36` translation and receptor logic,
- replace `C23` runtime enforcement,
- replace `C5` verification authority.

It does:
- define native and non-native trust anchors,
- define the bounded security profile set,
- define canonical authority binding,
- define replay and downgrade rules,
- define explicit capability grants for sensitive actions.

This is the minimum L3 authority Alternative B needs before the downstream
manifest, tool, SDK, and conformance tasks can proceed safely.
