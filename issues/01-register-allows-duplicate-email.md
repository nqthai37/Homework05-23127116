# `POST /api/register` accepts duplicate email addresses

## Environment and reproduction

EShop commit `85af3ba875c88283615e22cb108f13e2fccaf0e9`, dynamic run `20260818_075210197_8a7566de`. POST the same sanitized `{name,email,password}` twice using an `example.invalid` address. Do not log the password.

## Expected

The second request is rejected (for example `409 Conflict`) and no second identity is created.

## Actual

Both requests returned `200`, `User registered successfully`, with distinct IDs `3` and `4`. Both exact IDs were deleted and verified absent.

## Evidence and impact

`database.js:50-60` has no `UNIQUE` constraint on email, and `server.js:20-30` has no duplicate check. Dynamic evidence: `evidence/smoke-test-20260818.md`. Duplicate identities create ambiguous account ownership and contaminate tests unless unique addresses are used.
