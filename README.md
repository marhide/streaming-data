## What is it and what does it do?

streaming-data is an application that gets data about articles from The Guardian's API and sends them to an AWS SQS queue.


## How do you use it?

### The Guardian API key:
First you will need to generate a key for The Guardian's API at [open-platform.theguardian.com/access/](https://open-platform.theguardian.com/access/).

Make sure to save the API key somewhere as it is needed via ether user input or to be set as an environmental variable run the application. To set the Guardian API key as an environmental variable, run the command

`export GUARDIAN_API_KEY=[you guardian api key]`

This will make it so that the application will use this API key by default every time it is ran. *This is optional and can be skipped if you would like to enter an API key via user input every time the application is ran.*

### AWS IAM User
If you don't have one already, create an IAM user in AWS with permissions that grants full access to AWS's SQS.
Create a secret access key for this IAM user if there isn't one already.

You will then need to export these environmental varibales to allow the application to run commands as the IAM user.

`export AWS_DEFAULT_REGION=[the aws region you would like to use eg. 'eu-west-2']`

`export AWS_ACCESS_KEY_ID=[your aws access key id]`

`export AWS_SECRET_ACCESS_KEY=[your aws secret access key]`

### AWS SQS queue
Now choose a name for the SQS queue and export it as an environmental variable too.

`export SQS_QUEUE_NAME=[the name you want for your sqs queue]`

*Hint: When exporting these environmental variables, don't include the square brackets or quotation marks.*

### Setup
To create a virtual environment and to install dependencies needed for the application, run the command

`make dev-setup`


If there isn't already an SQS queue for the application to send the results from the Guardian API to, you will have to create one with the following command. This SQS queue will have the same name as the value of the `SQS_QUEUE_NAME` variable.

`make new-sqs-queue`

### Running the application
Once an SQS queue has been created, you can run the application, by using the command

`make run-app`


## About testing:
Install the testing dependencies with the following command

`make test-requirements`

To run the test, use the command

`make unit-test`
