$ErrorActionPreference = 'Stop'

$python = Get-Command py -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Error 'Could not find Python. Install Python 3 and try again.'
}

Write-Host 'Creating virtual environment...'
if ($python.Name -eq 'py') {
    py -m venv .venv
} else {
    python -m venv .venv
}

Write-Host 'Upgrading pip...'
& .\.venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host 'Installing Python dependencies...'
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpeg) {
    Write-Host 'FFmpeg detected. Editor audio import/conversion should work.'
} else {
    Write-Host 'FFmpeg not found. That is okay if you only want to play included songs.'
    Write-Host 'Install FFmpeg later if you want to import audio in the editor.'
}

Write-Host ''
Write-Host 'Setup complete.'
Write-Host 'Next steps:'
Write-Host '  .\.venv\Scripts\Activate.ps1'
Write-Host '  python main.py'
