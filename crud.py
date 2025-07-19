import pyodbc
from fastapi import FastAPI
import json
from pydantic import BaseModel

database_connection ="DRIVER={SQL Server};SERVER=43.204.45.205,1560;DATABASE=HSRPOEM;UID=R3480;PWD=Yashwant@13"
conn = pyodbc.connect(database_connection)
cursor = conn.cursor()
cursor.execute("Select * from Items")
data = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
print(columns,data)


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


class Item(BaseModel):
    Name: str | None = None
    Description: str | None = None
    Price: int | None = None


@app.post("/insertdata")
def Insert_data(item: Item):
    name = item.Name
    price = item.Price
    desc = item.Description

    lst = [name, desc, price]

    with pyodbc.connect(database_connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"Insert into Items (Name, Description, Price) values (?,?,?)", lst)
            
    return ("Data inserted successfully") 

    #         data = cursor.fetchall()
    #         columns = [desc[0] for desc in cursor.description]
            
    # dic = {}
    # for row in data:
    #     for y in range (len(columns)):
    #         dic[columns[y]] = row[y]  

    # records=json.dumps(dic, default=str)

    # return {records}