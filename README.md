# python-sg-property-dashboard
The Singapore Property Market is currently booming, and more expensive HDB flats are on the rise,
We would like to see how often the market is behaving to anticipate the increase of the HDB flats over a period of time in terms of percentage. Hence, we can understand how much we can expect to buy a flat in a particular area.

I have created a Python Framework using FastAPI as the backend and Streamlit as the frontend. 
I am also scraping a popular Singapore property website for the data.

I am using my local MariaDB as my storage, feel free to change the credentials for your usage at src/utils/helper.py in the DATABASE_URL section to your own database.

To quickly start this project, you need to run two terminals, one for frontend and another for backend.

python -m main.py 
streamlit run main.py

From there you can quickly spin up your project and use the dashboard for your own use. 

I am planning to deploy this project into Docker in the future.