# Singapore Property Dashboard

The Singapore Property Market is currently booming, and more expensive HDB flats are on the rise.
We would like to see how often the market is behaving to anticipate the increase of the HDB flats over a period of time in terms of percentage. Hence, we can understand how much we can expect to buy a flat in a particular area.

## Getting Started

I have created a Python Framework using FastAPI as the backend and Streamlit as the frontend. 
I am also scraping a popular Singapore property website for the data.

I am using my local MariaDB as my storage, feel free to change the credentials for your usage at `src/utils/helper.py` in the `DATABASE_URL` section to your own database.

## Installation

```bash
# Clone the repository to your local machine
git clone https://github.com/your-username/python-sg-property-dashboard.git

# Install the required dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd python-sg-property-dashboard

# Start the FastAPI server
python -m main

# Navigate to the project directory
cd python-sg-property-dashboard

# Run the Streamlit app
streamlit run main.py

```

We plan to deploy this project using Docker in the future for easier deployment and distribution.
