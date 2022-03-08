import sqlite3

conn = sqlite3.connect('dataMahasiswa.db')

class Mahasiswa:
    def __init__(self):
        self.__data = conn.execute("SELECT NIM from COMPANY")

    def getMahasiswa(self):
        return [x[0] for x in self.__data]
        
class ProfileMahasiswa:
    def __init__(self, nim=None, fullname=None):
        self.__isExist = False
        try:
            if nim != None:
                self.__data = conn.execute(f"SELECT NIM, BIRTHDAY, FULLNAME, IPK from COMPANY WHERE NIM = '{nim}'")
            elif fullname != None:
                self.__data = conn.execute(f"SELECT NIM, BIRTHDAY, FULLNAME, IPK from COMPANY WHERE FULLNAME = '{fullname}'")
            for row in self.__data:
                self.__nim = row[0]
                self.__birthday = row[1]
                self.__fullname = row[2]
                self.__ipk = row[3]
                self.__isExist = True
            
        except Exception as e:
            print("Profile Class:",e)
    def isExist(self):
        return self.__isExist

    def getNim(self):
        if self.isExist() == True:
            return self.__nim
        return None
    def getBirthday(self):
        if self.isExist() == True:
            return self.__birthday
        return None
    def getFullname(self):
        if self.isExist() == True:
            return self.__fullname
        return None
    def getIpk(self):
        if self.isExist() == True:
            return self.__ipk
        return None

    def saveProfile(self, nim, birthday, fullname, ipk):
        conn.execute(f"INSERT INTO COMPANY   (NIM,BIRTHDAY,FULLNAME,IPK) \
                        VALUES               ('{nim}','{birthday}','{fullname}','{ipk}')")
        self.__init__(nim, fullname)

def loadData():
    try:
        conn.execute('''CREATE TABLE COMPANY
                (
                NIM                 TEXT    PRIMARY KEY    NOT NULL,
                BIRTHDAY            TEXT,
                FULLNAME            TEXT,
                IPK                 INT
                );
        ''')
        print("Table created successfully")
    except Exception as e:
        print("loadData():",e)
loadData()

ProfileMahasiswa(nim="12301042001").saveProfile(
    "12301042001",
    "01-04-2001",
    "TEGAR MAULANA FAHREZA",
    3.73
)
print(ProfileMahasiswa(nim="12301042001").getFullname())

conn.close()
