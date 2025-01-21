

if (!(Test-Path ".\uv_install.ps1")) {
    curl -o "uv_install.ps1" --proto '=https' --tlsv1.2 -LsSf "https://github.com/astral-sh/uv/releases/download/0.5.18/uv-installer.ps1"    
}
if (!(Test-Path ".\uv_install.ps1")) {    
    Write-Host "uv installer not present."
    exit 1
}
# Install uv
. .\uv_install.ps1
# cleanup after uv install
if (Test-Path ".\uv_install.ps1") {
    Remove-Item uv_install.ps1
}

# reference bin directly in case path is not updated successfully
$uv="$($HOME)\.local\bin\uv.exe"
# Install python version
& $uv init --python 3.12
# Install app requirements
& $uv add -r requirements.txt


