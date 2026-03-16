param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 4180,
    [switch]$Daemon,
    [switch]$Open
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = "python"
$scriptPath = Join-Path $repoRoot "scripts\aas_controller.py"

if ($Daemon) {
    $argsList = @(
        $scriptPath
        "daemon-start"
        "--host", $Host
        "--port", "$Port"
    )
    & $python @argsList
    if ($Open) {
        Start-Process "http://$Host`:$Port/operator/"
    }
    exit $LASTEXITCODE
}

$argsList = @(
    $scriptPath
    "serve"
    "--host", $Host
    "--port", "$Port"
)
if ($Open) {
    $argsList += "--open"
}

& $python @argsList
exit $LASTEXITCODE
