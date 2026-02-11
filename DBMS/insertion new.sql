USE lms_db;

-- USER INSERTION

INSERT INTO User (name, email, password)
VALUES
('Arjun Kumar', 'arjun.kumar@gmail.com', 'arjun'),
('Priya Sharma', 'priya.sharma@gmail.com', 'priya'),
('Rahul Verma', 'rahul.verma@gmail.com', 'rahul'),
('Sneha Iyer', 'sneha.iyer@gmail.com', 'sneha'),
('Karthik R', 'karthik.r@gmail.com', 'karthik'),
('Neha Patel', 'neha.patel@gmail.com', 'neha'),
('Rohit Meena', 'rohit.meena@gmail.com', 'rohit'),
('Anjali Das', 'anjali.das@gmail.com', 'anjali'),
('Vikram Singh', 'vikram.singh@gmail.com', 'vikram');

-- ADMIN INSERTION

INSERT INTO User (name, email, password, role)
VALUES
('System Admin', 'admin@lms.in', 'admin', 'ADMIN');

-- COURSE-1,MOUDLE,VIDEO
INSERT INTO Course (title, description, duration, level)
VALUES
('Introduction to Programming with C++',
 'Learn C++ basics, syntax, control structures, functions, arrays and build a mini project.',
 40,
 'Advanced'),

('Fundamentals of DBMS',
 'Understand databases, ER model, relational model, SQL and normalization concepts.',
 45,
 'Advanced'),

('Frontend Web Development',
 'Learn HTML, CSS, JavaScript and responsive web design techniques.',
 50,
 'Advanced'),

('Data Structures in C++',
 'Master arrays, linked lists, stacks, queues, trees, graphs and sorting algorithms.',
 55,
 'Intermediate'),

('Introduction to AI & Machine Learning',
 'Learn AI fundamentals, supervised learning, preprocessing and model evaluation.',
 60,
 'Intermediate');
 
 
 INSERT INTO Module (course_id, module_title, module_order, module_type)
VALUES
(1, 'Basics of C++ & Syntax', 1, 'VIDEO'),
(1, 'Variables, Data Types & Operators', 2, 'VIDEO'),
(1, 'Control Statements (if, switch, loops)', 3, 'VIDEO'),
(1, 'Functions & Arrays', 4, 'VIDEO'),
(1, 'Mini Project – Student Record System', 5, 'PROJECT'),
(1, 'Final Quiz – C++ Fundamentals', 6, 'QUIZ');

INSERT INTO Video (module_id, video_title, video_url)
VALUES
(1, 'Basics of C++ & Syntax',
 'https://youtu.be/s0g4ty29Xgg?si=w4vee_IskJAW20nU'),

(2, 'Variables, Data Types & Operators',
 'https://youtu.be/fZbSl58orNs?si=SXFGYQ1z92TwFxy_'),

(3, 'Control Statements (if, switch, loops)',
 'https://youtu.be/9-BjXs1vMSc?si=ZbQkpy79TwlORL0G'),

(4, 'Functions & Arrays',
 'https://youtu.be/OgosiMQPGVA?si=jT8pHRB9vRvOBDK5');

-- COURSE-2,MOUDLE,VIDEO

INSERT INTO Course (title, description, duration, level)
VALUES
('Fundamentals of DBMS',
 'Understand databases, ER model, relational model, SQL and normalization concepts.',
 45,
 'intermediate');
 
 INSERT INTO Module (course_id, module_title, module_order, module_type)
VALUES
(2, 'Introduction to Databases', 1, 'VIDEO'),
(2, 'ER Model & Relational Model', 2, 'VIDEO'),
(2, 'SQL Basics (DDL, DML)', 3, 'VIDEO'),
(2, 'Normalization & Keys Explained', 4, 'VIDEO'),
(2, 'Mini Project – Database Design', 5, 'PROJECT'),
(2, 'Final Quiz – DBMS Fundamentals', 6, 'QUIZ');

INSERT INTO Video (module_id, video_title, video_url)
VALUES
(7, 'Introduction to Databases',
 'https://www.youtube.com/watch?v=HXV3zeQKqGY'),

(8, 'ER Model & Relational Model',
 'https://www.youtube.com/watch?v=FQm_wpA9BR0'),

(9, 'SQL Basics (DDL, DML)',
 'https://www.youtube.com/watch?v=7S_tz1z_5bA'),

(10, 'Normalization & Keys Explained',
 'https://www.youtube.com/watch?v=UrYLYV7WS_8');
 
 -- COURSE-3,MOUDLE,VIDEO
 
 INSERT INTO Course (title, description, duration, level)
VALUES
('Frontend Web Development',
 'Learn HTML, CSS, JavaScript and responsive web design techniques.',
 50,
 'Beginner');

INSERT INTO Module (course_id, module_title, module_order, module_type)
VALUES
(3, 'HTML Basics', 1, 'VIDEO'),
(3, 'CSS Full Course for Beginners', 2, 'VIDEO'),
(3, 'JavaScript Basics for Beginners', 3, 'VIDEO'),
(3, 'Responsive Web Design (Media Queries)', 4, 'VIDEO'),
(3, 'Mini Project – Responsive Portfolio Website', 5, 'PROJECT'),
(3, 'Final Quiz – Frontend Development', 6, 'QUIZ');

INSERT INTO Video (module_id, video_title, video_url)
VALUES
(19, 'HTML Basics',
 'https://www.youtube.com/watch?v=pQN-pnXPaVg'),

(20, 'CSS Full Course for Beginners',
 'https://www.youtube.com/watch?v=OXGznpKZ_sA'),

