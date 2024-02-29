This repo shows how to host a streamlit webapp on the community cloud or other webhosting platforms (heroku, ploomber) that makes API call to an AI service (beam.cloud) running on a serverless infrastructure for generative AI

The example shown here will do a sentiment analysis of a given sentence and will display the results provided by a sentiment roberta model.

## Steps
1. Perform the installation [steps](https://docs.beam.cloud/getting-started/installation) for beam
2. Run `beam serve beam_app.py` and wait for deplyment to finish
3. Get the url and credentials from the beam dashboard
4. Start streamlit app using `streamlit run streamlit_app_git.py`
5. Enter the credentials
6. Enter a text and get the sentiment response
