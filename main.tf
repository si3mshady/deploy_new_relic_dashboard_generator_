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

    mkdir deployment/
    cd deployment/
    pip3 install -r ../requirements.txt -t .
    zip -r ./deployment_package.zip .
    cp ./deployment_package.zip ../deployment_package.zip
    cd ../
    zip -g deployment_package.zip lambda.py
    zip -g deployment_package.zip sendemail.py
HEREDOC
  }
}



resource "aws_lambda_function" "daily_nr_metrics" {
  depends_on = [
    null_resource.create_deployment_package
  ]
  timeout       = 40
  filename      = "deployment_package.zip"
  function_name = "daily_nr_metrics"
  role          = aws_iam_role.new_relic_iam_for_lambda.arn
  handler       = "lambda.lambda_handler"
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

  inline_policy {
    name = "ses_full_access"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["*"]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }

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


resource "aws_cloudwatch_event_target" "daily_dashboard" {
  arn       = aws_lambda_function.daily_nr_metrics.arn
  target_id = "metrics"
  rule      = aws_cloudwatch_event_rule.daily.id
}


resource "aws_cloudwatch_event_rule" "daily" {

  schedule_expression = "rate(1 day)"

}
