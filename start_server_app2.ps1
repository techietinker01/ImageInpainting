# Start server for app2.py (H5 model version)
# Activate virtual environment and start Flask server with TensorFlow warnings suppressed
& ./.venv/Scripts/Activate.ps1
$env:TF_ENABLE_ONEDNN_OPTS="0"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Image Inpainting Server (app2.py)" -ForegroundColor Green
Write-Host "  Using H5 Model: saved_model.h5" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    # Use waitress on Windows because gunicorn depends on unix-only fcntl
    Write-Host "Starting with waitress (Windows-friendly WSGI server)..." -ForegroundColor Yellow
    python -m waitress --help > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Waitress found! Starting server..." -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 Server will be available at:" -ForegroundColor Cyan
        Write-Host "   http://localhost:5000" -ForegroundColor White
        Write-Host "   http://127.0.0.1:5000" -ForegroundColor White
        Write-Host ""
        Write-Host "🧪 Test endpoints:" -ForegroundColor Cyan
        Write-Host "   Status: http://localhost:5000/api/status" -ForegroundColor White
        Write-Host "   About:  http://localhost:5000/about" -ForegroundColor White
        Write-Host "   UI:     http://localhost:5000" -ForegroundColor White
        Write-Host ""
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        Write-Host ""
        
        python -m waitress --port=5000 app2:app
    } else {
        Write-Host "⚠️ waitress not available, falling back to Flask dev server" -ForegroundColor Yellow
        python app2.py
    }
} catch {
    Write-Host "❌ Error starting waitress, falling back to Flask dev server" -ForegroundColor Red
    python app2.py
}
