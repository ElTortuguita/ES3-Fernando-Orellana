$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonProyecto = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonProyecto)) {
    $pythonProyecto = Join-Path $PSScriptRoot '..\..\work\venv-aventuras\Scripts\python.exe'
}
if (-not (Test-Path -LiteralPath $pythonProyecto)) {
    throw 'Primero instala el entorno siguiendo README.txt.'
}
& $pythonProyecto manage.py runserver 127.0.0.1:8013
