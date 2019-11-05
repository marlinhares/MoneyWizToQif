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
STRTHOUSANDSEP = '.'
STRDECIMALPOINT = ','

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
                    if(c):
                        c = c.replace(' > ', ':')
                        row[6].append(c)

                lstRows.append(row)                

                # normalize payee as description in case payee is not set
                row[5] = row[5] or row[4]

                # normalize memo
                row[9] = row[9].replace('\n', ' ').replace('\r', '')

                # normalize value
                v = row[10]
                v = row[10].replace(STRTHOUSANDSEP, '')                
                row[10] = v


        
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
    
    for a in lstMyaccs:

        s= ''
        for t in lstMytrans:
            
            if(t[2] != a): continue
            
            strNumcheck = ''

            s2 = ''
            cat = t[6]
            if(len(cat)==0):
                s2 = templates.strTempl_trans_in_cat.format(strCategory='[(null)]')
                
            elif(len(cat)==1):
                s2 = templates.strTempl_trans_in_cat.format(strCategory=cat[0])

            else:
                # divide split value because moneywiz does not send it individualy
                v = t[10].replace(STRTHOUSANDSEP, '')
                v = v.replace(STRDECIMALPOINT, '.')
                v = vTotal = float (v)
                v = v / len(cat)
                v = float(format(v, '.2f'))
                j=0
                for c in cat:
                    j=j+1
                    if(j==len(cat)):
                        v = vTotal - v*(len(cat))
                    strValue = str(v)
                    strValue = strValue.replace('.', STRDECIMALPOINT)

                    s2 += templates.strTempl_trans_in_spl.format(strCategory_spl=c,strMemo_spl='',strValue_spl=strValue)

            # if transfer use this
            if(t[3]):
                s2 = templates.strTempl_trans_in_cat.format(strCategory='[' + t[3] + ']')
                strNumcheck = 'TXFR'


            s += templates.strTempl_trans_in.format(strDate=t[7], strPayee=t[5], strMemo=t[9], strNumCheck=strNumcheck, strValor=t[10], strCategorySplit=s2)

        if(s):
            s = templates.strTempl_trans.format(strAccount=a, strTransactions=s)
            print s