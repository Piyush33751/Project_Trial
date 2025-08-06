-- Step 1: Create the table
CREATE TABLE firefighters_info (
    name VARCHAR(50),
    area VARCHAR(50),
    status VARCHAR(20),
    password VARCHAR(10)
);

-- Step 2: Insert the data
INSERT INTO firefighters_info (name, area, status, password) VALUES
('Sam Ng', 'Yishun', 'On-Duty', '1234'),
('Jayden Tan', 'Jurong', 'On-Duty', '1234'),
('Javier Liew', 'Serangoon', 'On-Duty', '1234'),
('Nikhil', 'Harbourfront', 'On-Duty', '1234'),
('Kayden Koo', 'Tampines', 'On-Duty', '1234'),
('Ben Chen', 'Canberra', 'On-Duty', '1234'),
('Ali', 'Bedok', 'Off-Duty', '1234'),
('Irfan', 'Pioneer', 'Off-Duty', '1234'),
('Kester Kwan', 'Tiong Bahru', 'Off-Duty', '1234'),
('Dennis Ho', 'Yew Tee', 'Off-duty', '1234');

-- Step 3: Select only people who are On-Duty
SELECT * FROM firefighters_info
WHERE status = 'On-Duty';