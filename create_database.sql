CREATE DATABASE IF NOT EXISTS rz_status;
use rz_status;

CREATE TABLE  IF NOT EXISTS user (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(500),
    password VARCHAR(200),
    is_admin BOOLEAN,
    PRIMARY KEY (id)
);

CREATE TABLE  IF NOT EXISTS urls (
    id INT NOT NULL AUTO_INCREMENT,
    url VARCHAR(200),
    PRIMARY KEY (id)
);


INSERT INTO user (email, password, is_admin) VALUES ('admin', 'df6b9fb15cfdbb7527be5a8a6e39f39e572c8ddb943fbc79a943438e9d3d85ebfc2ccf9e0eccd9346026c0b6876e0e01556fe56f135582c05fbdbb505d46755a', true);
INSERT INTO urls (url) VALUES ('http://www.amazon.com');
