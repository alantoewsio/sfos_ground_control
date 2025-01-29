$location="~\.local\bin"
$exesInstalled=((Test-Path -Path "$($location)\uv.exe") -and (Test-Path -Path "$($location)\uvx.exe"))
$uvReady=($exesInstalled -and $pathSet)



$targetpath=Resolve-Path $location
$pathSet=$env:Path -split ";" -contains $targetpath
$newPath = (($env:Path + ";$($targetpath)" -split ";") | Sort-Object | Get-Unique) -join ";"
if (-not $pathSet) {
    $env:Path = $newPath
    [Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::User)    
    $pathSet=$env:Path -split ";" -contains $targetpath
}
$uvReady=($exesInstalled -and $pathSet)

if ((-not $uvReady) -and (-not (Test-Path ".\uv_install.ps1"))) {
    curl -o "downloaded_uv_install.ps1" --proto '=https' --tlsv1.2 -LsSf "https://github.com/astral-sh/uv/releases/download/0.5.18/uv-installer.ps1"    
}
if (!(Test-Path ".\downloaded_uv_install.ps1")) {    
    Write-Host "uv installer not present."
    exit 1
}
# Install uv
. .\downloaded_uv_install.ps1

# Check if installation completed
$exesInstalled=((Test-Path -Path "$($location)\uv.exe") -and (Test-Path -Path "$($location)\uvx.exe"))
$uvReady=($exesInstalled -and $pathSet)

# cleanup 
if (Test-Path ".\downloaded_uv_install.ps1") {
    Remove-Item downloaded_uv_install.ps1
}