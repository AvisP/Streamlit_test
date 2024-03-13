from beam import App, Runtime, Image
from transformers import pipeline

app = App(
    name="sentiment-analysis",
    runtime=Runtime(
        cpu=2,
        memory="8Gi",
        image=Image(
            python_version="python3.9",
            python_packages=["transformers", "torch"],
        ),
    ),
)

def load_models():
    model = pipeline(
        "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        tokenizer = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    )
    return model


@app.rest_api(loader=load_models)
def predict_sentiment(**inputs):
    # Retrieve model from loader
    model = inputs["context"]

    result = model(inputs["text"], truncation=True, top_k=3)
    prediction = {i["label"]: i["score"] for i in result}

    print(prediction)

    return {"prediction": prediction}
