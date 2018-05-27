import psycopg2, sys

psql_user = 'ellahayashi'
psql_db = 'ellahayashi'
psql_password = 'V00184392'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname = psql_db, user = psql_user, password = psql_password, host = psql_server, port = psql_port)

cursor = conn.cursor()

def print_header(student_id, student_name):
	print("Transcript for %s (%s)"%(str(student_id), str(student_name)))

def print_row(course_term, course_code, course_name, grade):
	if grade is not None:
		print("%6s %10s %-35s   GRADE: %s"%(str(course_term), str(course_code), str(course_name), str(grade)))
	else:
		print("%6s %10s %-35s   (NO GRADE ASSIGNED)"%(str(course_term), str(course_code), str(course_name)))

if len(sys.argv)<2:
	print('Usage: %s <student id>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)

student_id = sys.argv[1]

insert_statement = cursor.mogrify("select student_id, name from students where student_id = %s;",(student_id,))
cursor.execute(insert_statement)

row = cursor.fetchone()
if row is None:
	print("No such student")
	exit(0)
print_header(row[0], row[1])

insert_statement2 = cursor.mogrify("select term_code, course_code, course_name, grade from enrolled natural join course_offerings natural join students where student_id = %s;",(student_id,))
cursor.execute(insert_statement2)

while True:
	row = cursor.fetchone()
	if row is None:
		break
	else:
		print_row(row[0],row[1],row[2],row[3])

cursor.close()
conn.close()











