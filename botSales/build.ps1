$exclude = @("venv", "botSales.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "botSales.zip" -Force