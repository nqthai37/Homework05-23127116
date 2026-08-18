# Authorization verification — 2026-08-18

## Objective

Verify whether `POST /api/admin/coupons` enforces both authentication and the
documented Admin-role boundary. Tokens and passwords are redacted and were never
written to this file.

## Static evidence

`authenticateToken` at `backend/server.js:100-110`:

1. reads the bearer token;
2. returns `401 {"error":"Unauthorized"}` when absent;
3. verifies the JWT and returns `403 {"error":"Forbidden"}` when invalid;
4. assigns the decoded payload to `req.user` and calls `next()`.

`POST /api/admin/coupons` at `backend/server.js:457-480` uses this middleware but
does not read or validate `req.user.role`. Therefore source inspection predicts
that any valid user JWT can create coupons. This paragraph is **static evidence**,
not proof that the request succeeded dynamically.

Admin and normal-user JWTs were acquired dynamically from `POST /api/login`.
The response returns `token` and `user` at `backend/server.js:32-52`. Credentials
came from local seed configuration and are not reproduced here.

## Dynamic procedure

Run ID: `20260818_075210197_8a7566de`.

1. Login as the seeded Admin; status `200`, token retained only in memory.
2. Login as the seeded normal user; status `200`; response role was `user`.
3. Call the coupon endpoint without a token.
4. Call it with the Admin JWT and a unique `perf_smoke_` code.
5. Call it with the normal-user JWT and a different unique `perf_smoke_` code.
6. Delete only the coupon IDs returned by steps 4 and 5.
7. Query coupons and verify both IDs and the rejected no-token code are absent.

## Observed dynamic results

| Case | Authenticated role | Code | HTTP | Response | Created ID | Cleanup |
| --- | --- | --- | ---: | --- | ---: | --- |
| No token | N/A | `perf_smoke_notoken_20260818_075210197_8a7566de` | 401 | `Unauthorized` | N/A | Code verified absent |
| Admin JWT | `admin` | `perf_smoke_admin_20260818_075210197_8a7566de` | 200 | `Coupon created` | 5 | ID 5 deleted; verified absent |
| Normal-user JWT | `user` | `perf_smoke_user_20260818_075210197_8a7566de` | 200 | `Coupon created` | 6 | ID 6 deleted; verified absent |

## Conclusion

Authentication is enforced: the request without a token returned `401`.
Authorization is not enforced: a JWT whose login response reported `role=user`
successfully performed an Admin coupon creation and received `200` with ID `6`.
This is dynamic evidence supporting the static finding that the route does not
check `req.user.role`.

The test created no persistent coupon record. Both successful test records were
deleted by exact ID and verified absent. No token or password is present in the
evidence.

## Safe reproduction pattern

Use two independently acquired in-memory JWT variables and never print them:

```powershell
$headers = @{ Authorization = "Bearer $NormalUserJwt" }
$code = "perf_smoke_user_$(Get-Date -Format 'yyyyMMdd_HHmmssfff')"
$body = @{ code=$code; type='percent'; discount_value=10;
  min_order_amount=100000; expired_at='2099-12-31';
  max_uses_per_user=1 } | ConvertTo-Json

$created = Invoke-RestMethod -Method Post `
  -Uri 'http://localhost:3000/api/admin/coupons' `
  -Headers $headers -ContentType 'application/json' -Body $body
try {
  $created | Select-Object message, id
} finally {
  if ($created.id) {
    Invoke-RestMethod -Method Delete `
      -Uri "http://localhost:3000/api/admin/coupons/$($created.id)" `
      -Headers $headers
  }
}
```
