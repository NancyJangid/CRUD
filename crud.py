import pyodbc
from fastapi import FastAPI
import json

database_connection ="DRIVER={SQL Server};SERVER=43.204.45.205,1560;DATABASE=HSRPOEM;UID=R3480;PWD=Yashwant@13"
conn = pyodbc.connect(database_connection)
cursor = conn.cursor()
cursor.execute("Select * from Items")
data = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]


cursor.close()
conn.close()

app = FastAPI()
@app.get("/getdata")
def GET():
    conn = pyodbc.connect(database_connection)
    cursor = conn.cursor()
    cursor.execute("Select * from Items")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    dic = {}
    for row in data:
        for y in range (len(columns)):
            dic[columns[y]] = row[y]  

    records=json.dumps(dic, default=str)

    return {records}
