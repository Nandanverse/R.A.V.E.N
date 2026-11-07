<#
.SYNOPSIS
    RAVEN Startup Script - Starts both backend and frontend
.DESCRIPTION
    Starts the RAVEN backend (FastAPI) and frontend (Vite dev server) in separate windows.
#>

param(
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

$venvPath = Join-Path $scriptDir "backend\.venv"
$backendDir = Join-Path $scriptDir "backend"
$frontendDir = Join-Path $scriptDir "frontend"

if (-not (Test-Path $venvPath)) {
    Write-Error "Virtual environment not found. Run setup.ps1 first."
    exit 1
}

function Start-Backend {
    Write-Host "Starting RAVEN Backend..." -ForegroundColor Cyan
    $python = Join-Path $venvPath "Scripts\python.exe"
    Start-Process -FilePath $python -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory $backendDir -WindowStyle Normal
}

function Start-Frontend {
    Write-Host "Starting RAVEN Frontend..." -ForegroundColor Cyan
    Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory $frontendDir -WindowStyle Normal
}

if ($BackendOnly) {
    Start-Backend
} elseif ($FrontendOnly) {
    Start-Frontend
} else {
    Start-Backend
    Start-Sleep -Seconds 3
    Start-Frontend
    Write-Host "`nRAVEN is starting up!" -ForegroundColor Green
    Write-Host "Backend:  http://localhost:8000" -ForegroundColor Gray
    Write-Host "Frontend: http://localhost:5173" -ForegroundColor Gray
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Gray
}