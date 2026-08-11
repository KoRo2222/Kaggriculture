$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (Get-Command conda -ErrorAction SilentlyContinue) {
    conda env update -f environment.yml --prune
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create/update the conda environment."
    }
    Write-Host "Activate with: conda activate kagri"
    exit 0
}

if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.12 -m venv .venv
    } else {
        python -m venv .venv
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the Python virtual environment. Python 3.12 is recommended."
    }
}
& ".venv\Scripts\python.exe" -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "Failed to upgrade pip."
}
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install project dependencies."
}
Write-Host "Activate with: .\.venv\Scripts\Activate.ps1"
