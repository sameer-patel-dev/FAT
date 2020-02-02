import time
import hashlib


class ErrorThrows:
    error_code_timeout = 0 # timeout will be 1 for timeout error
    error_code_amount  = 0 # if owned money is less than sending amount, value will go 1
    error_code_stock   = 0 # if stock is less than amount ordered then value goes 1

class Person:
    # Base class for people
    def __init__(self):
        self.person_name=''
        self.unique_id=0
        self.money=0
        self.personal_details={}

    def createPerson(self,name='',current_money=0,personal_details={}):
        self.setName(name)
        self.setMoney(current_money)
        self.setPersonalDetails(personal_details)

    def setName(self,name=''):
        self.person_name=name

    def getName(self):
        return self.person_name

    def setUniqueId(self,UniqueId=0):
        self.unique_id=UniqueId
    def getUniqueId(self):
        return self.unique_id

    def setPersonalDetails(self,setDetails={}):
        self.personal_details=setDetails
    def getPersonalDetails(self):
        return self.personal_details

    def setMoney(self,initialMoney=0):
        self.money=initialMoney
    def getMoney(self):
        return self.money

    def receiveMoney(self,received_money=0):
        self.money+=receiveMoney
    def sendMoney(self,send_money=0):
        if(self.money>=send_money):
            self.money-=send_money
            ErrorThrows.error_code_amount=0
        else:
            ErrorThrows.error_code_amount=1

class Thing:
    #Base class for thing ( buy & sell )
    def __init__(self):
        self.thing_name=''
        self.price = 0
        self.in_stock = 0
        self.attributes = {}


    def createThing(self,thing_name='',current_price=0,current_stock=0,attrs={}):
        self.setThingName(thing_name)
        self.setPrice(current_price)
        self.setStock(current_stock)
        self.setAttributes(attrs)

    def setPrice(self,MRP=0):
        self.price = MRP
    def getPrice(self):
        return self.price

    def setThingName(self,settingNameThing=''):
        self.thing_name = settingNameThing
    def getThingName(self):
        return self.thing_name

    def setAttributes(self,settingAttributes={}):
        self.attributes=settingAttributes

    def setStock(self,initialStock=0):
        self.in_stock=initialStock
    def getStock(self):
        return self.in_stock
    def increaseStock(self,getStock=0):
        self.in_stock+=int(getStock)
    def reduceStock(self,soldStock=0):
        if(soldStock<=self.in_stock):
            self.in_stock -= soldStock
            ErrorThrows.error_code_stock=0
        else:
            ErrorThrows.error_code_stock=1


class Horticulture:
    # fruits
    def __init__(self):
        self.plants = []
    def addPlant(self,some_Thing=Thing()):
        # give Thing object
        self.plants.append(some_Thing)
    def getPlants(self):
        return self.plants

class Agriculture:
    # veggies
    def __init__(self):
        self.plants = []
    def addPlant(self,some_Thing=Thing()):
        # give Thing object
        self.plants.append(some_Thing)
    def getPlants(self):
        return self.plants

class Floriculture:
    # flowers
    def __init__(self):
        self.plants = []
    def addPlant(self,some_Thing=Thing()):
        # give Thing object
        self.plants.append(some_Thing)
    def getPlants(self):
        return self.plants


class Farmer(Person):
    def __init__(self):
        super().__init__()
        self.plants=[]
        self.horticulture_plants=Horticulture()
        self.agriculture_plants =Agriculture()
        self.floriculture_plants=Floriculture()
        # Farmer Now Has
        # self.money : set,get,send,receive
        # self.personalDetails : set,get


    def setPlants(self,fruits=Horticulture(),veggies=Agriculture(),flowers=Floriculture()):
        self.horticulture_plants=fruits
        self.agriculture_plants =veggies
        self.floriculture_plants=flowers


    def getAllPlants(self):
        return {'horticulture':self.horticulture_plants,'agriculture':self.agriculture_plants,'floriculture':self.floriculture_plants}

