# SmartRoadCrackWebApp

SmartRoadCrackWebApp is a small Flask web application for detecting and managing road-crack images. It provides a web UI to upload images, runs image processing to detect cracks, and stores results for review.

## Table of contents
- Project overview
- Features
- Project structure
- Requirements
- Installation
- Running the app
- Testing
- File upload & results


## Project overview

This repository contains a Flask application that accepts image uploads, runs crack-detection/image-processing routines (in `src/image_processing.py`) and displays results in the web UI. It is designed as a small demonstrator and is organized to be easy to extend.

## Features

- Simple web UI (templates in `templates/`) to upload and view results
- Image processing logic centralized in `src/image_processing.py`
- Results saved under `data/results/` and `static/results/` for serving
- Unit tests (simple pytest tests included)

## Project structure

Top-level files and folders:

- `app.py` - Flask app entrypoint and routes
- `requirements.txt` - Python dependencies
- `test_app.py`, `test_buttons.py` - tests
- `src/` - application modules
  - `image_processing.py` - image processing functions
  - `utils.py` - helper utilities
- `data/` - input and result data folders
  - `upload/` - uploaded images
  - `results/` - processed outputs
- `static/` - static files (CSS, JS, images)
- `templates/` - HTML templates: `index.html`, `result.html`

## Requirements

This project uses Python (3.8+ recommended). Install packages from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

If you don't have a virtual environment, create one first:

```powershell
python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1; python -m pip install -r requirements.txt
```

## Installation & run (development)

1. Install dependencies (see previous section).
2. Ensure `data/upload/` and `data/results/` exist (they are present in the repo). You can create them manually if needed.
3. Start the app:

```powershell
python app.py
```

The app will start a Flask development server (by default on http://127.0.0.1:5000). Open the browser and navigate to the root to upload images.

## Usage

- Open the app in your browser.
- Use the upload form to choose an image or images.
- Submit to run the processing pipeline — processed images/results will be written into `data/results/` and served from `static/results/` (or as implemented in the app).
- View the result page (`result.html`) for processed output.

## Running tests

This project includes a couple of pytest tests. Run them from the project root:

```powershell
python -m pytest -q
```

Add more tests under `tests/` or expand existing test files.

## Development notes

- Image processing logic is implemented in `src/image_processing.py`. If you want to change detection settings, start there.
- Utility functions are in `src/utils.py`.
- Static assets: `static/css/style.css` controls basic styling.

