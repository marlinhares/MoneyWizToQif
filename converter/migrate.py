from datetime import datetime
from time import sleep
import csv
import templates

############################################
# PARAMETERS
############################################
STRFILENAME = 'moneywiz.csv'
STRDELIMITER = '|'
STRFILENAME_OUT = 'toprocess.qif'

############################################
# GLOBALS
############################################
setTmp = set()
lstMyaccs = []
lstMytags = set()
lstMycats = set()
lstMytrans = []
lstRows=[]


with open(STRFILENAME) as infile:
    
    csv_reader = csv.reader(infile, delimiter=STRDELIMITER)
    
    for row in csv_reader:           
        if len(row)>2: 
            if row[0]=='':
                # normalize categories in a list
                cats = row[6].split(', ')
                row[6] = []
                for c in cats:
                    c = c.replace(' > ', ':')
                    row[6].append(c)                
                lstRows.append(row)
                print row
        
# lets get the accounts
for row in lstRows:
    if row[2]: setTmp.add(row[2])
    if row[3]: setTmp.add(row[3])

lstMyaccs = sorted(setTmp)

# lets get the categories
setTmp = set()
for row in lstRows:
    if row[6]:
        cats = row[6]
        for c in cats:            
            setTmp.add(c)

lstMycats = sorted(setTmp)

# lets get the transactions
for row in lstRows:
    # discard if transaction is transfer and positive value (it already has a correspondent negative)
    if not (row[2] and row[3] and row[10][0]!='-'):        
        lstMytrans.append(row)

for a in lstMytrans:
    print a
    
print lstMyaccs

print lstMycats


#with open(STRFILENAME_OUT, 'w+') as outfile:
if 1:
    
    s= ''
    for a in lstMyaccs:
        s += templates.strTempl_Acc_in.format(strAccountName=a)
        
    s = templates.strTempl_Acc.format(strAccounts=s)
    print s
    
    s= ''
    for c in lstMycats:
        i = 0
        for t in lstMytrans:
            for c2 in t[6]:
                if(c2 == c):
                    i = i + 1 if (t[10][0]!='-') else i -1
        
        strType = 'I' if i > 0 else 'E'
        
            
        s += templates.strTempl_Cat_in.format(strCategoryName=c, strCategoryType=strType)
        
    s = templates.strTempl_Cat.format(strCategories=s)
    print s
    
    