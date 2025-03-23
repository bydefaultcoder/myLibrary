from django.db import connection

def get_libraries(pageQuery):
    with connection.cursor() as cursor:
        to_fetch = ['location_id', 'location_name','timming','opening_time','closing_time','discription','number_of_seats']
        query = f"SELECT {",".join(to_fetch)} FROM booking_location "+pageQuery
        # WHERE status='exposed'"+pageQuery
        print(query)
        cursor.execute(query)
        print(cursor.description)
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
    return results

def get_libraries(id,pageQuery):
    with connection.cursor() as cursor:
        to_fetch = ['location_id', 'location_name','timming','opening_time','closing_time','discription','number_of_seats']
        query = f"SELECT {",".join(to_fetch)} FROM booking_location "+pageQuery
        # WHERE status='exposed'"+pageQuery
        print(query)
        cursor.execute(query)
        print(cursor.description)
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
    return results

def libraryDetail(pageQuery):
    with connection.cursor() as cursor:
        to_fetch = ['location_id', 'location_name','timming','opening_time','closing_time','discription','number_of_seats']
        query = f"SELECT {",".join(to_fetch)} FROM booking_location "+pageQuery
        # WHERE status='exposed'"+pageQuery
        print(query)
        cursor.execute(query)
        print(cursor.description)
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
    return results