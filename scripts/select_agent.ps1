param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("public_baseline", "official_starter")]
    [string]$Name
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Source = Join-Path $Root "agents\$Name\main.py"
$Target = Join-Path $Root "main.py"
Copy-Item -LiteralPath $Source -Destination $Target -Force
Write-Host "Selected agent: $Name"
Write-Host "main.py: $Target"

