# Activate virtual environment and start Flask server with TensorFlow warnings suppressed
& ./.venv/Scripts/Activate.ps1
$env:TF_ENABLE_ONEDNN_OPTS="0"
Write-Host "Starting Flask server with TensorFlow warnings suppressed..."
try {
	# Use waitress on Windows because gunicorn depends on unix-only fcntl
	Write-Host "Starting with waitress (Windows-friendly WSGI server)..."
	python -m waitress --help > $null 2>&1
	if ($LASTEXITCODE -eq 0) {
		python -m waitress --port=5000 app:app
	} else {
		Write-Host "waitress not available, falling back to Flask dev server"
		python app.py
	}
} catch {
	Write-Host "Error starting waitress, falling back to Flask dev server"
	python app.py
}