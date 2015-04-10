Canvas Admin Scripts
====================

**commlister.py**

This script allows you to take a list of students and list their communication channels and addresses associated with the communication channel.


**course_copy_csv.py**

This script can take a csv file of course ids and copy a specified course into each of the courses.

**enroller.py**

This will enroll one user in multiple courses with a designated role

**enrollment_checker.py**

This will compare a csv of user ids and sections they are enrolled in from banner and checks to see if their enrollment exists
in Canvas.

**quiz_submission_ip_addresses.py**

This will collect quiz submissions for a given quiz and collect the start and end date and time of each submission and
query the student's pageviews and returns the first IP address that is returned during the period they took the quiz.

**user_id_to_canvas_id.py**

This will convert a students sis_user_id to their Canvas id. This script takes a csv file as a commandline argument 
and uses that for the list of students. e.g. (user_id_to_canvas_id.py student_list.csv)