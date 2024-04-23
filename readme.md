# EM-VIEW: A Simple Dashboard for Your EM-DAT Data

This is a [Streamlit](https://streamlit.io/) Web App designed for visualize the [EM-DAT International 
Disaster Database](https://www.emdat.be/) data contained in your official EM-DAT xlsx file. 
You can download the EM-DAT data by registering at https://public.emdat.be/.


## Prerequisites

- Python 3.11.3
- Streamlit
- Other dependencies (see `requirements.txt` or `environment.yaml`)

## Local Installation

TODO: add requirements and environement files. 

### Virtual Environment (venv)

1. Clone the repo:
   ```bash
   git clone <your repo link>
   ```

2. Navigate to the project directory:
   ```bash
   cd <your repo name>
   ```

3. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   On Windows, run:
   ```bash
   venv\Scripts\activate
   ```
   On Unix or MacOS, run:
   ```bash
   source venv/bin/activate
   ```

5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Anaconda (conda)

1. Clone the repo:
   ```bash
   git clone <your repo link>
   ```

2. Navigate to the project directory:
   ```bash
   cd <your repo name>
   ```

3. Create a new conda environment with the provided `environment.yaml` file:
   ```bash
   conda env create -f environment.yaml
   ```

4. Activate the conda environment:
   ```bash
   conda activate <your environment name>
   ```

5. If your `environment.yaml` doesn't specify the dependencies, install them manually:
   ```bash
   conda install --file requirements.txt
   ```

## How to Run

After you have installed the necessary dependencies, you can run the app locally with the following command:

Streamlit will provide a URL in the terminal, usually `http://localhost:8501`. Open this URL in your web browser to interact with the app.

## Contributing

TODO <Include information about how others can contribute to your project.>

## License

TODO <Include information about your project's license, if any.>

## Contact

TODO <Include some contact information for you or your team, if available.>

## Acknowledgements

TODO <Include credit for any external resources that helped you achieve your project.>