param(
    [switch]$Search,
    [switch]$Alpha,
    [switch]$CodeMode,
    [switch]$MultiAgent,
    [switch]$NoMultiAgent,
    [string[]]$ExtraArgs
)

function Add-RipgrepToPath {
    $candidates = @()
    if ($env:APPDATA) {
        $candidates += Join-Path $env:APPDATA "npm\node_modules\@openai\codex\node_modules\@openai\codex-win32-x64\vendor"
    }
    if ($env:LOCALAPPDATA) {
        $candidates += Join-Path $env:LOCALAPPDATA "npm-cache"
    }

    foreach ($root in $candidates) {
        if (-not (Test-Path $root)) {
            continue
        }
        $rg = Get-ChildItem -Path $root -Recurse -Filter "rg.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -eq $rg) {
            continue
        }
        $rgDir = $rg.Directory.FullName
        $pathParts = @($env:PATH -split ';') | Where-Object { $_ }
        if ($pathParts -notcontains $rgDir) {
            $env:PATH = "$rgDir;$env:PATH"
        }
        return $rg.FullName
    }
    return $null
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$runner = if ($Alpha) { "codex-alpha" } else { "codex" }
$argsList = @("--no-alt-screen", "-C", $repoRoot)
$multiAgentEnabled = $MultiAgent -or (-not $NoMultiAgent)
$null = Add-RipgrepToPath

if ($Search) {
    $argsList += "--search"
}
if ($CodeMode) {
    $argsList += @("--enable", "code_mode")
}
if ($multiAgentEnabled) {
    $argsList += @("--enable", "multi_agent")
}
if ($ExtraArgs) {
    $argsList += $ExtraArgs
}

& $runner @argsList
$LASTEXITCODE
