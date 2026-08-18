# HW05 test environment — 2026-08-18

Collection time zone: UTC+07:00 (Asia/Saigon). All values below were obtained
from commands run on the machine intended for the HW05 official runs. No value
was inferred from a generic hardware specification.

## Environment summary

| Item | Observed value | Command/evidence |
| --- | --- | --- |
| Hostname | `LAPTOP-BKI58MTI` | `hostname`; `$env:COMPUTERNAME` |
| Windows | Microsoft Windows 11 Home Single Language, 64-bit, version `10.0.26200`, build `26200.9168`, display version `25H2` | `Get-CimInstance Win32_OperatingSystem`; registry `CurrentBuild=26200`, `UBR=9168` |
| Computer | LENOVO model `82JW` | `Get-CimInstance Win32_ComputerSystem` |
| CPU | AMD Ryzen 5 5600H with Radeon Graphics; 6 physical cores; 12 logical processors; reported max clock 3301 MHz | `Get-CimInstance Win32_Processor` |
| Installed RAM | One Samsung 16 GiB module (`17,179,869,184` bytes), 3200 MT/s; Windows reports `17,024,749,568` usable physical bytes (about 15.86 GiB) | `Get-CimInstance Win32_PhysicalMemory`; `Get-CimInstance Win32_ComputerSystem` |
| Physical disk | `SAMSUNG MZVLB512HBJQ-000L2`; SSD; NVMe; `512,110,190,592` bytes (512.11 GB decimal / about 476.94 GiB); Healthy/OK | `Get-PhysicalDisk`; cross-check with `Get-CimInstance Win32_DiskDrive` |
| Java in current `PATH` | Oracle Java 8 Update 501: `1.8.0_501-b08`, 64-bit HotSpot | `where.exe java`; `java -version` |
| Java used for official runs | Eclipse Temurin OpenJDK `17.0.19+10`, 64-bit | Explicit `...\jdk-17.0.19+10\bin\java.exe -version` |
| Apache JMeter | Apache JMeter `5.6.3` | Temurin 17 executable ran `ApacheJMeter.jar --version` successfully |
| SUT branch | `main`, tracking `origin/main` | `git branch --show-current`; `git status --short --branch` |
| SUT commit | `85af3ba875c88283615e22cb108f13e2fccaf0e9` | `git rev-parse HEAD` |
| SUT commit message | `first upload` | `git log -1 --pretty=format:'%s'` |
| SUT working tree | **Not clean** | `git status --short` output recorded below |

Note: the Windows registry's legacy `ProductName` value reports “Windows 10 Home
Single Language”, but `Win32_OperatingSystem.Caption` reports “Microsoft Windows
11 Home Single Language”. The evidence uses the operating-system caption and
retains the exact build/version values rather than silently accepting the legacy
registry label.

## Java verification

### Java resolved from `PATH`

Command:

```powershell
where.exe java
java -version
```

Observed output:

```text
C:\Program Files (x86)\Common Files\Oracle\Java\java8path\java.exe
java version "1.8.0_501"
Java(TM) SE Runtime Environment (build 1.8.0_501-b08)
Java HotSpot(TM) 64-Bit Server VM (build 25.501-b08, mixed mode)
```

### JDK selected for official JMeter runs

Executable verified:

```text
C:\Users\nguye\.gradle\jdks\eclipse_adoptium-17-amd64-windows\jdk-17.0.19+10\bin\java.exe
```

Command:

```powershell
& 'C:\Users\nguye\.gradle\jdks\eclipse_adoptium-17-amd64-windows\jdk-17.0.19+10\bin\java.exe' -version
```

Observed output:

```text
openjdk version "17.0.19" 2026-04-21
OpenJDK Runtime Environment Temurin-17.0.19+10 (build 17.0.19+10)
OpenJDK 64-Bit Server VM Temurin-17.0.19+10 (build 17.0.19+10, mixed mode, sharing)
```

Temurin 17 is the runtime used for the official runs. The repository's official
run configuration already identifies this JDK, and JMeter 5.6.3 was re-verified
in this collection with that exact executable. Java 8 remains the `PATH` default
but was not used for official runs because earlier initialization with it was
abnormally slow; using the explicit Java 17 path also prevents accidental runtime
selection from changing between runs.

## Apache JMeter verification

Verified files:

```text
C:\Users\nguye\Documents\GitHub\HW05-23127116\.tools\apache-jmeter-5.6.3\bin\jmeter.bat
C:\Users\nguye\Documents\GitHub\HW05-23127116\.tools\apache-jmeter-5.6.3\bin\ApacheJMeter.jar
```

Command executed with the selected official JDK:

```powershell
& 'C:\Users\nguye\.gradle\jdks\eclipse_adoptium-17-amd64-windows\jdk-17.0.19+10\bin\java.exe' `
  -jar 'C:\Users\nguye\Documents\GitHub\HW05-23127116\.tools\apache-jmeter-5.6.3\bin\ApacheJMeter.jar' `
  --version
```

Observed version banner ended with:

```text
Apache JMeter 5.6.3
Copyright (c) 1999-2024 The Apache Software Foundation
```

The command emitted Windows Java Preferences access warnings under the restricted
collection account, but it completed and printed the JMeter 5.6.3 banner. No test
plan was executed.

## EShop SUT Git state

Repository:

```text
C:\Users\nguye\Documents\GitHub\eshop-sut
```

Exact `git status --short --branch` observation:

```text
## main...origin/main
 M backend/database.sqlite
?? GUI_CheckList_ThanhToan.md
?? backend/node_modules/
?? images/
```

Therefore results must be attributed to commit
`85af3ba875c88283615e22cb108f13e2fccaf0e9` **plus the recorded dirty working
tree**, especially the modified runtime database. This collection did not clean,
reset, commit or otherwise change the SUT repository.

## Task Manager screenshot — manual TODO

No Task Manager image was generated or fabricated.

- [v] On the machine above, open **Task Manager → Performance**.
- [v] Capture evidence showing **CPU**, **Memory**, and **Disk**. If one screenshot
      cannot show the needed values legibly, capture one screenshot per tab.
- [v] Keep the hostname or other machine attribution visible where practical.
- [v] Save the original screenshot(s) under `evidence/hardware/`, for example:
      `task-manager-cpu-20260818.png`, `task-manager-memory-20260818.png`, and
      `task-manager-disk-20260818.png`.
- [v] Do not edit utilization values or present a screenshot taken outside the
      relevant run as simultaneous resource evidence.
