```sql
CREATE TABLE vehicle (
	id int NOT NULL IDENTITY(1,1) primary key,
	customer_id int NOT NULL,
	ano_modelo text NULL,
	modelo text NULL,
	fabricante text NULL,
	ano_veiculo text NULL,
	categoria text NULL
);

INSERT INTO [dw].dbo.vehicle (customer_id, ano_modelo, modelo, fabricante, ano_veiculo, categoria) VALUES(0, '2022', 'Uno', 'Fiat', '2022', 'Hatch');
INSERT INTO [dw].dbo.vehicle (customer_id, ano_modelo, modelo, fabricante, ano_veiculo, categoria) VALUES(0, '2022', 'Prisma', 'Chevrolet', '2022', 'Sedan');
INSERT INTO [dw].dbo.vehicle (customer_id, ano_modelo, modelo, fabricante, ano_veiculo, categoria) VALUES(0, '2022', 'Kicks', 'Nissan', '2022', 'SUV');

SELECT * FROM vehicle;
```