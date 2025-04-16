resource "aws_sqs_queue" "terraform_queue" {
  name                      = "my_queue"
  delay_seconds             = 1
  max_message_size          = 16384
  message_retention_seconds = 86400
  receive_wait_time_seconds = 1

}