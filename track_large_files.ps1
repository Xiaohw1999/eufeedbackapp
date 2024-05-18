$largeFiles = Get-Content large_files.txt
foreach ($file in $largeFiles) {
    git lfs track $file
}

git add .gitattributes
git commit -m "Track all large files with Git LFS"

# powershell -ExecutionPolicy Bypass -File .\track_large_files.ps1
