<#
.SYNOPSIS
    RAVEN Backend Startup Script
.DESCRIPTION
    Starts the RAVEN FastAPI backend server
#>

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

$venvPath = Join-Path $scriptDir "backend\.venv"
$backendDir = Join-Path $scriptDir "backend"

if (-not (Test-Path $venvPath)) {
    Write-Error "Virtual environment not found. Run setup.ps1 first."
    exit 1
}

$python = Join-Path $venvPath "Scripts\python.exe"
Write-Host "Starting RAVEN Backend..." -ForegroundColor Cyan
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Gray
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Gray

& $python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload