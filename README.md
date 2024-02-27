# dv_iZEV
Data visualization with Statistics on the Incentives for Zero-Emission Vehicles (iZEV) Program FY2019-2020

## Getting Started
To get started with this project, you'll need to clone the repository and set up a virtual environment. This will allow you to install the required dependencies without affecting your system-wide Python installation.

### Cloning the Repository

    git clone https://github.com/jkmathilda/dv-iZEV.git

### Setting up a Virtual Environment

    cd ./dv-iZEV

    pyenv versions

    pyenv local 3.11.6

    echo '.env'  >> .gitignore
    echo '.venv' >> .gitignore

    python -m venv .venv        # create a new virtual environment

    source .venv/bin/activate   # Activate the virtual environment

### Install the required dependencies

    pip list

    pip install -r requirements.txt

### Running the Application

    python -m streamlit run dashboard.py
    
### Deactivate the virtual environment

    deactivate


# Example
