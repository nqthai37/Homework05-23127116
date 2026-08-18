# Normal-user JWT can create an Admin coupon

## Reproduction

Login as a seeded normal user, confirm `role=user`, retain the JWT only in memory, and POST a sanitized unique body to `/api/admin/coupons`. Delete the exact returned ID afterward.

## Expected / actual

Expected `403 Forbidden` and no coupon. Actual: `200`, `Coupon created`, ID `6`; exact-ID cleanup succeeded. A no-token control returned `401`, so authentication exists but role authorization does not.

## Evidence and impact

`authenticateToken` (`server.js:100-110`) validates the JWT; the route (`server.js:457-480`) never checks `req.user.role`. Dynamic evidence: `evidence/authorization-test-20260818.md`. Any authenticated user can create discount instruments intended for administrators (FR-12/SEC-03).
