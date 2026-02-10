USE lms_db;
-- student user

INSERT INTO User (name, email, password)
VALUES
('Arjun Kumar', 'arjun.kumar@gmail.com', 'Arjun Kumar'),
('Priya Sharma', 'priya.sharma@gmail.com', 'Priya Sharma'),
('Rahul Verma', 'rahul.verma@gmail.com', 'Rahul Verma'),
('Sneha Iyer', 'sneha.iyer@gmail.com', 'Sneha Iyer'),
('Karthik R', 'karthik.r@gmail.com', 'Karthik R'),
('Neha Patel', 'neha.patel@gmail.com', 'Neha Patel'),
('Rohit Meena', 'rohit.meena@gmail.com', 'Rohit Meena'),
('Anjali Das', 'anjali.das@gmail.com', 'Anjali Das');

-- admin user 

INSERT INTO User (name, email, password, role)
VALUES
('System Admin', 'admin@lms.com', 'admin123', 'ADMIN'),
('Course Admin', 'course.admin@lms.com', 'course123', 'ADMIN');

-- courses

INSERT INTO Course (title, description, duration, level)
VALUES
('Artificial Intelligence & Machine Learning',
 'Introduction to AI and ML concepts, algorithms, and applications',
 60,
 'advanced'),

('Cyber Security',
 'Basics of cyber security, threats, attacks, and protection mechanisms',
 45,
 'intermediate'),

('Data Structures and Algorithms',
 'Core data structures and algorithmic problem solving techniques',
 50,
 'Intermediate'),

('Web Development',
 'HTML, CSS, and basic backend concepts for building web applications',
 40,
 'Beginner'),

('Database Management Systems',
 'Relational databases, SQL, normalization, and transactions',
 55,
 'Intermediate');
 
 -- ENROLLMENT
 
 INSERT INTO Enrollment (user_id, course_id, enrolled_date, status)
VALUES
(1, 1, '2026-01-10', 'ACTIVE'),
(2, 2, '2026-01-12', 'COMPLETED'),
(3, 3, '2026-01-15', 'ACTIVE'),
(4, 1, '2026-01-18', 'COMPLETED'),
(5, 4, '2026-01-20', 'ACTIVE'),
(6, 5, '2026-01-22', 'ACTIVE'),
(7, 3, '2026-01-25', 'COMPLETED'),
(8, 2, '2026-01-28', 'ACTIVE'),
(9, 5, '2026-02-01', 'ACTIVE'),
(10, 4, '2026-02-03', 'COMPLETED');

-- MOUDLE

INSERT INTO Module (course_id, module_title, module_order)
VALUES
-- Course 1: AI & ML
(1, 'Introduction to AI', 1),
(1, 'Machine Learning Basics', 2),
(1, 'Applications of AI', 3),

-- Course 2: Cyber Security
(2, 'Cyber Security Fundamentals', 1),
(2, 'Types of Cyber Attacks', 2),
(2, 'Security Best Practices', 3),

-- Course 3: DSA
(3, 'Arrays and Linked Lists', 1),
(3, 'Stacks and Queues', 2),
(3, 'Sorting and Searching', 3),

-- Course 4: Web Development
(4, 'HTML Basics', 1),
(4, 'CSS Styling', 2),
(4, 'Introduction to Backend', 3),

-- Course 5: DBMS
(5, 'Database Basics', 1),
(5, 'Normalization', 2),
(5, 'SQL and Transactions', 3);


