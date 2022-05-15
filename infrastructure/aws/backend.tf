# Backend configuration require a AWS storage bucket.
terraform {
  backend "s3" {
    bucket = "terraform-state-igti-ney"
    key    = "state/igti/edc/mod2/aula2/terraform.tfstate"
    region = "us-east-1"
  }
}