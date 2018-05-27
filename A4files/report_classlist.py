import psycopg2, sys

psql_user = 'ellahayashi'
psql_db = 'ellahayashi'
psql_password = 'V00184392'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname = psql_db, user = psql_user, password = psql_password, host = psql_server, port = psql_port)

cursor = conn.cursor()

def print_header(course_code, course_name, term, instructor_name):
	print("Class list for %s (%s)"%(str(course_code), str(course_name)))
	print("   Term %s"%(str(term), ))
	print("   Instructor: %s"%(str(instructor_name),))

def print_row(student_id, student_name, grade):
	if grade is not None:
		print("%10s %-25s   GRADE: %s"%(str(student_id), str(student_name), str(grade)))
	else:
		print("%10s %-25s"%(str(student_id),str(student_name)))

def print_footer(total_enrolled, max_capacity):
	print("%s/%s students enrolled"%(str(total_enrolled),str(max_capacity),))

if len(sys.argv)<3:
	print('Usage: %s <course code> <term>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)

course_code, term = sys.argv[1:3]

insert_statement = cursor.mogrify("select distinct course_code, course_name, term_code, instructor_name from enrolled natural join course_offerings where course_code = %s and term_code = %s;", (course_code, term))

cursor.execute(insert_statement)
row = cursor.fetchone()
if row is None:
	print("This is not a class")
	exit(0)
else:
	print_header(row[0], row[1], row[2], row[3])

insert_statement2 = cursor.mogrify("select distinct student_id, name, grade from enrolled natural join students where course_code = %s and term_code = %s;",(course_code, term))
cursor.execute(insert_statement2)

rows_found = 0
while True:
	row = cursor.fetchone()
	if row is None:
		break
	rows_found +=1
	print_row(row[0],row[1],row[2])

insert_statement3 = cursor.mogrify("select distinct count(*) over (partition by term_code, course_code) as number_enrolled, max_capacity from enrolled natural join course_offerings where course_code = %s and term_code = %s;",(course_code, term))
cursor.execute(insert_statement3)
row = cursor.fetchone()
print_footer(row[0], row[1])


cursor.close()
conn.close()










