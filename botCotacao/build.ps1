$exclude = @("venv", "botCotacao.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "botCotacao.zip" -Force