param(
    [switch]$Rebuild,
    [switch]$BuildSfos,
    [switch]$BuildWorker,
    [switch]$BuildExe,
    [switch]$BuildEverything
    )

function ConvertTo-Icon {
  param(
    [Parameter(Mandatory=$true)]
    $imagePath,
    $iconPath = "$env:temp\newicon.ico"
  )

    Add-Type -AssemblyName System.Drawing
    if (Test-Path $imagePath) {
        #$image_ext = [System.IO.Path]::GetExtension($imagePath)
        $image = [System.Drawing.Image]::FromFile($imagePath)
        $icon = [System.Drawing.Icon]::FromHandle($image.GetHicon())
        $stream = New-Object System.IO.FileStream($iconPath, [System.IO.FileMode]::Create)
        $icon.Save($stream)
        $stream.Close()
        $icon.Dispose()
        $image.Dispose()
        
        # explorer "/SELECT,$iconpath"
    } else { Write-Warning "$imagePath does not exist" }
    }

function IncrementVersion {    
    param(
        [Parameter(Mandatory=$true)]
        [string]$FilePath,
        [switch]$UseDate,
        [string]$SuffixOverride
    )

    # Regex pattern to capture the version line with groups:
    # - prefix: beginning of the version string (including __version__ = ")
    # - major, minor, patch: the numeric version segments
    # - suffix: any trailing characters before the closing quote
    $regex = '^(?<prefix>__version__\s*=\s*")(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)(?<suffix>[^"]*)(")'
    $content = Get-Content -Path $FilePath
    $newContent = $content | ForEach-Object {
        if ($_ -match $regex) {
            # Determine major and minor segments based on the flag
            if ($UseDate) {
                $newMajor = (Get-Date -Format "yyyy")
                $newMinor = (Get-Date -Format "MM")
            }
            else {
                $newMajor = $Matches['major']
                $newMinor = $Matches['minor']
            }

            # Increment the patch segment
            $newPatch = [int]$Matches['patch'] + 1

            # Use the override suffix if provided; otherwise, use the captured suffix
            if ($SuffixOverride) {
                $newSuffix = $SuffixOverride
            }
            else {
                $newSuffix = $Matches['suffix']
            }

            # Rebuild the version line
            $newLine = $Matches['prefix'] + $newMajor + '.' + $newMinor + '.' + $newPatch + $newSuffix + '"'            
            $newLine
        }
        else {
            $_
        }
    }

    if (-not ($content -eq $newContent)) {
        Set-Content -Path $FilePath -Value $newContent
        Write-Host "Version updated successfully."
    }
    else {
        Write-Host "Version string not found in the file: '$($FilePath)'"
    }
}

function Get-Version {    
    param(
        [Parameter(Mandatory=$true)]
        [string]$FilePath
    )

    # Regex to match the version line and capture the major, minor, patch and any trailing characters.
    $regex = '^(?<prefix>__version__\s*=\s*")(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)(?<suffix>[^"]*)(")'

    # Read the file content
    $content = Get-Content -Path $FilePath

    foreach ($line in $content) {
        if ($line -match $regex) {
            # Construct the version string from the captured groups
            $version = $Matches['major'] + '.' + $Matches['minor'] + '.' + $Matches['patch'] + $Matches['suffix']
            return $version
        }
    }

    Write-Warning "Version string not found in file."
}

