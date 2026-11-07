# RAVEN Setup Script for Windows
# Installs and configures RAVEN (Risk-Aware Autonomous Vulnerability Exploration Network)

param(
    [switch]$SkipDocker,
    [switch]$SkipOllama,
    [switch]$Minimal,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# Colors for output
$Green = ""
$Red = ""
$Yellow = ""
$Blue = ""
$Reset = ""

function Write-Color($Message, $Color) {
    Write-Host "$Color$Message$Reset"
}

function Write-Success($Message) { Write-Color "[OK] $Message" $Green }
function Write-Error($Message) { Write-Color "[FAIL] $Message" $Red }
function Write-Warning($Message) { Write-Color "[WARN] $Message" $Yellow }
function Write-Info($Message) { Write-Color "[INFO] $Message" $Blue }
function Write-Header($Message) { Write-Color "`n=== $Message ===" $Blue }

# Check if running as Administrator
function Test-Admin {
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check if command exists
function Test-Command($Command) {
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Check if Docker is running
function Test-Docker {
    try {
        docker version --format "{{.Server.Version}}" 2>$null | Out-Null
        return $true
    } catch {
        return $false
    }
}

Write-Header "RAVEN Setup - Risk-Aware Autonomous Vulnerability Exploration Network"
Write-Info "Project: https://github.com/nandanamin/RAVEN"
Write-Info "Author: Nandan Amin"

# Check Administrator
if (-not (Test-Admin)) {
    Write-Warning "Not running as Administrator. Some operations may require elevation."
}

# Track setup status
$setupStatus = @{
    Python = $false
    Node = $false
    Git = $false
    Docker = $false
    Ollama = $false
    Nmap = $false
    Zap = $false
    Venv = $false
    PyDeps = $false
    NodeDeps = $false
    Config = $false
    Database = $false
    Migrations = $false
    HealthCheck = $false
}

Write-Header "Checking Prerequisites"

# Python
Write-Info "Checking Python..."
if (Test-Command "python") {
    $pyVersion = python --version 2>&1
    if ($pyVersion -match "Python 3\.(1[0-9]|[2-9][0-9])") {
        Write-Success "Found: $pyVersion"
        $setupStatus.Python = $true
    } else {
        Write-Error "Python 3.10+ required. Found: $pyVersion"
    }
} else {
    Write-Error "Python not found. Install from https://python.org or use: winget install Python.Python.3.12"
}

# Node.js
Write-Info "Checking Node.js..."
if (Test-Command "node") {
    $nodeVersion = node --version
    if ($nodeVersion -match "v(1[8-9]|[2-9][0-9])\.") {
        Write-Success "Found: $nodeVersion"
        $setupStatus.Node = $true
    } else {
        Write-Error "Node.js 18+ required. Found: $nodeVersion"
    }
} else {
    Write-Error "Node.js not found. Install from https://nodejs.org or use: winget install OpenJS.NodeJS"
}

# Git
Write-Info "Checking Git..."
if (Test-Command "git") {
    $gitVersion = git --version
    Write-Success "Found: $gitVersion"
    $setupStatus.Git = $true
} else {
    Write-Error "Git not found. Install from https://git-scm.com or use: winget install Git.Git"
}

# Docker
if (-not $SkipDocker) {
    Write-Info "Checking Docker..."
    if (Test-Command "docker") {
        $dockerVersion = docker --version
        Write-Success "Found: $dockerVersion"
        if (Test-Docker) {
            Write-Success "Docker daemon is running"
            $setupStatus.Docker = $true
        } else {
            Write-Warning "Docker installed but daemon not running. Start Docker Desktop."
        }
    } else {
        Write-Warning "Docker not found. Install Docker Desktop from https://docker.com"
    }
} else {
    Write-Info "Skipping Docker check (--SkipDocker)"
    $setupStatus.Docker = $true
}

# Ollama
if (-not $SkipOllama) {
    Write-Info "Checking Ollama..."
    if (Test-Command "ollama") {
        $ollamaVersion = ollama --version
        Write-Success "Found: $ollamaVersion"
        $setupStatus.Ollama = $true
    } else {
        Write-Warning "Ollama not found. Install from https://ollama.ai or use: winget install Ollama.Ollama"
        Write-Info "After installing Ollama, run: ollama pull llama3.1:8b"
    }
} else {
    Write-Info "Skipping Ollama check (--SkipOllama)"
    $setupStatus.Ollama = $true
}

# Nmap
Write-Info "Checking Nmap..."
if (Test-Command "nmap") {
    $nmapVersion = nmap --version | Select-Object -First 1
    Write-Success "Found: $nmapVersion"
    $setupStatus.Nmap = $true
} else {
    Write-Warning "Nmap not found. Install from https://nmap.org or use: winget install Nmap.Nmap"
    if (-not $Minimal) { Write-Info "Nmap is required for reconnaissance functionality" }
}

# OWASP ZAP
Write-Info "Checking OWASP ZAP..."
if (Test-Command "zap.sh") {
    Write-Success "Found: zap.sh in PATH"
    $setupStatus.Zap = $true
} elseif (Test-Path "C:\Program Files\OWASP\Zed Attack Proxy\zap.bat") {
    Write-Success "Found: ZAP installed at default location"
    $setupStatus.Zap = $true
} else {
    Write-Warning "OWASP ZAP not found. Download from https://www.zaproxy.org/download/"
    if (-not $Minimal) { Write-Info "ZAP is required for web application scanning" }
}

# Check critical prerequisites
$criticalFailed = @()
if (-not $setupStatus.Python) { $criticalFailed += "Python" }
if (-not $setupStatus.Node) { $criticalFailed += "Node.js" }
if (-not $setupStatus.Git) { $criticalFailed += "Git" }

if ($criticalFailed.Count -gt 0) {
    Write-Error "Critical prerequisites missing: $($criticalFailed -join ', ')"
    Write-Info "Please install missing prerequisites and run setup again."
    exit 1
}

Write-Header "Creating Python Virtual Environment"

$venvPath = Join-Path $scriptDir "backend\.venv"
if ((Test-Path $venvPath) -and (-not $Force)) {
    Write-Warning "Virtual environment already exists at $venvPath"
    Write-Info "Use -Force to recreate"
    $setupStatus.Venv = $true
} else {
    try {
        if (Test-Path $venvPath) { Remove-Item $venvPath -Recurse -Force }
        python -m venv $venvPath
        Write-Success "Virtual environment created at $venvPath"
        $setupStatus.Venv = $true
    } catch {
        Write-Error "Failed to create virtual environment: $_"
        exit 1
    }
}

Write-Header "Installing Python Dependencies"

$pipPath = Join-Path $venvPath "Scripts\pip.exe"
$reqPath = Join-Path $scriptDir "backend\requirements.txt"

if (Test-Path $reqPath) {
    try {
        & $pipPath install -r $reqPath *>$null
        Write-Success "Python dependencies installed"
        $setupStatus.PyDeps = $true
    } catch {
        Write-Error "Failed to install Python dependencies: $_"
        exit 1
    }
} else {
    Write-Error "requirements.txt not found at $reqPath"
    exit 1
}

Write-Header "Installing Frontend Dependencies"

$frontendDir = Join-Path $scriptDir "frontend"
if (Test-Path $frontendDir) {
    Set-Location $frontendDir
    try {
        npm install
        Write-Success "Frontend dependencies installed"
        $setupStatus.NodeDeps = $true
    } catch {
        Write-Error "Failed to install frontend dependencies: $_"
        exit 1
    }
    Set-Location $scriptDir
} else {
    Write-Error "Frontend directory not found"
    exit 1
}

Write-Header "Creating Configuration"

$envExample = Join-Path $scriptDir ".env.example"
$envFile = Join-Path $scriptDir ".env"

if ((Test-Path $envFile) -and (-not $Force)) {
    Write-Warning ".env already exists. Skipping creation."
    Write-Info "Use -Force to overwrite"
    $setupStatus.Config = $true
} elseif (Test-Path $envExample) {
    try {
        Copy-Item $envExample $envFile -Force
        Write-Success "Created .env from template"
        Write-Warning "IMPORTANT: Edit .env and set SECRET_KEY and other sensitive values!"
        $setupStatus.Config = $true
    } catch {
        Write-Error "Failed to create .env: $_"
        exit 1
    }
} else {
    Write-Error ".env.example not found"
    exit 1
}

Write-Header "Initializing Database"

if ($setupStatus.Docker) {
    Write-Info "Starting PostgreSQL and Redis via Docker Compose..."
    try {
        docker compose up -d postgres redis
        Write-Success "Database services started"

        # Wait for PostgreSQL to be ready
        Write-Info "Waiting for PostgreSQL to be ready..."
        $maxAttempts = 30
        $attempt = 0
        while ($attempt -lt $maxAttempts) {
            try {
                docker exec raven-postgres pg_isready -U raven -d raven 2>$null | Out-Null
                Write-Success "PostgreSQL is ready"
                break
            } catch {
                Start-Sleep -Seconds 2
                $attempt++
            }
        }
        if ($attempt -ge $maxAttempts) {
            Write-Error "PostgreSQL did not become ready in time"
            exit 1
        }

        $setupStatus.Database = $true
    } catch {
        Write-Error "Failed to start database services: $_"
        exit 1
    }
} else {
    Write-Warning "Docker not available. Skipping database initialization."
    Write-Info "Ensure PostgreSQL is running on localhost:5432 with database 'raven'"
    Write-Info "Connection string: postgresql+asyncpg://raven:raven@localhost:5432/raven"
    $setupStatus.Database = $true
}

Write-Header "Running Database Migrations"

if ($setupStatus.Database) {
    Set-Location (Join-Path $scriptDir "backend")
    try {
        & (Join-Path $venvPath "Scripts\python.exe") -m alembic upgrade head
        Write-Success "Database migrations completed"
        $setupStatus.Migrations = $true
    } catch {
        Write-Error "Failed to run migrations: $_"
        exit 1
    }
    Set-Location $scriptDir
}

Write-Header "Health Checks"

# Backend health check
if ($setupStatus.Migrations) {
    Write-Info "Testing backend startup..."
    try {
        $backendDir = Join-Path $scriptDir "backend"
        $proc = Start-Process -FilePath (Join-Path $venvPath "Scripts\python.exe") `
            -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8001" `
            -WorkingDirectory $backendDir `
            -PassThru -WindowStyle Hidden

        Start-Sleep -Seconds 5

        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/health" -TimeoutSec 10 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "Backend health check passed"
                $setupStatus.HealthCheck = $true
            } else {
                Write-Warning "Backend returned status $($response.StatusCode)"
            }
        } catch {
            Write-Warning "Backend health endpoint not reachable"
        } finally {
            Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        }
    } catch {
        Write-Warning "Could not test backend startup: $_"
    }
}

Write-Header "Setup Summary"

$passed = ($setupStatus.Values | Where-Object { $_ -eq $true }).Count
$total = $setupStatus.Count
Write-Info "Steps completed: $passed / $total"

foreach ($step in $setupStatus.Keys) {
    $status = if ($setupStatus[$step]) { "[OK]" } else { "[FAIL]" }
    $color = if ($setupStatus[$step]) { $Green } else { $Red }
    Write-Color "  $status $step" $color
}

if ($passed -eq $total) {
    Write-Success "`nSetup completed successfully!"
} else {
    Write-Warning "`nSetup completed with some optional components missing."
    Write-Info "Missing optional components will limit functionality but core features will work."
}

Write-Header "Next Steps"

Write-Info "1. Edit .env file and configure:"
Write-Info "   - SECRET_KEY (generate with: python -c \"import secrets; print(secrets.token_hex(32))\")"
Write-Info "   - OLLAMA_MODEL (default: llama3.1:8b)"
Write-Info "   - DATABASE_URL if using external PostgreSQL"

Write-Info "`n2. Start Ollama and pull model (if not done):"
Write-Info "   ollama serve"
Write-Info "   ollama pull llama3.1:8b"

Write-Info "`n3. Start the application:"
Write-Info "   Backend:  .\start-backend.ps1"
Write-Info "   Frontend: .\start-frontend.ps1"
Write-Info "   Or use:   .\start.ps1 (starts both)"

Write-Info "`n4. Access the application:"
Write-Info "   Frontend: http://localhost:5173"
Write-Info "   Backend API: http://localhost:8000"
Write-Info "   API Docs: http://localhost:8000/docs"

Write-Info "`n5. Create your first assessment:"
Write-Info "   - Go to Settings > Scopes and define authorized targets"
Write-Info "   - Go to Assessments and create a new assessment"
Write-Info "   - Select scope and start reconnaissance"

Write-Info "`nDocumentation: See docs/ directory for detailed guides"