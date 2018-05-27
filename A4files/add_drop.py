import sys, csv, psycopg2

psql_user = 'ellahayashi'
psql_db = 'ellahayashi'
psql_password = 'V00184392'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432



if len(sys.argv)<2:
	print("Usage: %s <input file>", file=sys.stderr)
	sys.exit(0)

input_filename = sys.argv[1]

conn = psycopg2.connect(dbname = psql_db, user = psql_user, password = psql_password, host = psql_server, port = psql_port)
cursor = conn.cursor()




with open(input_filename) as f:
	for m in csv.reader(f):
		if len(m)==0:
			continue #ignore blank rows
		if len(m) != 5:
			print("Error: Invalid input line \"%s\""%(','.join(m)),file=sys.stderr)
			exit(0)
			break
		
		add_or_drop = m[0]
		student_id, student_name, course_code, term = m[1:5]
	
		if add_or_drop == 'ADD':
			insert_statment1 = cursor.mogrify("insert into students values(%s, %s);", (student_id, student_name))		
			cursor.execute(insert_statment1)
			
			insert_statment2 = cursor.mogrify("insert into enrolled values (%s, %s, %s);", (student_id, course_code, term))	
			try:
				cursor.execute(insert_statment2)
	#			conn.commit()
			except psycopg2.ProgrammingError as err:
				print("Caught a ProgrammingError:", file = sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()
			except psycopg2.IntegrityError as err:
				print("Error when trying to insert row:", student_id, student_name, course_code, term)	
				print(err,file=sys.stderr)
				conn.rollback()
				exit(0)
			except psycopg2.InternalError as err:
				print("Error when trying to insert row:", student_id, student_name, course_code, term)
				print(err,file=sys.stderr)
				conn.rollback()
				exit(0)

		elif add_or_drop == 'DROP':

			insert_statment = cursor.mogrify("delete from enrolled where student_id = %s and course_code = %s and term_code = %s;",(student_id, course_code, term))



			try:
				cursor.execute(insert_statment)
	#			conn.commit()
			except psycopg2.ProgrammingError as err:
				print("Caught a ProgrammingError:", file = sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()
			except psycopg2.IntegrityError as err:
				print("Error when trying to insert row:", student_id, student_name, course_code, term)	
				print(err,file=sys.stderr)
				conn.rollback()
				exit(0)
			except psycopg2.InternalError as err:
				print("Error when trying to insert row:", student_id, student_name, course_code, term)
				print(err,file=sys.stderr)
				conn.rollback()
				exit(0)

		else:
			print("ADD or DROP statement incorect")



conn.commit()
cursor.close()
conn.close()





