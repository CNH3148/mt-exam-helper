$hema_db = Get-ChildItem "app\data\*.json" | Where-Object { $_.Name -match "血液" -and $_.Name -notmatch "topics" -and $_.Name -notmatch "taxonomy" } | Select-Object -ExpandProperty FullName -First 1
$hema_topics = Get-ChildItem "app\data\topics_*.json" | Where-Object { $_.Name -match "血液" } | Select-Object -ExpandProperty FullName -First 1

$data = Get-Content $hema_db -Encoding UTF8 -Raw | ConvertFrom-Json
$topics = Get-Content $hema_topics -Encoding UTF8 -Raw | ConvertFrom-Json
$known = $topics.psobject.properties.name
$missing = $data | Where-Object { $null -ne $_.topic -and "" -ne $_.topic -and $_.topic -notin $known }
Write-Output "--- HEMA ---"
$missing | Group-Object topic | Sort-Object Count -Descending | Select-Object Count, Name | Format-Table -HideTableHeaders

$mol_db = Get-ChildItem "app\data\*.json" | Where-Object { $_.Name -match "分子" -and $_.Name -notmatch "topics" -and $_.Name -notmatch "taxonomy" } | Select-Object -ExpandProperty FullName -First 1
$mol_topics = Get-ChildItem "app\data\topics_*.json" | Where-Object { $_.Name -match "分子" } | Select-Object -ExpandProperty FullName -First 1

$data2 = Get-Content $mol_db -Encoding UTF8 -Raw | ConvertFrom-Json
$topics2 = Get-Content $mol_topics -Encoding UTF8 -Raw | ConvertFrom-Json
$known2 = $topics2.psobject.properties.name
$missing2 = $data2 | Where-Object { $null -ne $_.topic -and "" -ne $_.topic -and $_.topic -notin $known2 }
Write-Output "--- MOL ---"
$missing2 | Group-Object topic | Sort-Object Count -Descending | Select-Object Count, Name | Format-Table -HideTableHeaders