class Customer(Person):
    def __init__(self):
        super().__init__()
        # Farmer Now Has
        # self.money : set,get,send,receive
        # self.personalDetails : set,get


def hashString(sampleString=''):
    return hashlib.sha256((sampleString.encode())).hexdigest()


class Transaction:
    def __init__(self,sender=Person(),receiver=Person()):
        self.sender  =sender.getName()
        self.receiver=receiver.getName()
        self.message=''

    def createTextTransaction(self,message,sender,receiver):
        sender_sends = " " +sender+" sent "
        receiver_recv= " to "+receiver
        self.message=self.message+"\n"+sender_sends+message+receiver_recv

    def checkValidity(self,buyer=Customer(),seller=Farmer(),plantName='',quantity=0):
        if(quantity < 1 ):
            ErrorThrows.error_code_stock = 1
            return "NULL"
        plant_stock =0
        plant_locator=[]

        listOfAllPlantsOnSale = []
        listOfAllPlantNames   = []
        dict_farmer_plants = seller.getAllPlants()
        plant_found = Thing()

        for plants_iter in dict_farmer_plants.keys():
            for random_plant in dict_farmer_plants[plants_iter].getPlants():
                listOfAllPlantsOnSale.append(random_plant)
                listOfAllPlantNames.append(random_plant.getThingName())

        if(plantName in listOfAllPlantNames):
            plant_found=listOfAllPlantsOnSale[listOfAllPlantNames.index(plantName)]

        for plants_iter in dict_farmer_plants.keys():
            if(plant_found in dict_farmer_plants[plants_iter].getPlants()):
                plant_locator.append(plants_iter)
                plants_avail = dict_farmer_plants[plants_iter].getPlants()
                plant_locator.append(plants_avail.index(plant_found))
                plant_stock = plants_avail[plant_locator[1]].getStock()
                break
        if(plant_stock >= quantity ):
            ErrorThrows.error_code_stock=0
            price_plant=plant_found.getPrice() * quantity
            #print(price_plant)
            if(price_plant > buyer.getMoney()):
                ErrorThrows.error_code_amount = 1
                return "NULL"
            else:
                buyer.setMoney(buyer.getMoney() - price_plant)
                seller.setMoney(seller.getMoney() + price_plant)
                new_stock = seller.getAllPlants()[plant_locator[0]].getPlants()[plant_locator[1]].getStock() - quantity
                seller.getAllPlants()[plant_locator[0]].getPlants()[plant_locator[1]].setStock(new_stock)

                return price_plant

        else:
            ErrorThrows.error_code_stock = 1
            return "NULL"


    def createAmountTransaction(self,buyer=Customer(),seller=Farmer(),plant=Thing(),quantity=0):
        plantName=plant
        if(type(plant) == str):
            plantName=plant
        else:
            plantName=plant.getThingName()
        total_price = self.checkValidity(buyer,seller,plantName,quantity)
        if(total_price != "NULL"):
            sender_sent  = " " +buyer.getName()+" bought "
            plant_info   = " " + str(quantity)+ " of " +plantName + " from "
            receiver_recv= " from " +seller.getName()
            for_price    = " for " + str(total_price) + " INR "
            self.message=self.message+"\n"+sender_sent+plant_info+receiver_recv+for_price
        else:
            if(ErrorThrows.error_code_stock):
                print("InSufficent Stock")
            if(ErrorThrows.error_code_amount):
                print("InSufficient Balance")

    def retriveTransaction(self):
        return self.message

    def closeTransaction(self):
        self.sender=0
        self.receiver=0
        self.message=''




