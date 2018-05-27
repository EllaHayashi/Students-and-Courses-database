import sys,csv,psycopg2
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
		if len(m)<4:
			print("Error: Invalid input line \"%s\""%(','.join(m)), file=sys.stderr)
			exit(0)
			break
		code, name, term, instructor, capacity = m[0:5]
		prerequisites = m[5:] #list of zero or more items
		insert_statment1 = cursor.mogrify("insert into course values(%s);", (code,))

		insert_statment2 = cursor.mogrify("insert into course_offerings values (%s,%s,%s,%s,%s);", (code,name,term,instructor,capacity))

		try:	
			cursor.execute(insert_statment1)
		except psycopg2.ProgrammingError as err:
			print("Caught a ProgrammingError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.IntegrityError as err:
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.InternalError as err:
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()



		try:
			cursor.execute(insert_statment2)
		except psycopg2.ProgrammingError as err:
			print("Caught a ProgrammingError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.IntegrityError as err:
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.InternalError as err:
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()



		for i in range(len(prerequisites)):
			
			insert_statment3 = cursor.mogrify("insert into prerequisites values (%s,%s,%s);", (code, term, prerequisites[i]))
			try:
				cursor.execute(insert_statment3)
			except psycopg2.ProgrammingError as err:
				print("Caught a ProgrammingError:",file=sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()
			except psycopg2.IntegrityError as err:
				print("Caught an IntegrityError:",file=sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()
			except psycopg2.InternalError as err:
				print("Caught an IntegrityError:",file=sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()


conn.commit()
cursor.close()
conn.close()






