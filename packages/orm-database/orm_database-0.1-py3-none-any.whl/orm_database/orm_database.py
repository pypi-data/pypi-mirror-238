import asyncpg


class PostgreSQL:
    def __init__(self,host:str,user:str,password:str,database:str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    async def start(self):
        self.db = await asyncpg.connect(host=self.host,user=self.user,password=self.password,database=self.database)



        
        
   
    async def teble_create(self,table:str,field:dict):
        query = f"CREATE TABLE {table} ("
        filed_key = list(field.keys())
        for a in filed_key:
            query = query + a + " " + field[a] + " ,"
        query =  query[:-1]
        query = query + ")"
        await self.db.execute(query)
        await self.db.close()
        
        
        

    async def insert_value(self,table:str,value:dict):
        query = f"INSERT INTO {table}  ( "
        filed_key = list(value.keys())
        for a in filed_key:
            query = query +" " + a + " " +","
        query =  query[:-1]
        query = query + ")"
        query = query + " VALUES ("
        filed_value = list(value.values())
        for a in filed_value:
            query = query +" '" + str(a) + "' " +","
        query = query[:-1]
        query = query + ")"
        await self.db.execute(query)
        await self.db.close()



    
    async def insert_values(self,table:str,values:list):
        for value in values:
            query = f"INSERT INTO {table}  ( "
            filed_key = list(value.keys())
            for a in filed_key:
                query = query +" " + a + " " +","
            query =  query[:-1]
            query = query + ")"
            query = query + " VALUES ("
            
            filed_value = list(value.values())
            for a in filed_value:
                query = query +" '" + str(a) + "' " +","
            query = query[:-1]
            query = query + ")"
            print(query)
            await self.db.execute(query)
            query = ""
        await self.db.close()    
        
        


    async def select_all(self,table:str,filed:list,all:bool=False):
        if all == True : 
            query = "SELECT * FROM " + table
        if all == False : 
            query = "SELECT "
            for a in filed:
                query = query + a + ","
            query = query[:-1]
            query = query + " FROM " + table 
            
        print(query)
        stmt = await self.db.prepare(query)
        #for a in stmt:
        result  = list(await stmt.fetch())
        data = {}
        data_row=[]
        for a in result:
            conter = 0 
            for b in a:
                data[filed[conter]]= b
                conter += 1
            data_row.append(dict(data))
        await self.db.close()
        print(data_row)
        return data_row


    

    async def select_columns(self,table:str,filed:dict):
        #'SELECT * FROM users WHERE name = $1'
        query = "SELECT * "
        query = query + " FROM "
        query = query  + table  + " WHERE "
        fileds = list(filed.keys())
        query = query + fileds[0]+"="+"$1"
        try: 
            row = dict(await self.db.fetchrow(query,filed[fileds[0]]))
            return row
        except:
            return None
            
        
    
        

        
    
    
    

    
    
    
    
    


import motor.motor_asyncio


class Mongodb:
    def __init__(self, url,name):
        self.url = url
        self.name=name

    async def start(self):
        self.clint = motor.motor_asyncio.AsyncIOMotorClient(self.url)
        self.database = self.clint[str(self.name)]

    async def insert_one(self, data: dict, collection: str):
        coll = self.database[collection]
        await coll.insert_one(data)
        return data

    async def find_one(self,data:dict,collection:str):
        coll = self.database[collection]
        result=await coll.find_one(data)
        return result
    async def find(self,data:dict,collection:str):
        coll = self.database[collection]
        result= coll.find(data)
        arraydata = []
        async for a in result:
            a['_id'] =str (a['_id'])
            arraydata.append(a)
        return arraydata
        
    async def read_collection(self, collection: str):
        coll = self.database[collection]
        data = coll.find({})
        arraydata = []
        async for a in data:
            a['_id'] =str (a['_id'])
            arraydata.append(a)
        return arraydata


    async def replace_one(self, find_data :dict, replace_data:dict ,collection:str):
        coll = self.database[collection]
        data =  await coll.replace_one(find_data,replace_data)
        if data == None: 
            return None 
        else: 
            return data


    async def update_one(self, find_data :dict, replace_data:dict ,collection:str):
        coll = self.database[collection]
        data =  await coll.update_one(find_data,{'$set':replace_data})
        if data == None: 
            return None 
        else: 
            return data