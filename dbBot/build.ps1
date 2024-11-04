$exclude = @("venv", "botDemo.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "botDemo.zip" -Force