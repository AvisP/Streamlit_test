This repo shows how to host a streamlit webapp on the community cloud or other webhosting platforms (heroku, ploomber) that makes API call to an AI service (beam.cloud) running on a serverless infrastructure for generative AI

The example shown here will do a sentiment analysis of a given sentence and will display the results provided by a sentiment roberta model.

## Steps
1. Perform the installation [steps](https://docs.beam.cloud/getting-started/installation) for beam
2. Run `beam deploy beam_app.py` and wait for deplyment to finish
3. Get the url and credentials from the beam dashboard
4. Start streamlit app using `streamlit run streamlit_app_git.py`
5. Enter the credentials
6. Enter a text and get the sentiment response


A new app `streamlit_authenticate.py` has been provided that does authentication based on username and password provided. A private google spreadsheet stores the authorized users that can be modified as needed. The details of how to connect streamlit to google sheets through API can be found [here](https://github.com/streamlit/gsheets-connection).

For local development a folder called `.streamlit` has to be created in root directory and a `secrets.toml` inside it where the google API configurations will be stored. For online deployment on streamlit community cloud it will go in Secrets
