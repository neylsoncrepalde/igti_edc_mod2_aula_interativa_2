resource "aws_db_instance" "default" {
  allocated_storage    = 10
  engine               = "sqlserver-ee"
  engine_version       = "15.00.4198.2.v1"
  instance_class       = "db.t3.small"
  name                 = "igti-edc-mod2"
  username             = "admin"
  password             = "admin"
  skip_final_snapshot  = true
  publicly_accessible  = true
}