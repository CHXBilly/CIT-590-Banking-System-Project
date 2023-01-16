'''
This Python assignment will involve implementing a bank program that manages bank accounts and allows
for deposits, withdrawals, and purchases.

The program will initially load a list of accounts from a .txt file, and deposits and withdrawals from
additional .csv files. Then it will parse and combine all of the data and store it in a dictionary.

'''

# TODO insert your code
import math
import operator

def init_bank_accounts(accounts, deposits, withdrawals):
    bank_accounts = {}
    #open the file accounts, import the account number, first name and last name in a dictionary
    with open(accounts) as f:
        for line in f:
           (account_number, firstname, lastname) = line.split('|')
           bank_accounts[account_number.strip()] = {'first_name':firstname.strip(),'last_name':lastname.strip()}

    #open the file accounts, import the account number, and deposit amount in a dictionary
    with open(deposits) as f:
        for line in f:
            lst = line.strip().split(",")
            #get account_number and deposit amount from list
            account_number = lst[0].strip()
            value=0
            #make sure it go through all value in the list, if there is no value in the deposit it will just add 0
            for i in range(len(lst[1:])+1):
                value=value+float(lst[i])
                value=round(value,2)
            bank_accounts[account_number].update({'balance':value})

    with open(withdrawals) as f:
        for line in f:
            lst = line.strip().split(",")
            #get account_number and deposit amount from list
            account_number = lst[0].strip()
            value=0
            #make sure it go through all value in the list, if there is no value in the deposit it will just add 0
            for i in range(len(lst[1:])+1):
                value=value+float(lst[i])
                value=round(value,2)
            bank_accounts[account_number]['balance']-=value

    return bank_accounts

#get the info with the respect account_number
def get_account_info(bank_accounts, account_number):
    if account_number.isdigit():
        if int(account_number)>0 and int(account_number)<11:
            return bank_accounts[account_number]
        else:
            print('The account doesnt exist')
    else:
        return None

# Withdraws the given amount from the account with the given account_number
def withdraw(bank_accounts, account_number, amount):
    #make sure the account number exist
    if int(account_number)>0 and int(account_number)<11:
        if bank_accounts[account_number]['balance']<float(amount):
            raise RuntimeError('Amount greater than available balance')
        else:
            bank_accounts[account_number]['balance']-=float(amount)
            round_balance(bank_accounts,account_number)
            print('new balance',bank_accounts[account_number]['balance'])
    #the account doesnt exist print a friendly message
    else:
        print("Sorry, that account doesn't exist.")

# Deposits the given amount into the account with the given account_number
def deposit(bank_accounts, account_number, amount):
    #make sure the account number exist
    if int(account_number)>0 and int(account_number)<11:
        bank_accounts[account_number]['balance']+=float(amount)
        round_balance(bank_accounts,account_number)
        print('new balance',bank_accounts[account_number]['balance'])
    #the account doesnt exist print a friendly message
    else:
        print("Sorry, that account doesn't exist.")

def purchase(bank_accounts, account_number, amounts):
    total_purchase=math.fsum(amounts)+calculate_sales_tax(math.fsum(amounts))

    if int(account_number)>0 and int(account_number)<11:
        if bank_accounts[account_number]['balance']<float(total_purchase):
            raise RuntimeError('Amounts greater than available balance')
        else:
            #deduct the purchase amount from the balance if user has enough money and correct account number
            bank_accounts[account_number]['balance']-=float(total_purchase)
            round_balance(bank_accounts,account_number)
            print('new balance',bank_accounts[account_number]['balance'])
    #the account doesnt exist print a friendly message
    else:
        print("Sorry, that account doesn't exist.")

