# API smoke test and static review — 2026-08-18

## Scope and evidence rules

- SUT source: `C:\Users\nguye\Documents\GitHub\eshop-sut`.
- SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`.
- Base URL: `http://localhost:3000`.
- Dynamic run: `20260818_075210197_8a7566de`, 07:52:10 UTC+07.
- Tokens and passwords were held only in process memory and are not recorded.
- “Static” below means source/config inspection. “Dynamic” means an HTTP request
  was actually sent to the running SUT.

The SUT imports `backend/database.js`, whose `initDatabase()` drops, recreates and
seeds tables at process startup (`database.js:13-20`, invocation at the end of
the file). This is a reproducibility and data-loss risk; the review did not edit
or restart the SUT.

## 1. `GET /api/products`

### Static review

| Item | Verified implementation |
| --- | --- |
| Method and URL | `GET http://localhost:3000/api/products` |
| Query | Optional string query `search`. With a truthy value the route performs `name LIKE '%<search>%'`; without it, it selects all products. |
| Request body / Content-Type | No request body and no request `Content-Type` required. `Accept: application/json` is appropriate. |
| Authentication / authorization | None. The route has no authentication middleware. |
| Success | Default `200 OK`, `application/json; charset=utf-8`, JSON array of product rows. Empty result is `[]`. |
| Error behavior | The search branch returns `500` with an HTML database-error body. The no-search branch does not check `err`, so its database-failure behavior is not safely specified by the route. |
| Fields returned | Direct table columns: `id`, `name`, `price`, `description`, `imageUrl`, `category_id`. |
| Required/validation/unique | No route validation. `search` is interpolated directly into SQL. Product columns are nullable and have no unique constraint. |

Code trace:

- JSON middleware: `backend/server.js:12`.
- Route and database access: `backend/server.js:141-155`.
- Product schema: `backend/database.js:63-71`.
- API documentation: `api_specification.md:80-82`.

Safe PowerShell smoke command:

```powershell
$base = 'http://localhost:3000'
Invoke-WebRequest `
  -Method Get `
  -Uri "$base/api/products?search=MacBook" `
  -Headers @{ Accept = 'application/json' } |
  Select-Object StatusCode, Content
```

### Dynamic evidence

The running SUT returned `200 OK` and
`Content-Type: application/json; charset=utf-8` for the search request. Static
inspection establishes that the wire response is a JSON array; the client-side
PowerShell deserializer unrolled the single matching element, so its in-memory
type was not used as evidence of the wire JSON shape.

## 2. `POST /api/register`

### Static review

| Item | Verified implementation |
| --- | --- |
| Method and URL | `POST http://localhost:3000/api/register` |
| Body schema | JSON object read as `{ "name": string, "email": string, "password": string }`. These are intended fields, not enforced requirements. |
| Content-Type | `application/json`; parsed globally by `bodyParser.json()`. |
| Authentication / authorization | None. |
| Success | Default `200 OK`, JSON `{"message":"User registered successfully","id":<lastID>}`. `id` is top-level. |
| Database error | `500`, JSON `{"error":"<SQLite error message>"}`. |
| Required/validation | The route has no missing-field, type, email-format, or password validation. The schema makes all three columns nullable. |
| Unique constraint | `users.email` is not `UNIQUE`; no application-level duplicate check exists. |

Code trace:

- JSON middleware: `backend/server.js:12`.
- Route and parameterized insert: `backend/server.js:20-30`.
- User schema: `backend/database.js:48-61`.
- API documentation: `api_specification.md:11-21`.

Safe PowerShell smoke command (creates one record and prints only the returned
ID; cleanup must use that exact ID through the authenticated Admin delete route):

