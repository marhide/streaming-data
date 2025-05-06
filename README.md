# The Guardian API to AWS SQS Data Streaming Project

An application that gets data about articles from the The Guardian's API and sends it as a message to an AWS SQS queue.

## How do you use it?

This application will need [Python](https://www.python.org/) and [Terraform](https://developer.hashicorp.com/terraform/install) to be installed in order to run.

### Setup

#### The Guardian API key:

First you will need to generate a key for The Guardian's API at [open-platform.theguardian.com/access/](https://open-platform.theguardian.com/access/).

Make sure to save the API key somewhere as it is needed via ether user input or to be set as an environmental variable run the application. To set the Guardian API key as an environmental variable, run the command

`export GUARDIAN_API_KEY=[your API key]`

This will make it so that the application will use this API key by default every time it is ran. *This is optional and can be skipped if you would like to enter an API key via user input every time the application is ran.*


#### AWS IAM user

If you don't have one already, create an IAM user in AWS with permissions that grants full access to AWS SQS.
Create a secret access key for this IAM user if there isn't one already. You will then need to export these environmental variables to allow the application to run commands as the IAM user.

```
export AWS_DEFAULT_REGION=[AWS region you would like to use eg. 'eu-west-2']
export AWS_ACCESS_KEY_ID=[AWS access key ID]
export AWS_SECRET_ACCESS_KEY=[AWS secret access key]
```

#### AWS SQS queue

Now choose a name for the SQS queue and export it as an environmental variable too.

`export SQS_QUEUE_NAME=[the name you want for your SQS queue]`

*Hint: When exporting these environmental variables, don't include the square brackets or quotation marks.*


### Build

To create a virtual environment and to install dependencies needed for the application, run the command

`make dev-setup`

If there is not an SQS queue for the application to send the results from the Guardian API to already, you will have to create one with the following command.

`make new-sqs-queue`

This SQS queue will have the same name as the value of the `SQS_QUEUE_NAME` variable. If the value of the SQS queue environmental variable has been changed, the current existing queue will be deleted and a new queue with the new name will be created when this command is executed.

### Delete AWS infrastructure

To delete the SQS queue, run the command

`make delete-sqs-queue`

This will run `terraform destroy`. To do this manually, navigate to the terraform folder and run command `terraform destroy`.

### Running the application

Once an SQS queue has been created, you can run the application, by using the command

`make run-app`

Alternatively, the application can be used as a function as part of a component of a larger program.

```
from src.main import run_app

run_app()
```


### Parameters

All arguments passed into the `run_app()` function should be strings.

##### `api_key`

The API key needed to access TheGuardian's API. `test` should work in most cases.

##### `queue_name`

The name of the AWS SQS queue to send messages to.

##### `search_term`

Results from the API will only include this term.

##### `from_date`

Only returns articles from the API punished after this date. Has to be in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format (YYYY-MM-DD).

##### `sort_by`

The list of articles sent to the SQS queue will be ordered according to the sort by term's corresponding key. To sort by publication date, use `webPublicationDate`, `publicationdate`, `date`, `from`, `fromdate` or `datefrom`. To sort by article title, use `webTitle`, `title`, `article` or `name`. To sort by URL, use `webUrl` or `url`.

##### `sort_order`

Whether the articles will be in ascending or descending order. Use `asc` or `ascending` for the articles to be returned in ascending order. Use `desc` or `descending` for descending order.

####  Example:

```
run_app(
api_key="test",
queue_name="my_queue_name",
search_term="machine learning",
from_date="2000-01-01",
sort_by="title",
sort_order="asc"
)
```

When running the application with `make run-app`, you will be asked to input the API key and SQS queue name if they have not been exported as environmental variables during the setup. The user can skip inputting a search term or from date by pressing enter, submitting an empty string. The program will take the default search term/from date from the config if this happens.

### Config file

The default search functionality of the application can be changed through the `config.ini` file. When the application is being ran with `make run-app`, the only way to chage the sort by and sort order is through the config file.

####  Example:

```
default_search_term = machine learning
default_from_date = 1900-01-01
default_sort_by = webPublicationDate
default_sort_order = desc
```

These will be used when the user inputs an empty string or when the `run_app()` function is not passed an argument.

## Message information

The messages sent to the SQS queue will be in JSON format. It will have a key of the URL used to search the API and the value will be an array of objects with information about a specific article.
Each object in the array will be in the format:

```
{
    "webPublicationDate": "[publication date of article]",
    "webTitle": "[title of article]",
    "webUrl": "[URL of article on The Guardian's website]"
}
```

#### Example:

```
{
    "https://content.guardianapis.com/search?q=machine%20learning": 
        [
            {
                "webPublicationDate": "2025-04-29T14:15:50Z", 
                "webTitle": "The Smashing Machine: Dwayne Johnson fights for an Oscar in first trailer",
                "webUrl": "https://www.theguardian.com/film/2025/apr/29/smashing-machine-dwayne-rock-johnson-movie"
            },
            {
                "webPublicationDate": "2025-04-29T14:00:47Z",
                "webTitle": "Sage Bambino Plus coffee machine review: the perfect espresso machine for beginners",
                "webUrl": "https://www.theguardian.com/thefilter/2025/apr/29/sage-bambino-plus-coffee-espresso-machine-review-uk"
            },    
            {
                "webPublicationDate": "2025-04-23T05:00:10Z",
                "webTitle": "Government pauses plans to ease slot machine rules across Great Britain",
                "webUrl": "https://www.theguardian.com/society/2025/apr/23/government-pauses-plans-to-ease-slot-machine-rules-across-great-britain"
            }
    ]
}
```

All messages sent to the SQS queue will have the message group ID of `guardian-content`.

## Testing

Install the testing dependencies with the following command

`make test-requirements`

To run the test, use the command

`make unit-test`

To check test coverage run

`make check-coverage`