function Update-VSVersionInfo {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$SourceFile,
        [Parameter(Mandatory=$true)]
        [string]$TargetFile
    )

    # Extract version from the source file (expects format: __version__ = "major.minor.patch[...]" )
    $versionRegex = '^(?<prefix>__version__\s*=\s*")(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)(?<suffix>[^"]*)(")'
    $sourceContent = Get-Content -Path $SourceFile
    $extractedVersion = $null

    foreach ($line in $sourceContent) {
        if ($line -match $versionRegex) {
            $extractedVersion = "$($Matches['major']).$($Matches['minor']).$($Matches['patch'])"
            break
        }
    }

    if (-not $extractedVersion) {
        Write-Host "Version string not found in source file."
        return
    }

    # Split extracted version into parts
    $versionParts = $extractedVersion -split '\.'
    $major = $versionParts[0]
    $minor = $versionParts[1]
    $patch = $versionParts[2]

    # New version tuple string for updates
    $newTuple = "$major, $minor, $patch, 0"

    # Read target file content
    $targetContent = Get-Content -Path $TargetFile

    $updatedContent = $targetContent | ForEach-Object {
        $line = $_

        # Update filevers tuple (e.g., filevers=(96, 12, 19, 1),)
        $line = $line -replace 'filevers=\([^)]*\)(,?)', "filevers=($newTuple),"

        # Update prodvers tuple (e.g., prodvers=(4, 1, 2, 1),)
        $line = $line -replace 'prodvers=\([^)]*\)(,?)', "prodvers=($newTuple),"

        # Update ProductVersion in StringStruct (e.g., StringStruct(u'ProductVersion', u'2, 0, 3, 0'),)
        
        $line = $line -replace "(StringStruct\(\s*u'ProductVersion'\s*,\s*u')[^']+(')(,?)", "StringStruct( u'ProductVersion' u'$newTuple'"

        # Update FileVersion in StringStruct (e.g., StringStruct(u'FileVersion', u'96, 12, 19, 1'),)
        $line = $line -replace "(StringStruct\(\s*u'FileVersion'\s*,\s*u')[^']+(')(,?)", "StringStruct( u'FileVersion' u'$newTuple'"

        $line
    }

    # Write updated content back to the target file
    Set-Content -Path $TargetFile -Value $updatedContent
    Write-Host "VSVersionInfo updated with version ($newTuple)"
}

function Get-LatestWheel {
    # Fetch the name of the latest wheel package to include in exe
    $wheel_path = ".\sfos\dist\"
    $pattern = "sgc_worker-*.whl"
    $latest_wheel = Get-ChildItem -Path $wheel_path -Filter $pattern | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1

    if ($latest_wheel) {
        $latest_wheel = "sfos\dist\$($latest_wheel.Name)"
        return $latest_wheel
    } else {
        return
    }
}

# Cleanup any leftovers in build folder
if (test-path ".\dist") {
    Remove-Item ".\dist" -Recurse -Force -Confirm:$false
}

# Save existing copy under previous version 
if (test-path ".\gccli.exe") { remove-Item ".\gccli.exe" }

if (($BuildSfos) -or ($BuildEverything) ) {

    # make sure dev requirements are installed before running build process
    remove-item pyproject.toml
    copy-item pyproject_init.toml pyproject.toml

    & uv add -r requirements.txt
    & uv add -r requirements_dev.txt --dev
    & uv build sfos
}

if ( ($BuildWorker) -or ($BuildEverything) ) {
    $versionFile = ".\sfos\__init__.py"
    if ( -not $Rebuild ) { IncrementVersion $versionFile }
    # update the dependency and rebuild with the new version
    & uv add "sgc-worker@./sfos/" --upgrade-package sgc-worker
    & uv build .
}
if (($BuildExe) -or ($BuildEverything) ) {
    $versionFile = ".\sfos\agent\__init__.py"
    $iconFile = "./make/gclogo.ico"
    $vsversionFile = ".\make\exe_version.txt"
    $buildTarget = ".\sfos\dist\gccli.exe"
    $current_version = Get-Version($versionFile)
    $newTarget = ".\gccli.$($current_version).exe"
    $finalTarget = ".\gccli.exe"

    
    if ( -not $Rebuild ) { 
        IncrementVersion $versionFile -UseDate -SuffixOverride "-pre" 
        Update-VSVersionInfo $versionFile $vsversionFile
    }
    # Create gccli.exe
    & uv run pyinstaller -F gccli.py --icon $iconFile # -version-file=$vsversionFile
    # & uv run pyinstaller -F gccli.py --icon ./make/gclogo.ico -version-file=".\make\exe_version.txt" 
    # Move compiled exe into root folder
    
    if (test-path $buildTarget) {        
        Move-Item -Path $buildTarget -destination $newTarget
        Copy-Item -Path $newTarget -Destination $finalTarget
        Write-Host "Done. The contents of dist may be copied as a standalone application."
    } else {
        write-error "Build failed. check output for reason."
    }
}

# reset toml file
remove-item pyproject.toml
copy-item pyproject_init.toml pyproject.toml
