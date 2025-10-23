import os
import pymysql
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class FitnessServices:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT')),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }

    
    def authenticate(self, username, password):
        con = pymysql.connect(**self.db_config)
        curs = con.cursor(pymysql.cursors.DictCursor)
        try:
            query = "SELECT * FROM userlogin WHERE username=%s AND password=%s"
            curs.execute(query, (username, password))
            result = curs.fetchone()
            return result
        except Exception as e:
            print("Error in authenticate:", e)
            return None
        finally:
            curs.close()
            con.close()

   
    def newprofile(self, name, age, gender, height, weight, foodtype, steps_pr_day):
        con = pymysql.connect(**self.db_config)
        curs = con.cursor()
        try:
            query = """
                INSERT INTO newprofile (name, age, gender, height, weight, foodtype, steps_pr_day)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            curs.execute(query, (name, age, gender, height, weight, foodtype, steps_pr_day))
            con.commit()
            return True
        except pymysql.err.IntegrityError:
            return "duplicate"
        except Exception as e:
            print("Error in newprofile:", e)
            return False
        finally:
            curs.close()
            con.close()

    def report(self):
        con = pymysql.connect(**self.db_config)
        curs = con.cursor(pymysql.cursors.DictCursor)
        try:
            query = "SELECT name, age, gender, height, weight, foodtype FROM newprofile"
            curs.execute(query)
            data = curs.fetchall()
            return data
        except Exception as e:
            print("Error in report:", e)
            return []
        finally:
            curs.close()
            con.close()

  
    def change(self, name, height, weight, foodtype):
        con = pymysql.connect(**self.db_config)
        curs = con.cursor()
        try:
            query = "UPDATE newprofile SET height=%s, weight=%s, foodtype=%s WHERE name=%s"
            curs.execute(query, (height, weight, foodtype, name))
            con.commit()
            return True
        except Exception as e:
            print("Error in change:", e)
            return False
        finally:
            curs.close()
            con.close()

    def delete1(self, name):
        con = pymysql.connect(**self.db_config)
        curs = con.cursor()
        try:
            query = "DELETE FROM newprofile WHERE name=%s"
            curs.execute(query, (name,))
            con.commit()
            return True
        except Exception as e:
            print("Error in delete1:", e)
            return False
        finally:
            curs.close()
            con.close()

    def search_user(self, name):
        con = pymysql.connect(**self.db_config)
        curs = con.cursor(pymysql.cursors.DictCursor)
        try:
            query = "SELECT * FROM newprofile WHERE name=%s"
            curs.execute(query, (name,))
            data = curs.fetchone()
            if data:
                return data
            else:
                return {"message": "User not found"}
        except Exception as e:
            print("Error in search_user:", e)
            return {"message": "Error occurred"}
        finally:
            curs.close()
            con.close()
