param(
    [Parameter(Mandatory = $true)]
    [int]$TargetProcessId,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [Parameter(Mandatory = $true)]
    [int]$DurationSeconds,

    [int]$IntervalSeconds = 1
)

$ErrorActionPreference = "Stop"
$logicalProcessors = [Environment]::ProcessorCount
$samples = [System.Collections.Generic.List[object]]::new()
$previousCpuSeconds = $null
$previousTime = $null
$deadline = (Get-Date).AddSeconds($DurationSeconds)

while ((Get-Date) -lt $deadline) {
    $now = Get-Date
    $process = Get-Process -Id $TargetProcessId -ErrorAction Stop

    $processCpuPercent = $null
    if ($null -ne $previousCpuSeconds -and $null -ne $previousTime) {
        $wallSeconds = ($now - $previousTime).TotalSeconds
        if ($wallSeconds -gt 0) {
            $processCpuPercent = (($process.CPU - $previousCpuSeconds) / $wallSeconds / $logicalProcessors) * 100
        }
    }

    $systemCpu = $null
    $availableMemoryMb = $null
    $diskTimePercent = $null
    try {
        $counter = Get-Counter @(
            "\Processor(_Total)\% Processor Time",
            "\Memory\Available MBytes",
            "\PhysicalDisk(_Total)\% Disk Time"
        ) -ErrorAction Stop

        foreach ($sample in $counter.CounterSamples) {
            if ($sample.Path -like "*Processor(_Total)*") { $systemCpu = $sample.CookedValue }
            elseif ($sample.Path -like "*Memory*Available MBytes*") { $availableMemoryMb = $sample.CookedValue }
            elseif ($sample.Path -like "*PhysicalDisk(_Total)*") { $diskTimePercent = $sample.CookedValue }
        }
    } catch {
        # Process-level CPU and memory remain valid when system counters are unavailable.
    }

    $samples.Add([pscustomobject]@{
        Timestamp = $now.ToString("o")
        BackendProcessId = $TargetProcessId
        BackendCpuPercent = if ($null -eq $processCpuPercent) { $null } else { [math]::Round($processCpuPercent, 2) }
        BackendWorkingSetMB = [math]::Round($process.WorkingSet64 / 1MB, 2)
        BackendPrivateMemoryMB = [math]::Round($process.PrivateMemorySize64 / 1MB, 2)
        SystemCpuPercent = if ($null -eq $systemCpu) { $null } else { [math]::Round($systemCpu, 2) }
        AvailableMemoryMB = if ($null -eq $availableMemoryMb) { $null } else { [math]::Round($availableMemoryMb, 2) }
        PhysicalDiskTimePercent = if ($null -eq $diskTimePercent) { $null } else { [math]::Round($diskTimePercent, 2) }
    })

    $previousCpuSeconds = $process.CPU
    $previousTime = $now
    Start-Sleep -Seconds $IntervalSeconds
}

$parent = Split-Path -Parent $OutputPath
if ($parent) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
}
$samples | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding UTF8

