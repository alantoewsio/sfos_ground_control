# Cleanup any leftovers in build folder
if (verify-path ".\dist") {
    Remove-Item ".\dist" -Recurse -Force -Confirm:$false
}
if (verify-path ".\gccli.exe") {
    Remove-Item ".\gccli.exe" -Recurse -Force -Confirm:$false
}
# make sure dev requirements are installed before running build process
remove-item pyproject.toml
copy-item pyproject_init.toml pyproject.toml

& uv add -r requirements_dev.txt --dev

# Create wheel binary
& uv build sfos
# link the wheel binary in the root project

& uv remove sgc_worker
& uv add sfos\dist\sgc_worker-1.0.0-py3-none-any.whl
# Create gccli.exe
& uv run pyinstaller -F gccli.py

# Move compiled exe into root folder
if (verify-path ".\dist\gccli.exe") {
    Move-Item -Path dist\gccli.exe -destination .
    Write-Host "Done. The contents of dist may be copied as a standalone application."
} else {
    write-error "Build failed. check output for reason."
}

remove-item pyproject.toml
copy-item pyproject_init.toml pyproject.toml
