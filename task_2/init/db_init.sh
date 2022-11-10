#! /bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username="$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL 
	CREATE USER $APP_USER_DB with encrypted password '$APP_PASSWORD_DB';

	CREATE DATABASE $APP_DB_NAME;

	GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_USER_DB;

	\connect $APP_DB_NAME $APP_USER_DB;

	CREATE SCHEMA app;
	CREATE TABLE app.Product (
		id_product serial NOT NULL,
		product_name varchar(50) NOT NULL,
		CONSTRAINT "Product_pk" PRIMARY KEY (id_product)
	);

	CREATE TABLE app.Category (
		id_category serial NOT NULL,
		category_name varchar(50) NOT NULL,
		CONSTRAINT "Category_pk" PRIMARY KEY (id_category)
	);


	CREATE TABLE app.Product_Category (
		id_product integer NOT NULL,
		id_category integer NOT NULL,
		CONSTRAINT "Product_Category_pk" PRIMARY KEY (id_product,id_category)
	);

	ALTER TABLE app.Product_Category ADD CONSTRAINT "Category_fk" FOREIGN KEY ("id_category")
	REFERENCES app.Category (id_category) MATCH FULL
	ON DELETE RESTRICT ON UPDATE CASCADE;

	ALTER TABLE app.Product_Category ADD CONSTRAINT "Product_fk" FOREIGN KEY ("id_product")
	REFERENCES app.Product (id_product) MATCH FULL
	ON DELETE RESTRICT ON UPDATE CASCADE;

	\connect $APP_DB_NAME $POSTGRES_USER;

	COPY app.Product(id_product, product_name)
	FROM '/data/product.csv'
	DELIMITER ','
	CSV HEADER;

	COPY app.Category(id_category, category_name)
	FROM '/data/category.csv'
	DELIMITER ','
	CSV HEADER;

	COPY app.Product_Category(id_product, id_category)
	FROM '/data/product_category.csv'
	DELIMITER ','
	CSV HEADER;
EOSQL
