# Serving for EV Charger Station Occupancy Prediction Model

## How to

Clone git repo on EC2:

    sudo yum update -y
    sudo yum install git -y
    git clone https://github.com/hwangpeng-sam/model-serving.git

Run shell script files to build docker image:

    cd model-serving
    sh setting4build.sh
    sh image_build.sh

After setting aws configure, run the shell script file to push image: <br>
(Modify region, Elastic Container Registry!)

    sh image_push.sh

After create aws lambda function, connect your DB (by creating your private.db_info and inserting values into table) <br>
Lastly, create test event as belows. <br>
( lambda function configuration: Memory(2048 MB), Runtime(1m) ) 

    event = {}


