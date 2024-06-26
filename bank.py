import mysql.connector as sql
import random
import time
import sys
from colorama import init,Fore, Back, Style
import pwinput as pw
import re
from datetime import date, datetime
import termtables as tt

mycon = sql.connect(host = '127.0.0.1', user = 'root', passwd ='', database = 'base_db')
mycursor = mycon.cursor()

# Database Creation
# mycursor.execute('CREATE DATABASE base_db')
# mycon.commit()

# Table Creation
# mycursor.execute('CREATE TABLE details_table(user_id INT(4) PRIMARY KEY AUTO_INCREMENT, lastname VARCHAR(20), othernames VARCHAR(40), username VARCHAR(20), address VARCHAR(100), email VARCHAR(40), phone_number VARCHAR(10), bvn VARCHAR(10), nin VARCHAR(10), acc_no VARCHAR(20), bal FLOAT(10), password VARCHAR(10), pin VARCHAR(4))')
# mycon.commit()


# mycursor.execute('CREATE TABLE transaction_table(trans_id INT(4) PRIMARY KEY AUTO_INCREMENT,username VARCHAR(20), trans_type VARCHAR(20), beneficiary_no VARCHAR(15), amount FLOAT(10), remark VARCHAR(10)), date_time VARCHAR(30), pin VARCHAR(4))')
# mycon.commit()



