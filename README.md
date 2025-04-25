# Data Analytics Dashboard

A web-based data analytics dashboard that allows users to upload CSV files, view data previews, generate summary statistics, and visualize selected columns through interactive charts.

## Features

- CSV file upload and processing
- Data preview with pagination
- Summary statistics generation
- Interactive data visualization with multiple chart types:
  - Bar charts
  - Line charts
  - Histograms

## Requirements

- Python 3.7+
- Flask
- Pandas
- Matplotlib
- NumPy

## Installation

1. Clone this repository or download the source code.

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a CSV file using the file upload form

4. View the data preview and summary statistics

5. Select a column and chart type to generate visualizations

## File Structure

- `app.py`: Main Flask application file
- `templates/index.html`: HTML template for the dashboard
- `requirements.txt`: Python package dependencies
- `uploads/`: Directory for storing uploaded CSV files

## Notes

- The application supports CSV files up to 16MB in size
- Only the most recently uploaded file is used for visualizations
- The application creates an 'uploads' directory automatically if it doesn't exist 