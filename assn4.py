#!/user/bin/python

import sys

def sum_amount(cashier):
    return cashier[0] + cashier[1]*5 + cashier[2]*10 + cashier[3]*20


# Delete the last zeros
def modify_for_display(array):
    i = len(array)-1
    while array[i] == 0:
        i-=1
    array = array[0:i+1]
    for idx in range(0, len(array)):
        array[idx] = str(array[idx])
    output = " ".join(array) 
    return output


# Convert list of numbers to string
def convert_to_string(array):
    for i in range(0, len(array)):
        array[i] = str(array[i])
    output = " ".join(array)
    return output+"\n"


# Convert string to list of numbers
def convert_to_list(s):
    out = s.split(" ")
    for i in range(0, len(out)):
        out[i] = int(out[i])
    return out


# Create/Write to register file
def write_data (filename, data1, data2):
    try:
        register = open(filename, "w")
        register.write(convert_to_string(data1))
        register.write(str(data2))
        register.close()
    except IOError:
        print ("Error 4: Unable to read/write data file")
        exit(4)


if len(sys.argv) <= 1:
    print ("Usage: %s number of arguments." %sys.argv[0])
    exit(1)
#init
if sys.argv[1] == "init":
    cashier = [0, 0, 0, 0]
    total_sales = 0
    amount = 0
    if len(sys.argv) > 2 and len(sys.argv) < 9:
        if len(sys.argv) <= 4:
            print ("Error 1: Bad arguments %s." %sys.argv[0])
            exit (1)
        amount = int(sys.argv[2])
        if len(sys.argv)>4:
            cashier[0] = int(sys.argv[4])
        if len(sys.argv)>5:
            cashier[1] = int(sys.argv[5])
        if len(sys.argv)>6:
            cashier[2] = int(sys.argv[6])
        if len(sys.argv)>7:
            cashier[3] = int(sys.argv[7])
    if len(sys.argv) >= 9:
        print ("Error 1: Bad arguments %s." %sys.argv[0])
        exit (1)
    #Saving output
    if sum_amount(cashier) == amount:
        write_data("./register_dln45", cashier, total_sales)
        exit(0)
    else:
        #keep previous state - Dont write to register file
        cashier = [0, 0 ,0, 0]
        print ("Error 2: Amount don't jibe %s." %sys.argv[0])
        exit (2)

#report
if sys.argv[1] == "report":
    if len(sys.argv) > 2:
        print ("Error 1: Bad arguments %s." %sys.argv[0])
        exit (1)
    else:
        try:
            register = open("./register_dln45", "r")
            cashier = convert_to_list(register.readline())
            total_sales = int(register.readline())
            register.close()
            print ("%d : %d = %d %d %d %d" %(total_sales, sum_amount(cashier), cashier[0], cashier[1], cashier[2], cashier[3]))
            exit(0)
        except IOError:
            print ("Error 4: Unable to read/write data file")
            exit(4)

#top level read data for purchase/change operation
try:
    register = open("./register_dln45", "r")
    cashier = convert_to_list(register.readline())
    total_sales = int(register.readline())
    register.close()
except IOError:
    print ("Error 4: Unable to read/write data file")
    exit(4)

