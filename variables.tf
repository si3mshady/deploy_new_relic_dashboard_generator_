variable "aws_region" {
  default = "us-west-2"
}

variable "new_relic_layer_python" {
  default = "arn:aws:lambda:us-east-1:451483290750:layer:NewRelicPython39:17"
}

variable "new_relic_python_rt" {
  default = ["python3.9"]
}

variable "new_relic_account" {
  default = "754728514883"
}
