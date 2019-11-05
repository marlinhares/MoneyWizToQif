from datetime import datetime
from time import sleep
import csv

############################################
# PARAMETERS
############################################
STRFILENAME = 'moneywiz.csv'
STRDELIMITER = '|'

############################################
# GLOBALS
############################################
setMyaccs = set()
setMytags = set()
setMycats = set()
setMytrans = []
lstRows=[]


with open(STRFILENAME) as infile:
    
    csv_reader = csv.reader(infile, delimiter=STRDELIMITER)
    
    for row in csv_reader:        
        lstRows.append(row)
        


for row in lstRows:
    
    


    # vamos popular os accounts
    for row in csv_reader:
        
        alltrans.append(row)
        
    	if row[0]: myacc.add(row[0])
        
        if len(row)>12 and row[13]: mytags.add(row[13])
        
        if len(row)>6: 
            s = row[6]
            s = s.split(', ')
            
            for e in s:
                mycat.add(e)
            
    
mycat = sorted(mycat) 
myacc = sorted(myacc)
    
    
print(myacc)
print('=================')
print(mytags)
print('=================')
print(mycat)



for a in myacc:
    
    with open('processar/' + a + '.qfx', 'w+') as outfile:
    
        print(a)
        print('===================================')
        
        s = """OFXHEADER:100
        DATA:OFXSGML
        VERSION:102
        SECURITY:NONE
        ENCODING:USASCII
        CHARSET:1252
        COMPRESSION:NONE
        OLDFILEUID:NONE
        NEWFILEUID:NONE

        <OFX>
        <SIGNONMSGSRSV1>
        <SONRS>
        <STATUS>
        <CODE>0
        <SEVERITY>INFO
        <MESSAGE>OK
        </STATUS>
        <DTSERVER>20191026104908.000[-3]
        <LANGUAGE>ENG
        <INTU.BID>03000
        </SONRS>
        </SIGNONMSGSRSV1>
        <BANKMSGSRSV1>
        <STMTTRNRS>
        <TRNUID>0
        <STATUS>
        <CODE>0
        <SEVERITY>INFO
        <MESSAGE>OK
        </STATUS>
        <STMTRS>
        <CURDEF>USD
        <BANKACCTFROM>
        <BANKID>122000661
        <ACCTID>""" + a + """
        <ACCTTYPE>CHECKING
        </BANKACCTFROM>
        <BANKTRANLIST>
        <DTSTART>20160401130000.000[-3]
        <DTEND>20191031130000.000[-3]
        """ 
        s = s.replace('    ', '')
        outfile.write(s);
        
        for t in alltrans:
            if len(t)>2 and t[2] == a:
                #buscar valores
                sleep(0.001)
                id = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                id = id.replace('-', '').replace(' ', '').replace(':', '').replace('.','')
                id = 'R' + id
            
                payee = t[5]
                amount = t[10]
                amount = amount.replace('.', '')
                amount = amount.replace(',', '.')
                #amount = amount.replace('p', ',')
                #amount = amount.replace('v', '.')
                memo = t[9]
                data = t[7]
                data = datetime.strptime(data, '%m/%d/%Y')
                data = data.strftime("%Y%m%d")
                data = data + '130000.000[-3]'
                trans_type = 'DEBIT' if amount[0] == '-' else 'CREDIT'
            
                if(t[3]):
                    payee = payee + 'trx to ' + t[3]
                    memo = memo + 'trx to ' + t[3]
                
                print a
                print trans_type
                print id
                print payee
                print amount
                print memo
                print data
            
                s = """<STMTTRN>
                <TRNTYPE>""" + trans_type + """
                <DTPOSTED>""" + data + """
                <TRNAMT>""" + amount + """
                <FITID>""" + id + """
                <NAME>""" + payee + """
                </STMTTRN>
                """
                s = s.replace('    ', '')
                outfile.write(s)
                        
        s = """</BANKTRANLIST>
        <LEDGERBAL>
        <BALAMT>0.00
        <DTASOF>20191017130000.000[-3]
        </LEDGERBAL>
        </STMTRS>
        </STMTTRNRS>
        </BANKMSGSRSV1>
        </OFX>"""
        s = s.replace('    ', '')
        outfile.write(s)
    