(21, 'JavaScript Basics for Beginners',
 'https://www.youtube.com/watch?v=W6NZfCO5SIk'),

(22, 'Responsive Web Design (Media Queries)',
 'https://www.youtube.com/watch?v=srvUrASNj0s');

-- COURSE-5,MOUDLE,VIDEO

INSERT INTO Course (title, description, duration, level)
VALUES
('Data Structures in C++',
 'Master arrays, linked lists, stacks, queues, trees, graphs and sorting algorithms.',
 55,
 'Intermediate');

INSERT INTO Module (course_id, module_title, module_order, module_type)
VALUES
(4, 'Arrays & Linked Lists (Intro)', 1, 'VIDEO'),
(4, 'Stack & Queue Explained', 2, 'VIDEO'),
(4, 'Trees & Graphs Basics', 3, 'VIDEO'),
(4, 'Sorting & Searching Algorithms', 4, 'VIDEO'),
(4, 'Mini Project – Data Structure Implementation', 5, 'PROJECT'),
(4, 'Final Quiz – Data Structures', 6, 'QUIZ');

INSERT INTO Video (module_id, video_title, video_url)
VALUES
(25, 'Arrays & Linked Lists (Intro)',
 'https://www.youtube.com/watch?v=6w3L4Y1PI5M'),

(26, 'Stack & Queue Explained',
 'https://www.youtube.com/watch?v=wjI1WNcIntg'),

(27, 'Trees & Graphs Basics',
 'https://www.youtube.com/watch?v=oSWT8gNZ5oA'),

(28, 'Sorting & Searching Algorithms',
 'https://www.youtube.com/watch?v=ZZuD6iUe3Pc');
 
 -- COURSE-5,MOUDLE,VIDEO

INSERT INTO Course (title, description, duration, level)
VALUES
('Introduction to AI & Machine Learning',
 'Learn AI fundamentals, supervised learning, preprocessing and model evaluation techniques.',
 60,
 'Intermediate');


INSERT INTO Module (course_id, module_title, module_order, module_type)
VALUES
(5, 'What is AI & Machine Learning?', 1, 'VIDEO'),
(5, 'Data Preprocessing in ML', 2, 'VIDEO'),
(5, 'Supervised Learning Explained', 3, 'VIDEO'),
(5, 'Model Evaluation & Accuracy Metrics', 4, 'VIDEO'),
(5, 'Mini Project – Build a Simple ML Model', 5, 'PROJECT'),
(5, 'Final Quiz – AI & ML Basics', 6, 'QUIZ');

INSERT INTO Video (module_id, video_title, video_url)
VALUES
(31, 'What is AI & Machine Learning?',
 'https://www.youtube.com/watch?v=ukzFI9rgwfU'),

(32, 'Data Preprocessing in ML',
 'https://www.youtube.com/watch?v=0xVqLJe9_CY'),

(33, 'Supervised Learning Explained',
 'https://www.youtube.com/watch?v=nt63k3bfXS0'),

(34, 'Model Evaluation & Accuracy Metrics',
 'https://www.youtube.com/watch?v=85dtiMz9tSo');

-- QUIZ RECORD


INSERT INTO Quiz (module_id, quiz_title)
VALUES
(6,  'C++ Final Quiz'),
(12, 'DBMS Final Quiz'),
(24, 'Frontend Final Quiz'),
(30, 'Data Structures Final Quiz'),
(36, 'AI & ML Final Quiz');

-- QUESTION RECORDS

-- c-1
INSERT INTO Question
(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
(1, 'Which symbol is used to end a statement in C++?',
 'Colon', 'Semicolon', 'Dot', 'Comma', 'B'),

(1, 'Which keyword is used to define a function?',
 'function', 'define', 'void', 'func', 'C'),

(1, 'Which data type stores whole numbers?',
 'int', 'float', 'char', 'double', 'A');

-- c-2

INSERT INTO Question
(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
(2, 'What does DBMS stand for?',
 'Database Main System',
 'Database Management System',
 'Data Backup System',
 'Data Managing Service',
 'B'),

(2, 'Which SQL command is used to create a table?',
 'INSERT', 'CREATE', 'UPDATE', 'SELECT', 'B'),

(2, 'Primary key must be?',
 'Duplicate', 'Null', 'Unique', 'Optional', 'C');

-- c-3

INSERT INTO Question
(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
(3, 'HTML is used for?',
 'Styling', 'Structure', 'Database', 'Security', 'B'),

(3, 'CSS is used for?',
 'Structure', 'Styling', 'Logic', 'Database', 'B'),

(3, 'JavaScript is mainly used for?',
 'Styling', 'Database', 'Interactivity', 'Storage', 'C');

-- c-4

INSERT INTO Question
(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
(4, 'Stack follows which principle?',
 'FIFO', 'LIFO', 'Random', 'Priority', 'B'),

(4, 'Queue follows?',
 'LIFO', 'FIFO', 'Tree', 'Graph', 'B'),

(4, 'Binary search works on?',
 'Sorted data', 'Unsorted data', 'Random data', 'None', 'A');

-- c-5

INSERT INTO Question
(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
(5, 'AI stands for?',
 'Artificial Intelligence',
 'Automated Internet',
 'Advanced Interface',
 'Applied Informatics',
 'A'),

(5, 'Machine Learning is a subset of?',
 'DBMS', 'AI', 'Networking', 'OS', 'B'),

(5, 'Accuracy is used to measure?',
 'Speed', 'Performance of model', 'Storage', 'Memory', 'B');





