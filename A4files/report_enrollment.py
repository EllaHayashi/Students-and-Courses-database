import psycopg2

psql_user = 'ellahayashi'
psql_db = 'ellahayashi'
psql_password = 'V00184392'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname = psql_db,user=psql_user,password = psql_password, host = psql_server, port = psql_port)

cursor = conn.cursor()
cursor.execute("""select distinct * from(
			select term_code, course_code, course_name, instructor_name, count(*) over(partition by term_code, course_code) as number_enrolled, max_capacity
			from enrolled natural join course_offerings) as X
		union
		select distinct term_code, course_code, course_name, instructor_name, 0 as number_enrolled, max_capacity
		from
			(select term_code, course_code, course_name, instructor_name, max_capacity
				from course_offerings
			except
			select term_code, course_code, course_name, instructor_name, max_capacity
				from course_offerings natural join enrolled) as Y
		order by term_code, course_code;""")

rows_found = 0
while True:
	row = cursor.fetchone()
	if row is None:
		break
	rows_found+=1
	print("%6s %10s %-35s %-25s %s/%s"%(row[0], row[1], row[2], row[3], row[4], row[5]))

conn.commit()
cursor.close()
conn.close()






