# Application Archiving Guide

## Purpose
Timestamped snapshots in `archive/` give a local restore point before risky
changes. They are git-ignored to keep the repository lean.

## Naming
`archive/YYYY-MM-DD_HHmmss/` (e.g. `archive/2026-06-19_143022/`).

## Create a snapshot
- Unix/macOS: `./archive-project.sh`
- Windows: `.\archive-project.ps1`

Excludes `.git/`, `archive/`, `.venv/`, `__pycache__/`, `node_modules/`, build output.

## Restore
```powershell
Copy-Item -Path "archive\<timestamp>\*" -Destination "." -Recurse -Force
```

## Cleanup
```powershell
# keep only the last 5 snapshots
Get-ChildItem archive\ | Sort-Object CreationTime | Select-Object -SkipLast 5 | Remove-Item -Recurse
```
