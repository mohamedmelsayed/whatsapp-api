-- Create a table to store sender information
CREATE TABLE senders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store uploaded media metadata
CREATE TABLE uploaded_media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    media_id VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    media_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store message logs
CREATE TABLE message_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    customer_phone VARCHAR(15) NOT NULL,
    message_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES senders (id)
);