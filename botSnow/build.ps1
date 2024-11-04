$exclude = @("venv", "botSnow.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "botSnow.zip" -Force