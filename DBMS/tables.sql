CREATE DATABASE lms_db;

USE lms_db;


-- TABLE USER

CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('STUDENT', 'ADMIN') DEFAULT 'STUDENT'
);

-- COURESE TABLE

CREATE TABLE Course (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    duration INT NOT NULL,
    level VARCHAR(50) NOT NULL
);


-- ENROLLMENT TABLE 

CREATE TABLE Enrollment (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_date DATE NOT NULL,
    status ENUM('ACTIVE', 'COMPLETED') DEFAULT 'ACTIVE',
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);



-- MOUDLE TABLE

  CREATE TABLE Module (
    module_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    module_title VARCHAR(255) NOT NULL,
    module_order INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);



-- VIDEO PROGRESS TABLE TABLE 

CREATE TABLE Video_Progress (
    progress_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    lesson_id INT NOT NULL,
    watched_percentage INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (lesson_id) REFERENCES Lesson(lesson_id)
);


-- PROJECT SUBMISSION TABLE 

CREATE TABLE project_submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    project_link VARCHAR(255) NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE (user_id, course_id)
);

-- CIRTIFICATION TABLE 

CREATE TABLE certificates (
    certificate_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE (user_id, course_id)
);

-- LESSON TABLE

CREATE TABLE Lesson (
    lesson_id INT PRIMARY KEY AUTO_INCREMENT,
    module_id INT NOT NULL,
    lesson_title VARCHAR(255) NOT NULL,
    video_url VARCHAR(500) NOT NULL,
    duration INT NOT NULL,
    FOREIGN KEY (module_id) REFERENCES Module(module_id)
);

-- QUIZ TABLE

 CREATE TABLE Quiz (
    quiz_id INT PRIMARY KEY AUTO_INCREMENT,
    module_id INT NOT NULL,
    quiz_title VARCHAR(255) NOT NULL,
    FOREIGN KEY (module_id) REFERENCES Module(module_id)
);


-- Question Table

CREATE TABLE Question (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    quiz_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_option CHAR(1) NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES Quiz(quiz_id)
);

-- Quiz_Attempt Table

CREATE TABLE Quiz_Attempt (
    attempt_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    quiz_id INT NOT NULL,
    score INT NOT NULL,
    attempt_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(quiz_id)
);

-- Assignment Table

CREATE TABLE Assignment (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    module_id INT NOT NULL,
    assignment_title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (module_id) REFERENCES Module(module_id)
);

-- Project_Submission Table

CREATE TABLE Project_Submission (
    submission_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    assignment_id INT NOT NULL,
    github_link VARCHAR(500) NOT NULL,
    submitted_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id)
);

-- Certificate Table

CREATE TABLE Certificate (
    certificate_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    issued_date DATE NOT NULL,
    certificate_code VARCHAR(100) NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- video table

CREATE TABLE Video (
    video_id INT PRIMARY KEY AUTO_INCREMENT,
    module_id INT NOT NULL,
    video_title VARCHAR(255) NOT NULL,
    video_url VARCHAR(500) NOT NULL,
    video_order INT NOT NULL,
    FOREIGN KEY (module_id) REFERENCES Module(module_id)
);





SHOW tables;


SELECT @@foreign_key_checks;




