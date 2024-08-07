CREATE TABLE IF NOT EXISTS consultas (
    id SERIAL PRIMARY KEY,
    idade_grupo VARCHAR(50),
    peso FLOAT,
    total FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
