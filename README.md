# streaming-data

## What is it and what does it do?

streaming-data is an application that gets data about articles from The Guardian's API and sends them to an AWS SQS queue.

## How does it work?




## How do you use it?

first generate an API key for The Guardian's API at

[open-platform.theguardian.com/access/](https://open-platform.theguardian.com/access/)

make sure to save the API key somewhere as it is needed via ether user input or to be set as an environmental variable run the application. to set the Guardian API key as an environmental variable for the application to use by default, run

`export GUARDIAN_API_KEY=[you guardian api key]`

if you don't have one already, create an IAM user in AWS. give this IAM user a permission that grants full access to AWS's SQS
create a secret access key for this user.

you will then need to export these environmental varibales to allow the application to use your IAM user

`export AWS_DEFAULT_REGION=[the aws region you would like to use eg. 'eu-west-2']`

`export AWS_ACCESS_KEY_ID=[your aws access key id]`

`export AWS_SECRET_ACCESS_KEY=[your aws secret access key]`

you will need to choose a name for the SQS queue and also export it as an environmental variable

`export SQS_QUEUE_NAME=[the name you want for your sqs queue]`

hint: when exporting these environmental variables, don't include the square brackets or quotation marks.

next run

`make dev-setup`

if there isn't already an sqs queue for the application to send the results from the guardian api, you will have to create one with the following command. this sqs queue will have the same name as the value of the `SQS_QUEUE_NAME` variable

`make new-sqs-queue`

once an sqs queue has been created, you can run the application, by using the command

`make run-app`

## About testing:

install the testing library requirements with

`make test-requirements`

to test, run

`make unit-test`