import mysql.connector

def Conectar():
    try:
        conexion = mysql.connector.connect(
        host="localhost",          
        user="root",         
        password="M4tsum0t017*",   
        database="TopNails" 
    )
    except Exception as e:
        print("Ocurrió un error:", e)

    return conexion

con=Conectar()

if con.is_connected():
    print("Exito")
    
    
    
try:
   
    cursor = con.cursor()
    
   
    cursor.execute("SELECT * FROM persona")
    resultados = cursor.fetchall()

    for fila in resultados:
        print(fila)
finally:
    
    con.close()