```powershell
$base = 'http://localhost:3000'
$runId = Get-Date -Format 'yyyyMMdd_HHmmssfff'
$body = @{
  name     = "perf_smoke_$runId"
  email    = "perf_smoke_$runId@example.invalid"
  password = Read-Host 'Temporary smoke password'
} | ConvertTo-Json

$created = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/api/register" `
  -ContentType 'application/json' `
  -Body $body

$created | Select-Object message, id
# Cleanup only $created.id after obtaining an Admin JWT in memory:
# Invoke-RestMethod -Method Delete -Uri "$base/api/admin/users/$($created.id)" `
#   -Headers @{ Authorization = "Bearer $AdminJwt" }
```

### Dynamic duplicate test

The exact same JSON body was posted twice:

```text
Email         : perf_smoke_20260818_075210197_8a7566de@example.invalid
First result  : 200, User registered successfully, id 3
Second result : 200, User registered successfully, id 4
```

This dynamically confirms that duplicate email is accepted by this deployment.
Both records were deleted individually through `DELETE /api/admin/users/:id`:

```text
id 3 cleanup : 200, User deleted
id 4 cleanup : 200, User deleted
verification : ids 3 and 4 absent from GET /api/admin/users
```

## 3. `POST /api/admin/coupons`

### Static review

| Item | Verified implementation |
| --- | --- |
| Method and URL | `POST http://localhost:3000/api/admin/coupons` |
| Body schema | JSON object with `code`, `type`, `discount_value`, `min_order_amount`, `expired_at`, `max_uses_per_user`. |
| Content-Type | `application/json`. |
| Authentication | `Authorization: Bearer <JWT>` is required by `authenticateToken`. Missing token returns `401`; invalid token returns `403`. |
| Authorization | **No Admin-role enforcement.** Middleware verifies the JWT signature and assigns `req.user`; the route never checks `req.user.role`. Any valid normal-user JWT reaches the insert. |
| Success | Default `200 OK`, JSON `{"message":"Coupon created","id":<lastID>}`. |
| Database error | `500`, JSON `{"error":"<SQLite error message>"}`. Duplicate non-null `code` follows this path. |
| Required/validation | No explicit required-field, type, range, date, or enum validation. Route passes missing fields to SQLite. `max_uses_per_user || 1` converts missing, null and zero to `1`; negative values remain accepted. |
| Unique constraint | Only `coupons.code` is `UNIQUE`. Other coupon columns are nullable. SQLite permits multiple `NULL` values under a unique constraint. |

Code trace:

- JWT middleware: `backend/server.js:100-110`.
- Coupon route and insert: `backend/server.js:456-481`.
- Exact cleanup route: `backend/server.js:483-487`.
- Coupon schema: `backend/database.js:28-38`.
- API documentation: `api_specification.md:201-214`.

### Admin JWT acquisition

Obtain an Admin JWT with `POST /api/login` and a JSON body containing `email` and
`password`. Successful login returns default `200` with:

```json
{
  "message": "Login successful",
  "token": "<redacted>",
  "user": { "id": 1, "role": "admin" }
}
```

The token is a top-level field. Login implementation is
`backend/server.js:32-52`; seeded Admin configuration is
`backend/database.js:90-94`. Evidence must not print or commit the token/password.

Safe PowerShell smoke pattern (expects `$AdminJwt` already held in memory and
deletes exactly the returned ID):

```powershell
$base = 'http://localhost:3000'
$runId = Get-Date -Format 'yyyyMMdd_HHmmssfff'
$code = "perf_smoke_admin_$runId"
$headers = @{ Authorization = "Bearer $AdminJwt" }
$body = @{
  code              = $code
  type              = 'percent'
  discount_value    = 10
  min_order_amount  = 100000
  expired_at        = '2099-12-31'
  max_uses_per_user = 1
} | ConvertTo-Json

$created = Invoke-RestMethod -Method Post `
  -Uri "$base/api/admin/coupons" -Headers $headers `
  -ContentType 'application/json' -Body $body
try {
  $created | Select-Object message, id
} finally {
  if ($created.id) {
    Invoke-RestMethod -Method Delete `
      -Uri "$base/api/admin/coupons/$($created.id)" -Headers $headers
  }
}
```

### Dynamic coupon evidence

```text
No token:
  code    = perf_smoke_notoken_20260818_075210197_8a7566de
  result  = 401, Unauthorized
  verify  = code absent; no cleanup record existed

Admin JWT:
  code    = perf_smoke_admin_20260818_075210197_8a7566de
  result  = 200, Coupon created, id 5
  cleanup = 200, Coupon deleted

Normal-user JWT (role=user):
  code    = perf_smoke_user_20260818_075210197_8a7566de
  result  = 200, Coupon created, id 6
  cleanup = 200, Coupon deleted

Final verification:
  created coupon ids 5 and 6 absent from GET /api/coupons
```

The normal-user result is dynamic evidence of an authorization defect, detailed
in `evidence/authorization-test-20260818.md`.

## Cleanup summary

- Created user IDs: `3`, `4`; both deleted and verified absent.
- Created coupon IDs: `5`, `6`; both deleted and verified absent.
- The no-token code was verified absent.
- No broad prefix deletion, database reset, SUT restart or SUT source change was
  performed.