init()
class Bank:
    def __init__(self):
        self.intro()
    def intro(self):
        client = '*996#'
        inp = input("Enter *996# to continue: ")
        if inp == client:        
            self.landingPage()
        else:
            print(f'''{Fore.YELLOW} 
                  Warning! 
                  Do you want to terminate?
                  YES or NO?
                  {Style.RESET_ALL}
             ''')
            
            self.land()
    def land(self):        
        inp1 = input('Option: ')
        if inp1.upper() == "YES":
            print(Fore.RED + 'Exit!')
            sys.exit()
        elif inp1.upper() == "NO":
            self.intro()
        else:
            print(Fore.YELLOW+'Warning! Wrong Input, Try Again'+Style.RESET_ALL)
            self.land()

    def landingPage(self):
        print(f'''
                    Welcome to USSD banking
                    Press {Fore.GREEN}1 to CONTINUE{Style.RESET_ALL} or {Fore.GREEN}0 to EXIT{Style.RESET_ALL}
        ''')
        user = input('Select: ')
        if user == '1':
            self.presignIN()
        elif user == '0':
            print(f'{Fore.RED}Exit!{Style.RESET_ALL}')
            sys.exit()
        else:
            print(f'{Fore.RED} Invalid Input! Try again{Style.RESET_ALL}')  
            self.landingPage()  

    def presignIN(self):
        print(f"""
                    Select an option to continue
                    1. SignIn
                    2. Haven't gotten an account?
                    3. Exit
        """)  
        inp = input('Select: ')
        if inp == '1':
            self.pre() 
        elif inp == '2':
            self.signUp()
        elif inp == '3':
            print(Fore.RED + 'Exit!')
            sys.exit()
        else:
            print(f'{Fore.RED} Invalid Input! Try again{Style.RESET_ALL}')
            self.presignIN()
    
    # Confirmation Before SignIn
    def pre(self):
        print(Fore.GREEN+"  1"+Style.RESET_ALL+" for forgotten password"+Fore.GREEN+" ENTER "+Style.RESET_ALL+" to continue")
        user = input("Select: ")
        if user == '1':
            self.change()
        else: 
            self.signIn()  

    # Altering of Password
    def change(self):
        self.inp_user = input("Username: ")
        pwd1 = pw.pwinput('Change Password: ')
        pwd = pw.pwinput('Confirm Password: ')
        if pwd1 == pwd:
            print(Fore.YELLOW+'Updating...'+Style.RESET_ALL)
            query = "UPDATE details_table SET password=%s WHERE username=%s"
            val = (pwd, self.inp_user)
            mycursor.execute(query, val)
            mycon.commit() 
            time.sleep(2)
            print(Fore.GREEN+'Updated!'+Style.RESET_ALL)
            self.signIn()  
        elif pwd1 != pwd:
            print("Checking...") 
            time.sleep(2)
            print(Fore.RED+'Password does not match'+Style.RESET_ALL)
            print('Press 0 restart or 1 to signIn')  
            user = input('Select: ')
            if user == '0':
                self.presignIN()
            elif user == '1':
                self.signIn() 
            else:
                self.change()       

    # SignIn        
    def  signIn(self):  
            self.login = input('User name: ') 
            self.pwd =  pw.pwinput('Password: ')
            myquery = 'SELECT * FROM details_table WHERE username =%s AND password =%s'
            val = (self.login, self.pwd)
            mycursor.execute(myquery, val)

            details = mycursor.fetchall()

            if details:
                self.login = details[0][3]
                self.pwd = details[0][11]
                print(Fore.YELLOW+'Logging In...'+Style.RESET_ALL)
                time.sleep(2)
                print(Fore.GREEN+'Welcome'+Style.RESET_ALL)
                self.transaction_type()       
            else:
                    # print(Fore.RED+'Incorrect Username or Password'+Style.RESET_ALL)
                    
                print(Fore.RED+'Incorrect Username or Password'+Style.RESET_ALL)
                print('''
                        Select
                        1. Menu
                        0. Try again
                ''')
                user = input('Select: ')
                if user == '1':
                    self.pre()
                elif user == '0':
                    self.signIn()
                else:
                        print(Fore.RED+'Invalid Option!'+Style.RESET_ALL)
                        self.signIn()
   
    # SignUp  
    def  signUp(self):  
        self.lastname = input('Last Name: ')
        self.othernames = input('Other Names: ')
        self.address = input('Address: ')
        self.check()
        self.phone_check()
        self.username = input('Username: ')
    
        self.nin = random.randint(1000000000, 1100000000) 
        self.acc_no = random.randint(2000000000, 2100000000) 
        self.bal = float(0.0)
        self.bvn = random.randint(5000000000, 5100000000)
        self.signUp_password_check()
        self.signUp_pin_check()
        
        print(Fore.YELLOW+'Loading...'+Style.RESET_ALL)
        time.sleep(2)

        # SignIn Query
        try:
                    signup = "INSERT INTO details_table(lastname, othernames, username, address, email, phone_number, bvn, nin, acc_no, bal, password, pin) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (self.lastname.strip().upper(), self.othernames.strip().upper(), self.username.strip(), self.address.strip(), self.email.strip(), self.phone_number.strip(), self.bvn, self.nin, self.acc_no, self.bal, self.password, self.pin)
                    mycursor.execute(signup, val)
                    mycon.commit()


                    
        except:
            print(Fore.RED+"Username or Email Alredy Exits!"+Style.RESET_ALL)
            self.signUp() 
        else:
            print(f'''
                            Hi! {self.username}
                            Name {self.lastname.upper()} {self.othernames.upper()}
                            Account Number: {self.acc_no}       bvn: {self.bvn}     nin: {self.nin}
                            Phone Number: {self.phone_number}    Email: {self.email.strip()}         
                    ''')
            self.pre()       

    # Email Pattern Confirmation    
    def check(self):
        # defined pattern 
        pattern = re.compile(r'^[a-zA-Z0-9_%+]+@[a-zA-Z0-9_]+\.[a-zA-Z]+$')

        # matching of pattern
        self.email = input('Email: ')
        matches = pattern.search(self.email)
        if matches:
            # print(Fore.YELLOW+'Checking...'+Style.RESET_ALL)
            time.sleep(1)
        else:
            # print(Fore.YELLOW+'Checking...'+Style.RESET_ALL)
            time.sleep(1)
            print(Fore.RED+'Invalid Email'+Style.RESET_ALL)
            
            self.check()
    
    # Phone Number Pattern Confirmation
    def phone_check(self):
            self.phone_number = input('Phone number: +234 ')
            if re.match(r"^\d+$", self.phone_number):
                if len(self.phone_number) == 10:
                    pass
                else:
                    time.sleep(1)
                    print(Fore.RED+'Length must be 10'+Style.RESET_ALL) 
                    self.phone_check()       
            else:
                time.sleep(1)
                print(Fore.RED+'Phone number must be digit'+Style.RESET_ALL)
                self.phone_check()    

    # Checking Length of Password
    def signUp_password_check(self):
        self.password = pw.pwinput("Password: ")
        if len(self.password) != 6:
            print(Fore.RED+'Password should be Length of 6'+Style.RESET_ALL)
            self.signUp_password_check()
        elif len(self.password) == 6 and re.match(r"^[a-zA-Z]+$", self.password):
            pass   
        else:
            print(Fore.RED+'Password should be letters'+Style.RESET_ALL)
            self.signUp_password_check()

    # Checking Length of Pin
    def signUp_pin_check(self):
        pin = pw.pwinput("Enter your 4 digits pin: ")
        self.pin = pw.pwinput("Confirm pin: ")

        if re.match(r"^\d+$", self.pin):
                if len(self.pin) == 4 and pin == self.pin:
                    pass
                else:
                    time.sleep(1)
                    print(Fore.RED+'Length must be 4'+Style.RESET_ALL) 
                    self.signUp_pin_check()       
        else:
            time.sleep(1)
            print(Fore.RED+'Pin must be digit'+Style.RESET_ALL)
            self.signUp_pin_check()

    # Transaction Type
    def transaction_type(self):
        print('''
                Select to perform any trasanction
                1.  Transfer                 5. Account Balance
                2.  Deposit                  6. Transaction History
                3.  Airtime(self)            7. Pay Bills
                4.  Airtime(Others)          00. Inquiries
                22. Refresh                  0.  Exit                
        ''')
        inp = (input('Select: '))
        if inp == '1':
            self.trans ='Transfer'
            self.available()
            self.transfer()
        elif inp == '2':
            self.trans = 'Deposit'
            self.deposit()
        elif inp == '3':
            self.airtime_self()
        elif inp == '4':
            self.airtime()
        elif inp == '5':
            self.acc_bal()
        elif inp == '6':
            self.trans_history()
        elif inp == '7':
            self.bills()
        elif inp == '00':
            self.inq()
        elif inp == '0':
            print('Loading...')
            time.sleep(2)
            print(Fore.RED+'Exit!'+Style.RESET_ALL)
            sys.exit()
        elif inp == '22':
            print(Fore.YELLOW+"refreshing..."+Style.RESET_ALL)
            time.sleep(5)
            print(Fore.GREEN+'refreshed'+Style.RESET_ALL)
            time.sleep(1)
            self.transaction_type()
        else:
            print(Fore.RED+'Invalid Input!'+Style.RESET_ALL)
            self.transaction_type()

    # Registered Account
    def available(self):
            mycursor.execute('SELECT username, acc_no, lastname, othernames FROM details_table')
            rows = mycursor.fetchall()
            # table = PrettyTable()
            # table.field_names = [i[0] for i in mycursor.description]
            # for row in rows:
            #     table.add_row(row)
            header = ["username", "acc_no", "lastname", "othernames"]
            print(Fore.YELLOW+'Fetching Available Customers...'+Style.RESET_ALL)
            time.sleep(2)
            tt.print(rows, header)    
            # print(f'{Back.BLUE}{table}{Style.RESET_ALL}')
            self.acc_name()

    # Account Name Verification
    def acc_name(self):
        self.user = input("Beneficiary's Username: ")
        self.beneficiary = input('Account No: ')  
        if len(self.beneficiary) == 10:
            query = "SELECT * FROM details_table WHERE username=%s AND acc_no=%s"
            val = (self.user, self.beneficiary)
            mycursor.execute(query,val)
            output = mycursor.fetchall()
            if output:
                self.user = output[0][3]
                acc_no = output[0][9]
                lastname = output[0][1]
                othernames = output[0][2]
                
                print(Fore.YELLOW+"Loading..."+Style.RESET_ALL)
                time.sleep(2)
                print(f'''
                        {Fore.YELLOW}Account Number: {acc_no}
                        Beneficiary's Name: {lastname} {othernames}{Style.RESET_ALL}
                ''')
                self.status()
            else:
                print(Fore.RED+'Invalid Account Number'+Style.RESET_ALL)
                self.acc_name()    
    
    # Beneficiary Verification
    def status(self):
        try:
            if re.search(r'[a-zA-Z]', self.beneficiary):
                print(Fore.RED+'Invalid Acc No!'+Style.RESET_ALL)
                self.acc_name()
            else:
                print(f'Beneficiary\'s Acc No: {self.beneficiary}') 
                self.remark = 'Successful'
        except:
                ValueError(Fore.RED+' Values cant\'t be an alphabet '+Style.RESET_ALL)
                self.status()
                

    # Transfer   
    def transfer(self):
        try:
            self.amount = float(input('Amount: '))
            query = "SELECT * FROM details_table WHERE username=%s AND password=%s"
            val = (self.login, self.pwd)
            mycursor.execute(query,val)
            output = mycursor.fetchall()
            if output:
                acc_no = output[0][9]
                self.login = output[0][3]
                self.pin = output[0][12]
                balance = output[0][10]
                if self.amount >= 100.00:

                    if balance > self.amount:
                        self.balance = balance - self.amount
                        query = 'UPDATE details_table SET bal=%s WHERE username=%s'
                        val = (self.balance, self.login) 
                        mycursor.execute(query, val)
                        mycon.commit()
                        self.addd()

                    else:
                        print(Fore.RED+'Insufficient Balance!'+Style.RESET_ALL)
                        self.transfer()    
                else:
                    print(Fore.RED+'minimum of N100.00 is required!'+Style.RESET_ALL)
                    self.transfer()
        except NameError: 
            print(Fore.RED+' Check Your Input! '+Style.RESET_ALL)
            self.another()
        except ValueError:
            print(Fore.RED+' Check Your Input! '+Style.RESET_ALL)
            self.transfer()      
        finally:
            print(' ')  

    # Adding Account Balance
    def addd(self):
        query = "SELECT * FROM details_table WHERE username=%s AND acc_no=%s"
        val = (self.user, self.beneficiary)
        mycursor.execute(query,val)
        output = mycursor.fetchall()
        if output:
                acc_no = output[0][9]
                self.user = output[0][3]
                bal = output[0][10]   
                if self.balance >100.00:
                    self.tf = bal + self.amount 
                    query = 'UPDATE details_table SET bal=%s WHERE acc_no=%s'
                    val = (self.tf, self.beneficiary) 
                    mycursor.execute(query, val)
                    mycon.commit()

                    self.pin_confirmation()
                    print(Fore.GREEN+'Transaction successful'+Style.RESET_ALL)
                    time.sleep(2)
                    print(f'''
                            {Fore.YELLOW}N{self.amount}K has been debited from your account.
                            Your bal is N{self.balance}K{Style.RESET_ALL}
                    ''')
                    self.another()

                else:
                    print(Fore.RED+'minimum bal is N100.00!'+Style.RESET_ALL)
                    self.transfer()
    
    # Deposit
    def deposit(self):
        self.amount = float(input('Amount: '))
        query = "SELECT * FROM details_table WHERE username=%s AND password=%s"
        val = (self.login, self.pwd)
        mycursor.execute(query,val)
        output = mycursor.fetchall()
        if output:
            self.login = output[0][3]
            self.pin = output[0][12]
            balance = output[0][10]
            self.beneficiary = output[0][9]
            if self.amount >= 100.00:
                self.balance = balance + self.amount
                query = 'UPDATE details_table SET bal=%s WHERE username=%s'
                val = (self.balance, self.login) 
                mycursor.execute(query, val)
                mycon.commit()   
                self.remark = 'Successful'
                self.pin_confirmation()
                print('Transaction successful')
                self.another()
            else:
                print(Fore.RED+'minimum of N100.00 is required!'+Style.RESET_ALL)
            self.deposit()

    # Airtime(Others)           
    def airtime(self):
        self.beneficiary = input("Phone number: +234 ")
        if len(self.beneficiary) < 10:
            print('check the number!')
            self.airtime()
        elif len(self.beneficiary) == 10 or len(self.beneficiary) == 11:
            if self.beneficiary.startswith('705') or self.beneficiary.startswith('707') or self.beneficiary.startswith('807') or self.beneficiary.startswith('811') or self.beneficiary.startswith('815') or self.beneficiary.startswith('905'):
                net = 'glo'
                self.trans = (f'Airtime({net})')
                print(f'Network Provider: {net}')   
            elif self.beneficiary.startswith('701') or self.beneficiary.startswith('708') or self.beneficiary.startswith('802') or self.beneficiary.startswith('808') or self.beneficiary.startswith('812') or self.beneficiary.startswith('901') or self.beneficiary.startswith('902') or self.beneficiary.startswith('904') or self.beneficiary.startswith('907') or self.beneficiary.startswith('912') :
                net = 'Airtel'
                self.trans = (f'Airtime({net})')
                print(f'Network Provider: {net}')   
            elif self.beneficiary.startswith('7025') or self.beneficiary.startswith('7026') or self.beneficiary.startswith('703') or self.beneficiary.startswith('706') or self.beneficiary.startswith('803') or self.beneficiary.startswith('806') or self.beneficiary.startswith('810') or self.beneficiary.startswith('813') or self.beneficiary.startswith('814') or self.beneficiary.startswith('816') or self.beneficiary.startswith('903') or self.beneficiary.startswith('913') or self.beneficiary.startswith('916'):
                net = 'MTN'
                self.trans = (f'Airtime({net})')
                print(f'Network Provider: {net}')   
            else:
                self.trans = input('Network Provider: ')
        else:
            print('invalid!')

        self.amount = float(input('Amount: '))
    
        query = "SELECT * FROM details_table WHERE username=%s AND password=%s"
        val = (self.login, self.pwd)
        mycursor.execute(query,val)
        output = mycursor.fetchall()
        if output:
            self.login = output[0][3]
            self.pin = output[0][12]
            balance = output[0][10]
            if self.amount >= 100.00:
                if balance > self.amount:
                    self.balance = balance - self.amount
                    query = 'UPDATE details_table SET bal=%s WHERE username=%s'
                    val = (self.balance, self.login) 
                    mycursor.execute(query, val)
                    mycon.commit() 
                    self.remark = 'Succesful'  
                    self.pin_confirmation()
                    self.air_trans()
                    self.another()
                else:
                       self.remark = 'Pending'
                       print(Fore.RED+'Insufficient Fund!'+Style.RESET_ALL)
                       self.transfer()  
            else:
                print(Fore.RED+'minimum of N100.00 is required!'+Style.RESET_ALL)
                self.transfer()

    # Airtime(Self)            
    def airtime_self(self):
        query = "SELECT * FROM details_table WHERE username=%s AND password=%s"
        val = (self.login, self.pwd)
        mycursor.execute(query,val)
        output = mycursor.fetchall()
        if output:
            self.beneficiary = output[0][6]
            self.login = output[0][3]
            self.pin = output[0][12]
            balance = output[0][10]
            
            if self.beneficiary.startswith('705') or self.beneficiary.startswith('707') or self.beneficiary.startswith('807') or self.beneficiary.startswith('811') or self.beneficiary.startswith('815') or self.beneficiary.startswith('905'):
                    net = 'glo'
                    self.trans = (f'Airtime({net})')
                    print(f'Network Provider: {net}')
            elif self.beneficiary.startswith('701') or self.beneficiary.startswith('708') or self.beneficiary.startswith('802') or self.beneficiary.startswith('808') or self.beneficiary.startswith('812') or self.beneficiary.startswith('901') or self.beneficiary.startswith('902') or self.beneficiary.startswith('904') or self.beneficiary.startswith('907') or self.beneficiary.startswith('912') :
                net = 'Airtel'
                self.trans = (f'Airtime({net})')
                print(f'Network Provider: {net}')
            elif self.beneficiary.startswith('7025') or self.beneficiary.startswith('7026') or self.beneficiary.startswith('703') or self.beneficiary.startswith('706') or self.beneficiary.startswith('803') or self.beneficiary.startswith('806') or self.beneficiary.startswith('810') or self.beneficiary.startswith('813') or self.beneficiary.startswith('814') or self.beneficiary.startswith('816') or self.beneficiary.startswith('903') or self.beneficiary.startswith('913') or self.beneficiary.startswith('916'):
                net = 'MTN'
                self.trans = (f'Airtime({net})')
                print(f'Network Provider: {net}')
            else:
                self.trans = input('Network Provider: ')
            self.amount = float(input('Amount: '))
            if self.amount >= 100.00:
                if balance > self.amount:
                    self.balance = balance - self.amount
                    query = 'UPDATE details_table SET bal=%s WHERE username=%s'
                    val = (self.balance, self.login) 
                    mycursor.execute(query, val)
                    mycon.commit()   
                    self.remark = 'Successful'
                    self.pin_confirmation()
                    self.air_trans()
                    self.another()
                else:
                    print(Fore.RED+'Insufficient Fund!'+Style.RESET_ALL)
                    self.transfer()  
            else:
                print(Fore.RED+'minimum of N100.00 is required!'+Style.RESET_ALL)
                self.transfer()

     # Airtime Transaction           
    def air_trans(self):
        query = "INSERT INTO transaction_table(username,trans_type, beneficiary_no,amount, remark, date_time,pin) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        var = (self.login, self.trans, self.beneficiary, self.amount, self.remark, self.date,self.pin)
        mycursor.execute(query,var)
        self.dd()
        print(Fore.BLUE+'Recharged successful'+Style.RESET_ALL)
        time.sleep(2)
        print(f'''
                {Fore.YELLOW}N{self.amount}K has been debited from your account by {self.trans} network provider.
                Your bal is N{self.balance}K{Style.RESET_ALL}
        ''')
        self.another() 

    # Fetching Username And Password for Pin Confirmation
    def dd(self):
        self.pin =  self.pwd
        query = 'SELECT * FROM details_table WHERE username =%s AND password =%s'
        val = (self.login, self.pin)
        mycursor.execute(query, val)

        details = mycursor.fetchall()

        if details:
            self.login = details[0][3]
            self.pin = details[0][11]
        else:
            print(Fore.RED+'Incorrect Pin'+Style.RESET_ALL)
            self.pin_confirmation()

    # Transaction History     
    def trans_history(self):
        self.pwd = pw.pwinput('Pin: ')
        print(Fore.YELLOW+'Fetching...'+Style.RESET_ALL)
        time.sleep(3)
        # try:
        query = "SELECT * FROM transaction_table WHERE username=%s AND pin=%s"
        val = (self.login, self.pwd)
        mycursor.execute(query,val)
        output = mycursor.fetchall()
        if re.match(r"^\d+$", self.pwd):
            self.thv()
            if output:
                self.login = output[0][1]
                self.pwd = output[0][7]
                que = 'SELECT trans_id, trans_type, beneficiary_no, amount, remark, date_time  FROM transaction_table WHERE username=%s AND pin=%s'
                val = (self.login, self.pwd)
                mycursor.execute(que, val)
                rows = mycursor.fetchall()

                header = ["trans_id","trans_type", "beneficiary_no", "amount", "remark", "date_time" ]
                tt.print(rows,header)
                self.another()
            else:
                    print(Fore.YELLOW+'No Transaction Yet!'+Style.RESET_ALL)
                    self.another()
        else:
             print(Fore.RED+'Pin must be digits'+Style.RESET_ALL)
             self.trans_history()   

    # Transaction History's Pin Verification
    def thv(self):
        query = 'SELECT * FROM details_table WHERE username =%s AND pin=%s'
        val = (self.login, self.pwd)
        mycursor.execute(query, val)

        details = mycursor.fetchall()

        if details:
            self.login = details[0][3]
            self.pin = details[0][12]
        else:
            print(Fore.RED+'Incorrect Pin'+Style.RESET_ALL)
            self.trans_history()                 

    # Account Balance
    def acc_bal(self):
        pwd = pw.pwinput('Pin: ')
        print(Fore.YELLOW+'Checking...'+Style.RESET_ALL)
        time.sleep(2)
        query = "SELECT * FROM details_table WHERE username=%s AND pin=%s"
        val = (self.login, pwd)
        mycursor.execute(query,val)
        output = mycursor.fetchall()
        if output and re.match(r"^\d+$", pwd):
            self.lastname = output[0][1]
            self.othernames = output[0][2]
            self.login = output[0][3]
            self.pin = output[0][12]
            acc_no = output[0][9]
            balance = output[0][10]
            print(Fore.GREEN+'Fectching...'+Style.RESET_ALL)
            time.sleep(2)
            print(f'''
                        {Fore.YELLOW}Name: {self.lastname} {self.othernames}
                        Account Number: {acc_no}
                        Balance: N{balance}{Style.RESET_ALL}
            ''')
            self.another()
        else:
            print(Fore.RED+'Invalid Pin'+Style.RESET_ALL)
            self.acc_bal()

    # Inquiries
    def inq(self):
        print('''
                    Available services
                    1. Change pin
                    2. Change password
                    0. Back 
            ''') 
        user = input("Select: ")
        if user == '1':
           self.pin_change()
        elif user == '2':
            self.password_change()
        elif user == '0':
            self.transaction_type() 
        else:
            print(Fore.RED+'Invalid Input!'+Style.RESET_ALL)    
            self.inq() 

    # Changing of Password from Inquires         
    def password_change(self):
        password = pw.pwinput('Old Password: ')
        pwd1 = pw.pwinput('New Password: ')
        pwd = pw.pwinput('Confirm New Password: ')
        myquery = 'SELECT * FROM details_table WHERE password=%s AND username=%s'
        myval = (password, self.login)
        mycursor.execute(myquery, myval)
        details = mycursor.fetchall()
        if details:
            self.login = details[0][3]
            password = details[0][11]
            if pwd1 == pwd and len(pwd) == 6 and re.match(r"^[a-zA-Z]+$", pwd):
                print(Fore.YELLOW+'Updating...'+Style.RESET_ALL)
                query = "UPDATE details_table SET password=%s WHERE username=%s"
                val = (pwd, self.login)
                mycursor.execute(query, val)
                mycon.commit() 
                time.sleep(2)
                print(Fore.GREEN+'Updated!'+Style.RESET_ALL)
                self.transaction_type() 
            elif re.match(r"^[a-zA-Z0-9]+$", pwd):
                print(Fore.YELLOW+"Checking..."+Style.RESET_ALL) 
                time.sleep(2)
                print(Fore.RED+'Password must be letters'+Style.RESET_ALL)
                self.pattern()
            elif pwd1 != pwd:
                print(Fore.YELLOW+"Checking..."+Style.RESET_ALL)
                time.sleep(2)
                print(Fore.RED+'Password does not match'+Style.RESET_ALL)
                self.pattern()
            elif len(pwd) != 6:
                print(Fore.YELLOW+"Checking..."+Style.RESET_ALL)
                time.sleep(2)
                print(Fore.RED+'Password must be 6'+Style.RESET_ALL)
                self.pattern()
            else:
                print(Fore.RED+'Invalid!'+Style.RESET_ALL)
                self.password_change()    
        else:
                print(Fore.RED+'Invalid Input!'+Style.RESET_ALL)
                self.password_change() 

    # Password Pattern To Change Existing Password
    def pattern(self):
        print(f'''
                    {Fore.YELLOW}Press
                    1. Try Again 
                    0. Terminate
                    00. Menu{Style.RESET_ALL}
                    
                ''')  
        user = input('Select: ')
        if user == '0':
            print(Fore.RED+'Exit!'+Style.RESET_ALL)
            sys.exit()
        elif user == '1':
            self.password_change()  
                
        elif user == '00':
            self.transaction_type()                        

    # Changing of Pin from Inquires  
    def pin_change(self):
        self.pn = pw.pwinput('Old Pin: ')
        self.pwd1 = pw.pwinput('New Pin: ')
        self.new_pwd = pw.pwinput('Confirm New Pin: ')
        myquery = 'SELECT * FROM details_table WHERE pin=%s AND username=%s'
        myval = (self.pn, self.login)
        mycursor.execute(myquery, myval)
        details = mycursor.fetchall()
        if details:
            self.login = details[0][3]
            self.pwd = details[0][11]
            self.pn = details[0][12]
            if re.match(r"^\d+$", self.new_pwd):
                if self.pwd1 == self.new_pwd:
                    
                    if len(self.pwd1) == 4 and  len(self.new_pwd) == 4:
                        self.pnn()
                        query = "UPDATE details_table SET pin=%s WHERE username=%s"
                        val = (self.new_pwd, self.login)
                        mycursor.execute(query, val)
                        mycon.commit()
                        self.another()

                    elif self.pwd1 != self.new_pwd:
                        print(Fore.YELLOW+"Loading..."+Style.RESET_ALL) 
                        time.sleep(2)
                        print(Fore.RED+'pin does not match'+Style.RESET_ALL)
                        print('Press 0 to Terminate or 1 to continue')  
                        user = input('Select: ')
                        if user == '0':
                            sys.exit()
                        elif user == '1':
                            self.transaction_type()

                    else:
                            print('Loading...')
                            time.sleep(2)
                            print(Fore.RED+"pin should be 4 digits"+Style.RESET_ALL)

                else:
                    time.sleep(1)
                    print(Fore.RED+'Pin does not match'+Style.RESET_ALL) 
                    self.pin_change()       
            else:
                time.sleep(1)
                print(Fore.RED+'pin must be digit'+Style.RESET_ALL)
                self.pin_change()             
        else:
                print(Fore.YELLOW+"Loading..."+Style.RESET_ALL) 
                time.sleep(2)
                print(Fore.RED+"Invalid Pin"+Style.RESET_ALL)             
                self.pin_change() 

    # Updating of Pin into Transaction Table
    def pnn(self):
        myquery = 'SELECT * FROM transaction_table WHERE username=%s AND pin=%s'
        myval = (self.login, self.pn)
        mycursor.execute(myquery, myval)
        details = mycursor.fetchall()
        if details:
            self.login = details[0][1]
            self.pn = details[0][7]  
            que = 'UPDATE transaction_table SET pin=%s WHERE username=%s'
            var = (self.new_pwd, self.login)
            mycursor.execute(que,var)
            mycon.commit()
            print(Fore.YELLOW+'Updating...'+Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN+'Updated!'+Style.RESET_ALL)
        else:
            print(Fore.YELLOW+'Updating...'+Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN+'Updated!'+Style.RESET_ALL)
            time.sleep(1)
            print(f"""
                        {Fore.YELLOW}Dear {self.login.upper()}, no transaction has been made yet!
                        Try to deposit minimum of N100 for a start. Thank you{Style.RESET_ALL}
            """)   

    # Bills
    def bills(self):
       time.sleep(1)
       print(f'''
                1. Electricity
                2. Water
                3. Internet
                4. TV
        ''')
       user = input('Select: ')
       if user == '1':
           net = 'Bills'
           self.trans = (f'{net}(Electricity)')
           self.bill_inp()
           print('Wait')
       elif user == '2':
           net = 'Bills'
           self.trans = (f'{net}(Water)')
           self.bill_inp()
           print('Hold')
       elif user == '3':
           net = 'Bills'
           self.trans = (f'{net}(Internet)')
           self.bill_inp()
           print('Duro')
       elif user == '4':
           net = 'Bills'
           self.trans = (f'{net}(TV)')
           self.bill_inp()
           print('Awe')
       else:
           print(Fore.RED+'Invalid'+Style.RESET_ALL)                
           self.bills()   
    
    # Biils Transaction
    def bill_inp(self):
        self.amount = float(input('Amount: '))
        self.beneficiary = random.randint(1000000000, 1999999999)
        self.remark = 'Successful'
        self.pin_confirmation()
        self.another()
    
    # Another Transaction
    def another(self):
        time.sleep(1)
        print('Enter for Another Transaction or 0 to exit')
        user = input('Select: ')
        if user == "0":
            print(Fore.RED+'Exit!'+Style.RESET_ALL)
            sys.exit()
        else:
            self.transaction_type()  

    # Pin Confirmation         
    def pin_confirmation(self) : 
        self.pin =  pw.pwinput('Pin: ')
        print(Fore.YELLOW+'Loading...'+Style.RESET_ALL)
        time.sleep(1)
        query = 'SELECT * FROM details_table WHERE username =%s AND pin =%s'
        val = (self.login, self.pin)
        mycursor.execute(query, val)

        details = mycursor.fetchall()

        if details:
            self.login = details[0][3]
            self.pin = details[0][12]
            # user = input('Number: +234 ')
            if re.match(r"^\d+$", self.pin):
                if len(self.pin) == 4:
                    pass
                else:
                    print('Length must 4')    
            else:
                print('Pin must be digit')  
        else:
            print(Fore.RED+'Incorrect Pin'+Style.RESET_ALL)
            self.pin_confirmation()

        t = datetime.now()
        self.date = t.strftime("%d/%m/%Y %H:%M:%S")    
        self.tt()

    # Trasaction Table Query    
    def tt(self):
        mytran = "INSERT INTO transaction_table(username,trans_type, beneficiary_no,amount, remark, date_time,pin) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        var = (self.login, self.trans, self.beneficiary, self.amount, self.remark, self.date,self.pin)
        mycursor.execute(mytran, var)
        mycon.commit()    
        
bank = Bank()
