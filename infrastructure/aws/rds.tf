resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "sqlserver-ex"
  engine_version       = "15.00.4198.2.v1"
  instance_class       = "db.t3.small"
  db_name              = "igti-edc-mod2"
  username             = "admin"
  password             = "admin"
  skip_final_snapshot  = true
  parameter_group_name = "sqlserver-ee-15.0"
  publicly_accessible  = true
  license_model        = "license-included"
}