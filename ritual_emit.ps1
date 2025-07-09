$headers = @{ "Content-Type" = "application/json" }
$body = @{
    phase = "exhale"
    toneform = "shimmer"
    hue = "white"
    suggestion = "Clarity released"
    intensity = 0.8
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri http://localhost:5050/emit_glint -Method POST -Headers $headers -Body $body