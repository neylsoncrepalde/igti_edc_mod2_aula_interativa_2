variable "region" {
  description = "aws region"
  default     = "us-east-1"
}

variable "account_id" {
  default = 123456789
}

variable "environment" {
  default = "dev"
}

variable "prefix" {
  description = "objects prefix"
  default     = "igti-edc-mod2"
}

# Prefix configuration and project common tags
locals {
  prefix = var.prefix
  common_tags = {
    Environment = "dev"
    Project     = "igti-edc-mod2"
  }
}