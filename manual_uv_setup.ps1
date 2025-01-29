$location="~\.local\bin"
$exesFound=((Test-Path -Path "~\downloads\uv.exe") -and (Test-Path -Path "~\downloads\uvx.exe"))
$exesInstalled=((Test-Path -Path "$($location)\uv.exe") -and (Test-Path -Path "$($location)\uvx.exe"))


if ($exesFound -and (-not $exesInstalled)) {
    mkdir $location -Force
    cp ~\downloads\uv.exe,~\downloads\uvx.exe $location        
    $exesInstalled=((Test-Path -Path "$($location)\uv.exe") -and (Test-Path -Path "$($location)\uvx.exe"))
} 

$targetpath=Resolve-Path $location
$pathSet=$env:Path -split ";" -contains $targetpath
$uvReady=($exesInstalled -and $pathSet)
$newPath = (($env:Path + ";$($targetpath)" -split ";") | Sort-Object | Get-Unique) -join ";"
if (-not $pathSet) {
    $env:Path = $newPath
    [Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::User)    
    $pathSet=$env:Path -split ";" -contains $targetpath
}
$uvReady=($exesInstalled -and $pathSet)
if ($uvReady) {
    Write-Host "UV is installed and ready."
    try {
        & uv --version
    } catch {
        Write-Error "uv failed to run. Check that the correct binaries are installed for this machine."
        Remove-Item "$($location)\uv.exe"
    }
    try {
        & uvx --version
    } catch {
        Write-Error "uv failed to run. Check that the correct binaries are installed for this machine."
        Remove-Item "$($location)\uvx.exe"
    }
} elseif (-not $exesFound) {
    Write-Error "Install Error: uv binaries not available and not already installed." 
    Write-Error "Current platform: Windows $($env:PROCESSOR_ARCHITECTURE)"
    Write-Error "Download from https://github.com/astral-sh/uv/releases" 
    Write-Error "Then extract exe files and place them in your downloads folder."   
} elseif (-not (Test-Path $location)) {
    Write-Error "Install Error: Unable to create target path $($location)" 
} elseif (-not $exesInstalled) {
    Write-Error "Install Error: Unable to place uv.exe and uvx.exe in $($location)"
} elseif (-not $pathSet) {
    Write-Error "Install Error: Unable to add '$($location)' to Path environment variable"
    Write-Error "Current platform: Windows $($env:PROCESSOR_ARCHITECTURE)"
    Write-Error "Download the correct versions from https://github.com/astral-sh/uv/releases" 
    Write-Error "Then extract exe files and place them in your downloads folder."
}

