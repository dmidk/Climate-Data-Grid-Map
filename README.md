# Grid and station map of DMI's Open Data
An interactive map that allows the user to get an overview of stations, parameters, grids and municipalities used in DMIs Open Data 

### Setup

Optionally, create a virtual environment for the pip dependencies to run this repo:
```bash
python -m venv name_of_venv
```

Clone this repository, and install dependencies through pip:
```bash
pip install -r requirements.txt
```

### Running the script

To generate the site, you should acquire an API key for both the climateData API and
oceanObs. When you have the keys, you can run the software as a simple command line utility:
```bash
python Create\ Map.py --climate-api-key=$CLIMATE_API_KEY --oceanobs-api-key=$OCEAN_API_KEY
```
The script will write the HTML page to `index.html`, which is self-contained HTML page.