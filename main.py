from html.parser import HTMLParser
import requests
import random

def checkAdr(adr, privateKey):
    #  print(adr, privateKey)

    r = requests.get('https://blockchain.info/address/' + adr + '?format=json&offset=0')
    if r.status_code == 200:
        j = r.json()
        balance = j['final_balance']
        balanceRe = j['total_received']
        if balance > 0:
            print(balance, 'adr:', adr, 'privateKey:', privateKey)
        if balanceRe > 0:
            print('re:', balanceRe, 'adr:', adr, 'privateKey:', privateKey)
    else:
        print('status code is not 200')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.counter = 0
        self.getA = 0
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            self.counter += 1
            if self.counter == 1:
                #  print('attrs:', attrs)#private Key
                self.curPrivateKey = attrs[0][1]
            if self.counter == 2:
                self.getA = 1

    def handle_endtag(self, tag):
        if tag == 'span':
            self.counter -= 1

    def handle_data(self, data):
        if self.getA != 0 and self.getA != 3:
            self.getA += 1
        elif self.getA == 3:
            #  print('data:', data)#public key
            checkAdr(data, self.curPrivateKey)
            self.getA = 0

parser = MyHTMLParser()

def doPage(p):
    page = requests.get('http://directory.io/' + str(p))
    parser.feed(page.text)
    print('page', p, 'done')

#  done:
#  1        299
#  1000     1010
#  1111
#  1111111111
#  123456789042
#  100000000000000000000
#  10000000000000000000000000000000 10000000000000000000000000000010

def doRange(f, t):
    for x in range(f, t):
        doPage(x)


#for x in range(1, 11):
#    x_ = 10**x
#    doRange(x_, x_ + 11)

for x in range(10):
    doPage(random.randint(1, 904625697166532776746648320380374280100293470930272690489102837043110636675))
