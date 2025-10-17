# PowerShell script to run app2.py with H5 model
# Built by Rupam Kumari

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  Image Inpainting Server (H5 Model)" -ForegroundColor Yellow
Write-Host "  Built by Rupam Kumari" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️  Virtual environment not found. Using system Python." -ForegroundColor Yellow
}

# Check if H5 model exists
if (Test-Path "saved_model.h5") {
    $fileSize = (Get-Item "saved_model.h5").Length / 1MB
    Write-Host "✅ H5 model found: saved_model.h5 ($([math]::Round($fileSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "❌ H5 model not found: saved_model.h5" -ForegroundColor Red
    Write-Host "   Please run the Jupyter notebook to generate the model first." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if .env exists
if (Test-Path ".env") {
    Write-Host "✅ Environment file found: .env" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Using default settings." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Starting Flask server on http://localhost:5001" -ForegroundColor Cyan
Write-Host "   (H5 Model Version)" -ForegroundColor Gray
Write-Host ""
Write-Host "📝 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the Flask app
python app2.py
