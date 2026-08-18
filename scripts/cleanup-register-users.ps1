[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "Medium")]
param(
    [string]$BaseUrl = "http://localhost:3000",

    [Parameter(Mandatory = $true)]
    [System.Management.Automation.PSCredential]$AdminCredential
)

$ErrorActionPreference = "Stop"
$targetPattern = "^perf_register_.*@example\.invalid$"

$loginBody = @{
    email = $AdminCredential.UserName
    password = $AdminCredential.GetNetworkCredential().Password
} | ConvertTo-Json

$login = Invoke-RestMethod `
    -Method Post `
    -Uri "$BaseUrl/api/login" `
    -ContentType "application/json" `
    -Body $loginBody

if (-not $login.token) {
    throw "Admin login did not return a JWT token."
}

$headers = @{ Authorization = "Bearer $($login.token)" }
$usersResponse = Invoke-RestMethod `
    -Method Get `
    -Uri "$BaseUrl/api/admin/users" `
    -Headers $headers
$users = @($usersResponse | ForEach-Object { $_ })

$targets = @($users | Where-Object {
    $_.email -is [string] -and $_.email -match $targetPattern
})

$deletedIds = [System.Collections.Generic.List[int]]::new()
foreach ($user in $targets) {
    if ($PSCmdlet.ShouldProcess($user.email, "Delete test user id $($user.id)")) {
        Invoke-RestMethod `
            -Method Delete `
            -Uri "$BaseUrl/api/admin/users/$($user.id)" `
            -Headers $headers | Out-Null
        $deletedIds.Add([int]$user.id)
    }
}

$remainingResponse = Invoke-RestMethod `
    -Method Get `
    -Uri "$BaseUrl/api/admin/users" `
    -Headers $headers
$remaining = @($remainingResponse | ForEach-Object { $_ } | Where-Object {
        $_.email -is [string] -and $_.email -match $targetPattern
    })

[pscustomobject]@{
    MatchPattern = $targetPattern
    MatchedUsers = $targets.Count
    DeletedUsers = $deletedIds.Count
    RemainingMatchingUsers = $remaining.Count
    FirstDeletedId = if ($deletedIds.Count) { $deletedIds[0] } else { $null }
    LastDeletedId = if ($deletedIds.Count) { $deletedIds[$deletedIds.Count - 1] } else { $null }
}

if ($remaining.Count -ne 0 -and $deletedIds.Count -ne 0) {
    throw "Cleanup verification failed: matching test users remain."
}
