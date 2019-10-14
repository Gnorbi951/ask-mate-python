DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    registration_date date NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO users (user_name, password) VALUES ('admin', '$2b$12$9MQbFIv8mijmmHs.CGHZt.kcYTxymNlJ3BeKOVTDLpDpW18rCWBxS');

