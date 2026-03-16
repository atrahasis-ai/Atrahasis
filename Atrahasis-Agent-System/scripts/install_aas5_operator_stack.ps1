param(
    [switch]$Force
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$launcherRoot = Join-Path $repoRoot "runtime\launchers"
New-Item -ItemType Directory -Force -Path $launcherRoot | Out-Null

$wrappers = @(
    @{
        Name = "start-aas5-operator.cmd"
        Body = @"
@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0..\..\scripts\start_aas5_operator_stack.ps1" --open %*
"@
    },
    @{
        Name = "start-aas5-operator-daemon.cmd"
        Body = @"
@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0..\..\scripts\start_aas5_operator_stack.ps1" -Daemon -Open %*
"@
    },
    @{
        Name = "stop-aas5-operator-daemon.cmd"
        Body = @"
@echo off
python "%~dp0..\..\scripts\aas_controller.py" daemon-stop %*
"@
    }
)

foreach ($wrapper in $wrappers) {
    $path = Join-Path $launcherRoot $wrapper.Name
    if ((Test-Path $path) -and -not $Force) {
        continue
    }
    Set-Content -Path $path -Value $wrapper.Body -Encoding ASCII
}

Write-Host "Operator stack launchers are available under $launcherRoot"
