$largeFiles = Get-Content large_files.txt
foreach ($file in $largeFiles) {
    git rm --cached $file
    git add $file
}

git commit -m "Add all large files using Git LFS"


# powershell -ExecutionPolicy Bypass -File .\add_large_files.ps1