def sort_accounts(bank_accounts, sort_type, sort_direction):
    if sort_type=='account_number':
        #sort account number in ascending order
        if sort_direction=='asc':
            sort_orders = sorted(bank_accounts.items(), key=lambda x: int(x[0]))
            print(sort_orders)
            return sort_orders
        #else is in descending order
        else:
            sort_orders = sorted(bank_accounts.items(), key=lambda x: int(x[0]), reverse=True)
            print(sort_orders)
            return sort_orders
    elif sort_type=='first_name':
         #sort first name in ascending order
        if sort_direction=='asc':
            sort_orders = sorted(bank_accounts.items(), key=lambda x: x[1]['first_name'])
            print(sort_orders)
            return sort_orders
        #else is in descending order
        else:
            sort_orders = sorted(bank_accounts.items(), key=lambda x: x[1]['first_name'], reverse=True)
            print(sort_orders)
            return sort_orders
    elif sort_type=='last_name':
         #sort last name in ascending order
        if sort_direction=='asc':
            sort_orders = sorted(bank_accounts.items(), key=lambda x: x[1]['last_name'])
            print(sort_orders)
            return sort_orders
        #else is in descending order
        else:
            sort_orders = sorted(bank_accounts.items(), key=lambda x: x[1]['last_name'], reverse=True)
            print(sort_orders)
            return sort_orders
    elif sort_type=='balance':
         #sort balance in ascending order
        if sort_direction=='asc':
            sort_orders = sorted(bank_accounts.items(), key=lambda x: x[1]['balance'])
            print(sort_orders)
            return sort_orders
        #else is in descending order
        else:
            sort_orders = sorted(bank_accounts.items(), key=lambda x: x[1]['balance'], reverse=True)
            print(sort_orders)
            return sort_orders
    else:
        print("Unexpected inputs, please input 'account_number', 'first_name', 'last_name', or 'balance'")
        return None

def export_statement(bank_accounts, account_number, output_file):
    #create a new output file
    if int(account_number)>0 and int(account_number)<7:
        with open(output_file, 'w') as f:
            #read every key and value in the according bank account
            for key, value in bank_accounts[account_number].items():
                #make sure it writes in a new line every time
                f.write('%s:%s\n' % (key, value))
    else:
        print('The account doesnt exist')


def round_balance(bank_accounts, account_number):
    #round the balance to 2 digit
    bank_accounts[account_number]['balance']=round(bank_accounts[account_number]['balance'],2)

def calculate_sales_tax(amount):
    return 0.06*amount


def main():
    bank_accounts = init_bank_accounts('accounts.txt', 'deposits.csv', 'withdrawals.csv')
    while True:
        try:
            print("Welcome to the bank!  What would you like to do?\n1: Get account info\n2: Make a deposit\n3: Make a withdrawal\n4: Make a purchase\n5: Sort accounts\n6: Export a statement\n0: Leave the bank")
            #ask customer what choice
            customer_choice = int(input())
        except ValueError:
            print('Please enter a valid number')
            continue
        else:
            if customer_choice ==1:
                account_number = input('Account number? ')
                print(get_account_info(bank_accounts, account_number))

            elif customer_choice ==2:
                account_number = input('Account number? ')
                amount = input('Amount? ')
                deposit(bank_accounts, account_number, amount)
            elif customer_choice ==3:
                account_number = input('Account number? ')
                amount = input('Amount? ')
                withdraw(bank_accounts, account_number, amount)
            elif customer_choice ==4:
                account_number = input('Account number? ')
                amounts = input('Amount?(as comma separated list) ')
                amounts=amounts.split(',')
                amounts_list=[None]*len(amounts)

                for i in range(len(amounts)):
                    amounts_list[i]=float(amounts[i])
                purchase(bank_accounts, account_number, amounts_list)
            elif customer_choice ==5:
                sort_type = input("Sort type ('account_number', 'first_name', 'last_name', or 'balance')? ")
                sort_direction = input("Sort type ('asc' or 'desc')? ")
                sort_accounts(bank_accounts, sort_type, sort_direction)
            elif customer_choice ==6:
                account_number = input('Account number? ')
                output_file=account_number+'.txt'
                export_statement(bank_accounts, account_number, output_file)
            elif customer_choice ==0:
                print('Good bye')
                break
            else:
                print('Please put in a correct number')



if __name__ == "__main__":
    main()