#purchase
if sys.argv[1] == "purchase":
    if len(sys.argv) < 5:
        print ("Error 1: Bad arguments %s." %sys.argv[0])
        exit (1)
    else:
        amount = int(sys.argv[2])
        input_cashier = [0, 0, 0, 0]
        if len(sys.argv)>4:
            input_cashier[0] = int(sys.argv[4])
        if len(sys.argv)>5:
            input_cashier[1] = int(sys.argv[5])
        if len(sys.argv)>6:
            input_cashier[2] = int(sys.argv[6])
        if len(sys.argv)>7:
            input_cashier[3] = int(sys.argv[7]) 
        if sum_amount(input_cashier) < amount:
            #keep previous state - Dont write to register file
            cashier = [0, 0 ,0, 0]
            print ("Error 2: Amount don't jibe %s." %sys.argv[0])
            exit (2)
        else:
            #Update cashier/ sales
            total_sales += amount
            cashier[0] = cashier[0] + input_cashier[0]
            cashier[1] = cashier[1] + input_cashier[1]
            cashier[2] = cashier[2] + input_cashier[2]
            cashier[3] = cashier[3] + input_cashier[3]
            #Handle change
            input_amount =  sum_amount (input_cashier)
            change_amount = input_amount - amount
            change_output = [0, 0, 0, 0]
            if change_amount > (cashier[3]*20):
                change_output[3] = cashier[3]
                cashier[3] = 0
                change_amount -= change_output[3]*20 
            else:
                change_output[3] = change_amount/20
                cashier[3] -= change_amount/20
                change_amount -= change_output[3]*20
            if change_amount > (cashier[2]*10):
                change_output[2] = cashier[2]
                cashier[2] = 0
                change_amount -= change_output[2]*10
            else:
                change_output[2] = change_amount/10
                cashier[2] -= change_amount/10
                change_amount -= change_output[2]*10
            if change_amount > (cashier[1]*5):
                change_output[1] = cashier[1]
                cashier[1] = 0
                change_amount -= change_output[1]*5
            else:
                change_output[1] = change_amount/5
                cashier[1] -= change_amount/5
                change_amount -= change_output[1]*5
            if (change_amount > cashier[0]):
                change_output[0] = cashier[0]
                cashier[0] = 0
                change_amount -= change_output[0]
                #reverse back to previous state - Fix here
                print ("Error 3: Drawer has insufficient money for change")
                exit(3)
            else:
                change_output[0] = change_amount
                cashier[0] -= change_amount
                change_amount -= change_output[0]
            #Print output
            output = modify_for_display(change_output)
            print ("%s" %output)
            write_data("./register_dln45", cashier, total_sales)
            exit(0)
            
#change
if sys.argv[1] == "change":
    if len(sys.argv) < 5:
        print ("Error 1: Bad arguments %s." %sys.argv[0])
        exit (1)
    #reading input
    tendered = [0, 0, 0, 0]
    requested = [0, 0, 0, 0]
    i = 2
    while i>1 and sys.argv[i] != "=":
        tendered[i-2] = int(sys.argv[i])
        i+=1
    for k in range(0,len(sys.argv)-i-1):
        requested[k] = int(sys.argv[k+i+1])
        k+=1
    if sum_amount(tendered) != sum_amount(requested):
        #keep previous state - Dont write to register file
        cashier = [0, 0 ,0, 0]
        print ("Error 2: Amount don't jibe %s." %sys.argv[0])
        exit (2)
    else:
        #update cashier
        for n in range(0, len(cashier)):
            cashier[n] += tendered[n]
        #handle change
        change_output = [0, 0, 0, 0]
        # 20 = 5*2^2, 10 = 5*2^1, 5 = 5*2^0
        for n in range(0, 2):
            if requested[3-n] < cashier[3-n]: 
                change_output[3-n] = requested [3-n]
                cashier[3-n] -= requested [3-n]
            else:
                change_output[3-n] = cashier[3-n]
                cashier[3-n] = 0
                requested[3-n] -= change_output [3-n]
                requested[2-n] += requested[3-n]*5*(2**(2-n))/5*(2**(1-n))
        
        if requested[1] < cashier[1]:
            change_output[1] = requested [1]
            cashier[1] -= requested[1]
        else:
            change_output[1] = cashier[1]
            cashier[1] = 0
            requested[1] -= change_output[1]
            requested[0] += requested[1]*5
        
        if requested[0] < cashier [0]:
            change_output[0] = requested[0]
            cashier[0] -= requested[0]
        else:
            change_output[0] = cashier[0]
            cashier[0] = 0
            requested[0] -= change_output[0]
            if (requested[0] > 0): #Unresolved requested bill
                #reverse back to previous state - Fix here
                print ("Error 3: Drawer has insufficient money for change")
                exit(3)
        #Print output
        output = modify_for_display(change_output)
        print (output)
        write_data("./register_dln45", cashier, total_sales)
        exit(0)
