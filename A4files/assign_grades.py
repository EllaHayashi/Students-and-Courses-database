import sys, csv, psycopg2
psql_user = 'ellahayashi'
psql_db = 'ellahayashi'
psql_password = 'V00184392'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432



if len(sys.argv) <2:
	print("usage: %s <input file>", file=sys.stderr)
	sys.exit(0)

input_filename = sys.argv[1]

#Open your DB connection here
conn = psycopg2.connect(dbname = psql_db, user = psql_user, password = psql_password, host = psql_server, port = psql_port)

cursor = conn.cursor()

with open(input_filename) as f:
	for row in csv.reader(f):
		if len(row)==0:
			continue #ignore blank rows
		if len(row) !=4:
			print("Error: Invalid input line \"%s\""%(','.join(row)), file = sys.stderr)
			exit(0)		
			break
		course_code, term, student_id, grade = row
		finalGrade = row[3]
				
		insert_statment = cursor.mogrify("update enrolled set grade = %s where student_id = %s and course_code = %s and term_code = %s;",(grade, student_id, course_code, term))
		try:
			cursor.execute(insert_statment)
		except psycopg2.PtrogrammingError as err:
			print("Caught a ProgrammingError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.IntegrityError as err:
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.InternalError as err:
			print("Caught an InternalError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		


conn.commit()
cursor.close()
conn.close()





