<#
.SYNOPSIS
    RAVEN Frontend Startup Script
.DESCRIPTION
    Starts the RAVEN Vite development server
#>

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

$frontendDir = Join-Path $scriptDir "frontend"

if (-not (Test-Path (Join-Path $frontendDir "node_modules"))) {
    Write-Error "Frontend dependencies not installed. Run setup.ps1 first."
    exit 1
}

Write-Host "Starting RAVEN Frontend..." -ForegroundColor Cyan
Write-Host "Frontend will be available at: http://localhost:5173" -ForegroundColor Gray

Set-Location $frontendDir
npm run dev