# v~art Tool
#### MSc Project: DanceMoves: A Visual Analytics Tool for Dance Movement Analysis


### Installation
Create environment from file. With anaconda installed:
```bash
conda env create -f requirements.yml
```
Activate the environment
```bash
conda activate dash
```
Run the application 
```bash
python dance_moves.py
```
The server runs the application at `http://127.0.0.1:8050/`

### Project Structure
* `app.py`
The Flask Backend that serves the application

* `assets/`
This folder is required by Dash and contains anything that is considered local file storage like the dataset
(dance videos, JSON files), thumbnails, logos, css rules etc.

* `metrics/`
As the name suggests, it contains all the code for the similarity metrics and DTW

* `layouts/`
Since we have multipage application, this folder contains the different component layouts for each page

* `components/`
Folder that contains all the reusable components

* `settings.py`
Settings and constant global variables

* `utils.py`
Helper functions
