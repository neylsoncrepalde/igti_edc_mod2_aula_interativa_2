resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "sqlserver-ex"
  engine_version       = "15.00.4198.2.v1"
  instance_class       = "db.t3.small"
  username             = "admin"
  password             = "administrator"
  skip_final_snapshot  = true
  publicly_accessible  = true
  license_model        = "license-included"
}