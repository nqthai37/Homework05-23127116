param(
    [string]$BaseUrl = 'http://localhost:3000',
    [Parameter(Mandatory = $true)]
    [System.Management.Automation.PSCredential]$AdminCredential
)

$ErrorActionPreference = 'Stop'
$prefixPattern = '^PERF_'

$loginBody = @{
    email = $AdminCredential.UserName
    password = $AdminCredential.GetNetworkCredential().Password
} | ConvertTo-Json

$login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/login" `
    -ContentType 'application/json' -Body $loginBody
if (-not $login.token -or $login.user.role -ne 'admin') {
    throw 'Login did not return an Admin JWT.'
}

$headers = @{ Authorization = "Bearer $($login.token)" }
$response = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/coupons" -Headers $headers
$targets = @($response | ForEach-Object { $_ }) | Where-Object {
    $_.code -is [string] -and $_.code -match $prefixPattern
}

foreach ($coupon in $targets) {
    Invoke-RestMethod -Method Delete `
        -Uri "$BaseUrl/api/admin/coupons/$($coupon.id)" -Headers $headers | Out-Null
}

$remainingResponse = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/coupons" -Headers $headers
$remaining = @($remainingResponse | ForEach-Object { $_ }) | Where-Object {
    $_.code -is [string] -and $_.code -match $prefixPattern
}
if ($remaining.Count -ne 0) {
    throw "Cleanup verification failed: $($remaining.Count) PERF_ coupon(s) remain."
}

[pscustomobject]@{
    MatchPattern = $prefixPattern
    DeletedCount = $targets.Count
    RemainingCount = $remaining.Count
}
