$data = Get-Content "app\data\臨床血液學與血庫學.json" -Encoding UTF8 -Raw | ConvertFrom-Json
$topics = Get-Content "app\data\topics_臨床血液學與血庫學.json" -Encoding UTF8 -Raw | ConvertFrom-Json
$known = $topics.psobject.properties.name
$missing = $data | Where-Object { $_.topic -notin $known -and $_.topic -ne $null -and $_.topic -ne "" }
Write-Output "=== HEMA ==="
$missing | Group-Object topic | Sort-Object Count -Descending | Select-Object Count, Name | Format-Table -HideTableHeaders

$data2 = Get-Content "app\data\醫學分子檢驗學與臨床鏡檢學.json" -Encoding UTF8 -Raw | ConvertFrom-Json
$topics2 = Get-Content "app\data\topics_醫學分子檢驗學與臨床鏡檢學.json" -Encoding UTF8 -Raw | ConvertFrom-Json
$known2 = $topics2.psobject.properties.name
$missing2 = $data2 | Where-Object { $_.topic -notin $known2 -and $_.topic -ne $null -and $_.topic -ne "" }
Write-Output "=== MOL ==="
$missing2 | Group-Object topic | Sort-Object Count -Descending | Select-Object Count, Name | Format-Table -HideTableHeaders
