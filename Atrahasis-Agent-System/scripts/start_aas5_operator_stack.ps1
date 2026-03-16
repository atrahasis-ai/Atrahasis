param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 4180,
    [string]$AppServerUrl = "ws://127.0.0.1:8765",
    [string]$CodexExecutable,
    [switch]$Daemon,
    [switch]$Open,
    [switch]$NoAppServer
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
        "--app-server-url", $AppServerUrl
    )
    if ($CodexExecutable) {
        $argsList += @("--codex-executable", $CodexExecutable)
    }
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
    "--app-server-url", $AppServerUrl
)
if ($Open) {
    $argsList += "--open"
}
if ($NoAppServer) {
    $argsList += "--no-app-server"
}
if ($CodexExecutable) {
    $argsList += @("--codex-executable", $CodexExecutable)
}

& $python @argsList
exit $LASTEXITCODE
