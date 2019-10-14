DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_name character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    registration_date date NOT NULL DEFAULT CURRENT_DATE,
    status character varying(255) DEFAULT 'user'
);

INSERT INTO users (user_name, password, status)
VALUES ('admin', '$2b$12$9MQbFIv8mijmmHs.CGHZt.kcYTxymNlJ3BeKOVTDLpDpW18rCWBxS', 'admin');

-- Dont run this part twice please
ALTER TABLE question
ADD COLUMN user_id int REFERENCES users(id);

ALTER TABLE answer
ADD COLUMN user_id int REFERENCES users(id);

ALTER TABLE comment
ADD COLUMN user_id int REFERENCES users(id);
