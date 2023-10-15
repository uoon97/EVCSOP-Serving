# Serving for EV Charger Station Occupancy Prediction Model

## How to

Build the Docker image:

    docker build -t model_api:0.0 .

Run the Container:

    docker run -it --name model_api_0.0 -p 5000:5000 model_api:0.0

From another CMD, send the input features in a request:

    curl -X POST -F file=@img_129.jpg http://localhost:5000/inference

Since the model was not completed yet, the image used in the simple image classification model was used as input.

## Example

![model api by docker with flask](https://github.com/uoon97/model-api/assets/64677725/bbbbdcf9-519f-45d6-8c6a-30d2cca7a861)
