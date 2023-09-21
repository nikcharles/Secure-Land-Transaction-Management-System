# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 19:05:26 2023

@author: hp
"""

import hashlib
import random
import sys
import fileinput

r = 0
s = 0
#making over land transaction 
def modinv(a,m):
    a = a%m
    for x in range(1,m):
        if((a*x) % m == 1):
            return(x)
    return(1)

def isprime(num):
    for n in range(2,int(num**1/2)+1):
        if num%n==0:
            return False
    return True

def hasher(message):
    hash_val = hashlib.sha1(message.encode("UTF-8")).hexdigest()
    return hash_val

def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False
                
        if isPrime:
            prime_list.append(n)
    return prime_list



while(1):
    pl = primesInRange(101,999)
    p = random.choice(pl)

    temp=[]
    for q in range(2,p):
        if ((p-1)%q == 0) and isprime(q) and q>9:
            temp.append(q)
    if(len(temp) != 0):
        break
    
    
q=temp[0]
#print('\nThe value of p is: ',p)
#print('The value of q is: ',q)        
flag = True
while(flag):
   # h = int(input("Enter a value for h between 1 and (p-1) : "))
    h=random.randint(1,(p-1))
    if(1<h<(p-1)):
        g=1
        while(g==1):
            g = pow(h,int((p-1)/q)) % p
        flag = False
    else:
        print('Invalid Entry')
#print('\nThe value of g is: ',g)
#x = int(input('Enter a random value for x between 1 to (q-1): '))
x=random.randint(1, (q-1))
#print("\nThe private key(x) is: ",x)
y = (g**x) % p
#print("The public key(y) is: ",y)
def signature(name,p,q,g,x):
    with open(name) as file:
        text = file.read()
        hash_comp = hasher(text)
        #print("Hash of the document sent is: ",hash_comp)
    r = 0
    s = 0
    while(s==0 or r==0):
       # k = int(input('Enter a value for k(between 1 to (q-1)): '))
        k=random.randint(1,(q-1))
        r = ((pow(g,k))%p)%q
        i = modinv(k,q)
        hashed = int(hash_comp,16)
        s = (i*(hashed+(x*r))) % q
    return(r,s,k)
def verification(name,p,q,g,r,s,y):
    with open(name) as file:
        text = file.read()
        hash_comp = hasher(text)
        #print("Hash of the recieved document is: ",hash_comp)
        w = modinv(s,q)
        #print("\nValue of w is: ",w)
        hashed = int(hash_comp,16)
        u1 = (hashed*w) % q
        u2 = (r*w) % q
        v = ((pow(g,u1)*pow(y,u2))%p)%q
        #print("Value of u1 is: ",u1)
        #print("Value of u2 is: ",u2)
        #print("Value of v is: ",v)
        if(v==r):
            return(1)#valid document
        else:
            return(0)#invalid document
print()

#This will act as our repository
class buffer():
    #r = 0
    #owner_name = '0'
    
    def __init__(self,r,s,owner_name):
        self.r = r
        self.s = s
        self.owner_name = owner_name
        
    
argv = [] #database

#file_name=[r'C:\Users\hp\Desktop\crypto project\Land_1.txt', r'C:\Users\hp\Desktop\crypto project\Land_2.txt']
comp1 = signature(r'C:\Users\hp\Desktop\ism project\Land_1.txt',p,q,g,x)
#comp1 one is an array of data stored in the sequence as in signature functions reutrn.
argv.append(buffer(comp1[0],comp1[1],'nikhil'))
#print("test----r-", argv[0].r)
comp2 = signature(r'C:\Users\hp\Desktop\ism project\Land_2.txt',p,q,g,x)

argv.append(buffer(comp2[0],comp2[1],'selva'))

#DSA Environment is inserted 
#Argv[0] has data of hello.txt & can be edited
#Now code has to be made for transaction/exchange and start with testing
def transaction():
    print("in database: land1 land2")
    land_index=int(input("enter the land you want to access (1 for land 1 and similarly):"))
    onr_nam=input("enter owner name: ")
    onr_id=input("enter owner id: ")
    if(argv[land_index-1].owner_name==onr_nam):
        #main code here
        doc=input("enter the documents: ")
        temp=verification(doc, p, q, g, argv[land_index-1].r, argv[land_index-1].s, y)
        if(temp==1):
            print("the document is valid")
            print("the transaction is verified, proceed with payment\n")
            #payment code not considered as not the goal
            print("\npayment sucessful\n")
            new_onr=input("enter the new owner name: ")
            new_id=input("enter new owner id: ")
            old_data= hasher(onr_nam+str(argv[land_index-1].r)+str(argv[land_index-1].s)+"transaction")
            #cretae a record for old owner and related data
            #at the same time creating a un replicable modification in document
            count=0
            for i, line in enumerate(fileinput.input(doc, inplace=1)):
                count=count+1
                sys.stdout.write(line.replace(onr_nam, new_onr))
                if count == 27: 
                    sys.stdout.write("\n")
                    sys.stdout.write(old_data)
            for i, line in enumerate(fileinput.input(doc, inplace=1)):
                sys.stdout.write(line.replace(onr_id, new_id))
            print("the document is modified for future use")
            tmp_sign=signature(doc,p,q,g,x)
            argv[land_index-1].r=tmp_sign[0]
            argv[land_index-1].s=tmp_sign[1]
            argv[land_index-1].owner_name=new_onr
            print("the data base is updated")
        else:
            print("invalid document, modification occured.\n")  
    else:
        print("invalid owner name")
    print()
    return("")
    

def exchange():
    print("in database: land1 land2")
    land_1=int(input("enter the first land you want to access (1 for land 1 and similarly):"))
    onr_1=input("enter owner name for first land: ")
    onr_id_1=input("enter the owner id for first land: ")
    land_2=int(input("\n enter the second land you want to access (1 for land 1 and similarly):"))
    onr_2=input("enter owner name for second land: ")
    onr_id_2=input("enter the owner id for second land: ")
    if(argv[land_1-1].owner_name==onr_1 and argv[land_2-1].owner_name==onr_2):
        #main code here
        doc1=input("enter the documents for first land: ")
        temp1=verification(doc1, p, q, g, argv[land_1-1].r, argv[land_1-1].s, y)
        doc2=input("enter the documents for second land: ")
        temp2=verification(doc2, p, q, g, argv[land_2-1].r, argv[land_2-1].s, y)
        if(temp1==1 and temp2==1):
            #now change documents code
            #this has to be done
            print()
            print("the documents are valid and verified")
            print()
            print("proceed with excange")
            #argv[land_1-1].owner_name=onr_2
            old_1= hasher(onr_1+str(argv[land_1-1].r)+str(argv[land_1-1].s)+"exchange")
            count1=0
            for i, line in enumerate(fileinput.input(doc1, inplace=1)):
                count1=count1+1
                sys.stdout.write(line.replace(onr_1, onr_2))
                if count1 == 27: 
                    sys.stdout.write("\n")
                    sys.stdout.write(old_1)
            for i, line in enumerate(fileinput.input(doc1, inplace=1)):
                sys.stdout.write(line.replace(onr_id_1, onr_id_2))
            print("document of first land is updated")
            #argv[land_2-1].owner_name=onr_1
            old_2= hasher(onr_2+str(argv[land_2-1].r)+str(argv[land_2-1].s)+"exchange")
            count2=0
            for i, line in enumerate(fileinput.input(doc2, inplace=1)):
                sys.stdout.write(line.replace(onr_2, onr_1))
                count2=count2+1
                if count2 == 27: 
                    sys.stdout.write("\n")
                    sys.stdout.write(old_2)
            for i, line in enumerate(fileinput.input(doc2, inplace=1)):
                sys.stdout.write(line.replace(onr_id_2, onr_id_1))
            print()
            print("document of second land is updated")
            print()
            print("documents updated for future use")
            print()
            tmp_sign1=signature(doc1,p,q,g,x)
            argv[land_1-1].r=tmp_sign1[0]
            argv[land_1-1].s=tmp_sign1[1]
            argv[land_1-1].owner_name=onr_2
            print("first land database udated")
            tmp_sign2=signature(doc2,p,q,g,x)
            argv[land_2-1].r=tmp_sign2[0]
            argv[land_2-1].s=tmp_sign2[1]
            argv[land_2-1].owner_name=onr_1
            print("second land database updated")
            print()
            print("exchange sucessful")
        elif(temp1==0 and temp2==1):
            print("document of first land is modified")
        elif(temp1==1 and temp2==0):
            print("documnet of second land is modified")
        else:
            print("both documents are modified")
    elif(argv[land_1-1].owner_name!=onr_1 and argv[land_2-1].owner_name==onr_2):
        print("owner of first land is invalid")
    elif(argv[land_1-1].owner_name==onr_1 and argv[land_2-1].owner_name!=onr_2):
        print("owner of second land is invalid")
    else:
        print("invalid owners")
    return()
#the else wrong case return is not working check that
#in exchange code need to add code for appending to database after change
#in appending need to add a hash value in document as a record of previous changes 
#function for hash in file: hash(str(r)+str(s)+owner_name)


while(1):
    print('****MENU****')
    print('\n1.Transaction\n2.Exchange\n3.exit\n')
    ch = int(input('Enter your choice: '))
    if (ch==3):
        print('Thanks')
        break
    elif (ch==2):
        exchange()
    elif(ch==1):
        transaction()
    else:
        print("invalid")
    def choice(ch):
        switch = {1:transaction(),2:exchange(),3:''}
        return switch.get(ch,'Invalid')
    #print(choice(ch))