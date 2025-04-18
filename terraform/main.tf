resource "aws_sqs_queue" "terraform_queue" {
  name                      = var.queue_name
  delay_seconds             = 1
  max_message_size          = 16384
  message_retention_seconds = 86400
  receive_wait_time_seconds = 1
  fifo_queue                  = true
  content_based_deduplication = true
}