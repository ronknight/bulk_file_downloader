# Archive the project into a timestamped snapshot under archive\.
# Usage: .\archive-project.ps1

$ProjectPath = Get-Location
$ArchivePath = Join-Path $ProjectPath "archive"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$ArchiveFolder = Join-Path $ArchivePath $Timestamp

if (-not (Test-Path $ArchivePath)) { New-Item -ItemType Directory -Path $ArchivePath -Force | Out-Null }
if (Test-Path $ArchiveFolder) { Write-Host "Archive already exists: $ArchiveFolder"; exit 1 }
New-Item -ItemType Directory -Path $ArchiveFolder -Force | Out-Null

$ExcludePatterns = @(".git", "archive", ".venv", "__pycache__", ".pyc", ".DS_Store", "node_modules", "target", "build", "dist")
$totalItems = 0
foreach ($item in Get-ChildItem -Force) {
    if ($ExcludePatterns -contains $item.Name) { continue }
    $destination = Join-Path $ArchiveFolder $item.Name
    if ($item.PSIsContainer) {
        Copy-Item -Path $item.FullName -Destination $destination -Recurse -Force
    } else {
        Copy-Item -Path $item.FullName -Destination $destination -Force
    }
    $totalItems++
}
Write-Host "Archive created at: $ArchiveFolder ($totalItems items)"
