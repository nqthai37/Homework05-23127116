param(
    [Parameter(Mandatory = $true)]
    [string]$JtlPath
)

$rows = @(Import-Csv -LiteralPath $JtlPath)
if ($rows.Count -eq 0) {
    throw "No samples found in $JtlPath"
}

function Get-Percentile {
    param([double[]]$Values, [double]$Percentile)
    $sorted = @($Values | Sort-Object)
    if ($sorted.Count -eq 1) { return $sorted[0] }
    $rank = ($Percentile / 100) * ($sorted.Count - 1)
    $lower = [math]::Floor($rank)
    $upper = [math]::Ceiling($rank)
    if ($lower -eq $upper) { return $sorted[$lower] }
    return $sorted[$lower] + (($rank - $lower) * ($sorted[$upper] - $sorted[$lower]))
}

$startMs = ($rows | Measure-Object -Property timeStamp -Minimum).Minimum
$endMs = ($rows | ForEach-Object { [double]$_.timeStamp + [double]$_.elapsed } | Measure-Object -Maximum).Maximum
$durationSeconds = [math]::Max(0.001, ($endMs - $startMs) / 1000)

$rows | Group-Object label | ForEach-Object {
    $group = @($_.Group)
    $elapsed = [double[]]@($group | ForEach-Object { [double]$_.elapsed })
    $errors = @($group | Where-Object { $_.success -ne "true" }).Count
    [pscustomobject]@{
        Label = $_.Name
        Samples = $group.Count
        Errors = $errors
        ErrorRatePercent = [math]::Round(($errors / $group.Count) * 100, 3)
        AverageMs = [math]::Round(($elapsed | Measure-Object -Average).Average, 2)
        MinMs = ($elapsed | Measure-Object -Minimum).Minimum
        P50Ms = [math]::Round((Get-Percentile $elapsed 50), 2)
        P90Ms = [math]::Round((Get-Percentile $elapsed 90), 2)
        P95Ms = [math]::Round((Get-Percentile $elapsed 95), 2)
        P99Ms = [math]::Round((Get-Percentile $elapsed 99), 2)
        MaxMs = ($elapsed | Measure-Object -Maximum).Maximum
        ThroughputRps = [math]::Round($group.Count / $durationSeconds, 2)
    }
} | Format-Table -AutoSize