class Block:
    def __init__(self,index=0,proof=0,previous_hash='',current_transaction=Transaction()):
        self.index=index
        self.proof=proof
        # this will the unique ID of each of the people ( Farmer / Customer )
        self.previous_hash = previous_hash
        self.transaction = current_transaction.retriveTransaction()
        self.timestamp=time.time()

    def get_self_hash(self):
        string_data = "{}{}{}{}{}".format(self.index,self.proof,self.previous_hash,self.transaction,self.timestamp)
        return hashString(string_data)

    def return_text(self):
        string_data = "index:{} | proof:{} | pre_hash:{} | transaction:{} | time:{} | current_hash:{} ".format(self.index,self.proof,self.previous_hash,self.transaction,self.timestamp,self.get_self_hash())
        return string_data

class ChainedBlock:
    index = 0
    def __init__(self):
        self.blockchain=[]
        self.createGenesis()

    def createNewBlock(self,proof,previous_hash,current_transaction=Transaction()):
        newBlock = Block(
            index=len(self.blockchain),
            proof=proof,
            previous_hash=previous_hash,
            current_transaction=current_transaction
        )
        self.blockchain.append(newBlock)

    def createGenesis(self):
        genesisBlock = self.createNewBlock(0,0,Transaction())

    def createNewTransaction(self):
        pass

    @staticmethod
    def createProofWork(previous_proof):
        proof = previous_proof+1
        while(proof+previous_proof)%7!=0:
            proof+=1
        return proof

    def get_last_block(self):
        return self.blockchain[-1]


class BlockChainInstance:
    def __init__(self):
        self.blockchain = []

    def startBlockChain(self):
        self.blockchain = ChainedBlock()

    def addTextBlock(self,message="",sender="",receiver=""):

        last_block = self.blockchain.get_last_block()
        last_proof = last_block.proof
        proof = self.blockchain.createProofWork(last_proof)

        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
        transaction = Transaction()
        transaction.createTextTransaction(message,sender,receiver)
        # get a transaction
        last_hash = last_block.get_self_hash()
        block = self.blockchain.createNewBlock(proof, last_hash,transaction)
        transaction.closeTransaction()


    def addAmountBlock(self,buyer_name='',buyer_money=0,buyer_details={},seller_name='',seller_money=0,seller_details={},plant_name='',plant_price=0,plant_stock=0,plant_attrs={},quantity_buy=0):

        last_block = self.blockchain.get_last_block()
        last_proof = last_block.proof
        proof = self.blockchain.createProofWork(last_proof)

        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)


        transaction = Transaction()
        buyer=Customer()
        #buyer.setMoney(5000)
        #buyer.setName("Gsec")
        buyer.createPerson(buyer_name,buyer_money,buyer_details)

        seller=Farmer()
        #seller.setMoney(1000)
        #seller.setName("CSI")
        seller.createPerson(seller_name,seller_money,seller_details)

        plant = Thing()
        #plant.setPrice(20)
        #plant.setStock(731)
        #plant.setThingName(plant_name)
        plant.createThing(plant_name,plant_price,plant_stock,plant_attrs)

        Horti = Horticulture()
        Horti.addPlant(plant)

        seller.setPlants(fruits=Horti)

        quantity = quantity_buy

        transaction.createAmountTransaction(buyer,seller,plant_name,quantity)

        # get a transaction
        last_hash = last_block.get_self_hash()
        block = self.blockchain.createNewBlock(proof, last_hash,transaction)
        transaction.closeTransaction()

    def displayBlockChain(self):
        for i in range(len(self.blockchain.blockchain)):
            print(" for no. : ",i)
            print(self.blockchain.blockchain[i].return_text())

if __name__ == "__main__":
    sample = " ---------------------------"
    bc = BlockChainInstance()
    bc.startBlockChain()
    bc.addTextBlock("This is Message","Sender","Receiver")
    bc.addAmountBlock('Buyer',5000,{},"Seller",1000,{},"plant",20,400,{},10)

    bc.addTextBlock("Another Message","Go go sender","By by receiver")

    bc.displayBlockChain()
    print(sample)
