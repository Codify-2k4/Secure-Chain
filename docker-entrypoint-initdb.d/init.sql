-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Create the patients table
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    disease VARCHAR(200) NOT NULL,
    phone_number VARCHAR(15),
    email VARCHAR(100),
    disease_details TEXT,
    prescribed_medicines TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES users(id)
);

-- Create the access_permissions table
CREATE TABLE access_permissions (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL REFERENCES users(id),
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    granted BOOLEAN NOT NULL DEFAULT FALSE
);

-- Insert Users with hashed passwords
INSERT INTO users (username, password_hash, role) VALUES
('admin', 'pbkdf2:sha256:260000$mFgDp3dG6YHqk3zK$3e7a6c4f88a151a3c8a7f7a55b53e2674e3d0f3d7e8e5c4f47e3a3f4d6c2a8c0', 'admin'),  -- Password: admin123
('dr_smith', 'pbkdf2:sha256:260000$abc...', 'doctor'),  -- Password: doctor123
('dr_jones', 'pbkdf2:sha256:260000$def...', 'doctor'),  -- Password: doctor123
('patient1', 'pbkdf2:sha256:260000$pqr...', 'patient'),  -- Password: patient123
('patient2', 'pbkdf2:sha256:260000$stu...', 'patient');  -- Password: patient123

-- Insert Patients with additional details
INSERT INTO patients (name, age, disease, phone_number, email, disease_details, prescribed_medicines, user_id) VALUES
('John Doe', 35, 'Type 2 Diabetes', '123-456-7890', 'john.doe@example.com', 'Type 2 Diabetes with mild neuropathy', 'Metformin, Insulin', 4),   -- user_id = 4 (patient1)
('Jane Smith', 28, 'Hypertension', '234-567-8901', 'jane.smith@example.com', 'Primary hypertension with no complications', 'Lisinopril, Amlodipine', 5);  -- user_id = 5 (patient2)

-- Insert Access Permissions
INSERT INTO access_permissions (doctor_id, patient_id, granted) VALUES
(2, 1, true),  -- Doctor 2 has access to Patient 1
(3, 2, true);  -- Doctor 3 has access to Patient 2