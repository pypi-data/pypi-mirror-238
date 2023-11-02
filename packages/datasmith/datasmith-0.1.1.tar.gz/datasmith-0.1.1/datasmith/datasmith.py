import random
import csv
import pandas as pd
first_names = ('John','Andy','Joe','Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Sophia', 'Isabella', 'Mia', 'Jackson', 'Lucas',
    'Harper', 'Ethan', 'Aiden', 'Alexander', 'Sebastian', 'Charlotte', 'Grace', 'Scarlett', 'Lily', 'Amelia',
    'Madison', 'Evelyn', 'Chloe', 'Abigail', 'Ella', 'Benjamin', 'Carter', 'Henry', 'Samuel', 'Michael',
    'Eleanor', 'Luna', 'James', 'David', 'Matthew', 'William', 'Sofia', 'Emily', 'Jack', 'Sophie',
    'Logan', 'Daniel', 'Daniel', 'Grace', 'Nora', 'Ella', 'Emma', 'Oliver', 'Lucas', 'Liam',
    'William', 'Mia', 'Olivia', 'Aiden', 'Ethan', 'Sophia', 'Isabella', 'Mason', 'Harper', 'Ava',
    'Emily', 'Benjamin', 'Amelia', 'Elizabeth', 'David', 'Charlotte', 'Evelyn', 'Madison', 'Samuel', 'James',
    'Oliver', 'Ella', 'Lily', 'Scarlett', 'Henry', 'Daniel', 'Michael', 'Matthew', 'Grace', 'Nora',
    'Lucas', 'Logan', 'Sophie', 'Sofia', 'Aiden', 'Grace', 'William', 'Emily', 'Ava', 'Mia',
    'Ella', 'Nora', 'Sophia', 'Isabella', 'Olivia', 'Liam', 'Noah', 'Ethan', 'Benjamin', 'Mason',
    'Alexander', 'Evelyn', 'Amelia', 'Luna', 'David', 'Jackson', 'Jack', 'Sebastian', 'Harper', 'Daniel',
    'Lily', 'Madison', 'Abigail', 'Ella', 'Nora', 'Grace', 'Logan', 'Sofia', 'Ethan', 'Sophie',
    'Emma', 'William', 'Oliver', 'Chloe', 'Charlotte', 'Lucas', 'Aiden', 'Michael', 'Matthew', 'James')

last_names = ('Johnson','Smith','Williams','Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Wilson', 'Martin', 'Thompson', 'White', 'Harris',
    'Clark', 'Thomas', 'Young', 'Walker', 'King', 'Wright', 'Scott', 'Allen', 'Adams', 'Mitchell',
    'Hall', 'Green', 'Evans', 'Turner', 'Carter', 'Morris', 'Hill', 'Lewis', 'Roberts', 'Reed',
    'Cook', 'Bell', 'Bailey', 'Cooper', 'Rivera', 'Perez', 'Torres', 'Gray', 'Kelly', 'Bennett',
    'Baker', 'Mitchell', 'Ramirez', 'James', 'Phillips', 'Sanchez', 'Morales', 'Rodriguez', 'Jackson', 'Foster',
    'Diaz', 'Hayes', 'Myers', 'Ford', 'Owens', 'Garcia', 'Gonzalez', 'Washington', 'Butler', 'Simmons',
    'Fleming', 'Stone', 'Gardner', 'Lopez', 'Robinson', 'Ward', 'Cruz', 'Perry', 'Long', 'Howard',
    'Patterson', 'Reyes', 'Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Wilson', 'Martin', 'Thompson',
    'White', 'Harris', 'Clark', 'Thomas', 'Young', 'Walker', 'King', 'Wright', 'Scott', 'Allen', 'Adams',
    'Mitchell', 'Hall', 'Green', 'Evans', 'Turner', 'Carter', 'Morris', 'Hill', 'Lewis', 'Roberts', 'Reed')

def create_names(rows):
    name_group=[]
    first_name_group = []
    last_name_group=[]
    #random.seed(10)
    while(len(set(name_group))!=rows):
        first_name=random.choice(first_names)
        last_name=random.choice(last_names)
        full_name=first_name+" "+last_name
        if(full_name not in set(name_group)):
            first_name_group.append(first_name)
            last_name_group.append(last_name)
            name_group.append(full_name)
    return first_name_group,last_name_group,name_group
    # print(name_group)
    # print(first_name_group)
    # print(last_name_group)

def create_email(first_name_group,last_name_group):
    email_group=[]
    X=['gmail.com','yahoo.com','hotmail.com']
    for i,j in zip(first_name_group,last_name_group):
        email=i.lower()+j.lower()+"@"+random.choice(X)
        email_group.append(email)
    return email_group
    #print(email_group)

#number=''.join(random.choice(X)+[str(random.randint(0,9) for _ in range(9))])
def craete_number(rows):
    X = ['6', '7', '8', '9']
    number_group=[]
    while(len(set(number_group))!=rows):
        number = ''.join([random.choice(X)] + [str(random.randint(0, 9)) for _ in range(9)])
        if(number not in set(number_group)):
            number_group.append(number)
    return number_group
    #print(number_group)

def create_dataset(rows,*args):

    final_list=[]
    if 'name' in args:
        first_name_group,last_name_group,name_group=create_names(rows)
        name_group.insert(0,'name')
        final_list.append(name_group)
    if 'email' in args:
        email_group=create_email(first_name_group,last_name_group)
        email_group.insert(0,'email')
        final_list.append(email_group)
    else:
        email_group=[]
    if 'number' in args:
        number_group=craete_number(rows) 
        number_group.insert(0,'number')
        final_list.append(number_group) 
    else:
        number_group=[]  


    with open('trailV1.csv', mode='w', newline='') as file:
      writer = csv.writer(file)
      writer.writerows(final_list)



n=int(input("Enter number of rows: "))
create_dataset(n,'name','email','number')

with open('trailV1.csv', mode='r') as infile:
    reader = csv.reader(infile)
    data = list(reader)
# print(data)
# Transpose the data
transposed_data = list(map(list, zip(*data)))

# Write the transposed data to a new CSV file
with open('x.csv', mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(transposed_data)

df=pd.read_csv('x.csv')
print(df.to_string())