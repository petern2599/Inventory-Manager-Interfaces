import psycopg2

class InventoryDBConnector():
    def __init__(self):
        pass

    def connect_to_db(self):
        self.connector = psycopg2.connect(database="inventory",
                                        host="localhost",
                                        user="postgres",
                                        password="password",
                                        port=5432)
        
        self.cursor = self.connector.cursor()
        

    def query_db(self,query):
        print("Performing current query...")
        self.cursor.execute(query)
        print(self.cursor.fetchone())

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