param(
    [string]$BaseUrl = "http://localhost:3000",
    [Parameter(Mandatory = $true)]
    [System.Management.Automation.PSCredential]$AdminCredential
)

$ErrorActionPreference = "Stop"

$login = Invoke-RestMethod `
    -Method Post `
    -Uri "$BaseUrl/api/login" `
    -ContentType "application/json" `
    -Body (@{
        email = $AdminCredential.UserName
        password = $AdminCredential.GetNetworkCredential().Password
    } | ConvertTo-Json)

if (-not $login.token) {
    throw "Admin login did not return a JWT token."
}

$headers = @{ Authorization = "Bearer $($login.token)" }
$deletedUsers = 0
$deletedCoupons = 0

$users = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/admin/users" -Headers $headers
foreach ($user in @($users)) {
    if ($user.email -like "perf_register_*@example.invalid") {
        Invoke-RestMethod -Method Delete -Uri "$BaseUrl/api/admin/users/$($user.id)" -Headers $headers | Out-Null
        $deletedUsers++
    }
}

$coupons = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/coupons" -Headers $headers
foreach ($coupon in @($coupons)) {
    if ($coupon.code -like "PERF_*") {
        Invoke-RestMethod -Method Delete -Uri "$BaseUrl/api/admin/coupons/$($coupon.id)" -Headers $headers | Out-Null
        $deletedCoupons++
    }
}

[pscustomobject]@{
    DeletedPerformanceUsers = $deletedUsers
    DeletedPerformanceCoupons = $deletedCoupons
}
