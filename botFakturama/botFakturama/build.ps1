$exclude = @("venv", "botFakturama.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "botFakturama.zip" -Force