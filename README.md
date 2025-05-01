# streaming-data

## What is it and what does it do?

streaming-data is an application that gets data about The Guardian articles and sends them to an AWS SQS queue.

## How does it work?




## How do you use it?

first generate an API key for The Guardian's API at

[open-platform.theguardian.com/access/](https://open-platform.theguardian.com/access/)

make sure to save the API key somewhere as it is needed via user input to run the application

if you don't have one already, create an IAM user in AWS. give this IAM user a permission that grants full access to AWS's SQS
create a secret access key for this user.

you will then need to export these environmental varibales to allow the application to use your IAM user

`$ export AWS_DEFAULT_REGION=[the aws region you would like to use eg. 'eu-west-2']`

`$ export AWS_ACCESS_KEY_ID=[your aws access key id]`

`$ export AWS_SECRET_ACCESS_KEY=[your aws secret access key]`

you will need to choose a name for the SQS queue and also export it as an environmental variable

`$ export MY_SQS_QUEUE_NAME=[the name you want for your sqs queue]`

hint: when exporting these environmental variables, don't include the square brackets or quotation marks.

next run

`make dev-setup`

now run

`make new-sqs-queue`

finally, to run the application, run

`make run-app`

about testing:

install the testing library requirements with

make test-requirements

to test, run

make unit-test