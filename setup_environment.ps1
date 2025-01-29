$location="~\.local\bin"
$exesInstalled=((Test-Path -Path "$($location)\uv.exe") -and (Test-Path -Path "$($location)\uvx.exe"))
$targetpath=Resolve-Path $location
$pathSet=$env:Path -split ";" -contains $targetpath
$uvReady=($exesInstalled -and $pathSet)

if ($uvReady) {
    if (Test-Path -Path "pyproject.toml") {
        remove-item pyproject.toml        
    }
    copy-item pyproject_init.toml pyproject.toml
    & uv add -r requirements.txt
} else {
    write-error "Environment manager not installed. Install uv to continue"
}

