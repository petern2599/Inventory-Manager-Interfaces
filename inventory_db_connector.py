import psycopg2

class InventoryDBConnector():
    def __init__(self):
        pass

    def connect_to_db(self,db,host,user,password,port):
        self.connector = psycopg2.connect(database=db,
                                        host=host,
                                        user=user,
                                        password=password,
                                        port=port)
        
        self.cursor = self.connector.cursor()
        

    def insert_db(self,query):
        print("Performing current query...")
        self.cursor.execute(query)
        self.connector.commit()

    def close_connection(self):
        print("Closing connection to database...")
        self.connector.close()

if __name__ == "__main__":
    conn = InventoryDBConnector()
    try:
        conn.connect_to_db()
        print("Database connection established!")
        conn.query_db("SELECT * FROM inventory")
    except Exception as e:
        print("Could not connect to database!")
        print(e)