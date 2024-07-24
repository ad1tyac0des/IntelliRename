pip install -r requirements.txt

# Checking if .env file exists and contains NVIDIA_API_KEY
if (!(Test-Path .env) -or !(Get-Content .env | Select-String -Quiet "NVIDIA_API_KEY")) {
    Write-Host ""
    Write-Host "Creating .env file"
    New-Item -Path .env -ItemType File -Force | Out-Null
    $apiKey = Read-Host "Please enter your NVIDIA API key"
    Set-Content .env "NVIDIA_API_KEY=$apiKey"
    Write-Host ""
    Write-Host ".env file created with API key."
}
else {
    Write-Host ""
    Write-Host ".env file with API key already exists."
}

Write-Host ("-" * 100)
Write-Host ""
Write-Host "Running the Script..."
Write-Host ""
python rename_image.py