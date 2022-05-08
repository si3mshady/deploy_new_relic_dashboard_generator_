terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"

    }
  }
}


# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}

resource "null_resource" "create_deployment_package" {
  provisioner "local-exec" {
    command = <<HEREDOC
    source venv/bin/activate && pip freeze > requirements.txt
    mkdir deployment/
    pip install -r requirements.txt -t deployment/
    cp lambda_handler.py deployment/
    cp sendemail.py deployment/
    touch __init__.py deployment/
    zip -r  deployment_package.zip deployment
HEREDOC
  }
}



resource "aws_lambda_function" "daily_nr_metrics" {

  filename      = "deployment_package.zip"
  function_name = "daily_nr_metrics"
  role          = aws_iam_role.new_relic_iam_for_lambda.arn
  handler       = "lambda_handler.lambda_handler"
  runtime       = var.new_relic_python_rt[0]
}



resource "aws_iam_role" "new_relic_ca_access" {
  name               = "new_relic_ca_role"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "754728514883"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
               "sts:ExternalId": 3257316
            }
      }
    }
  ]
}
POLICY
}


resource "aws_iam_policy_attachment" "read-only-attach" {
  name = "read-only-attachment"

  roles = [aws_iam_role.new_relic_ca_access.name]

  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"

}



resource "aws_iam_role" "new_relic_iam_for_lambda" {
  name = "new_relic_iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}
