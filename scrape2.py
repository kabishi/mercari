#Mercari Scraper, Only Find Sold Items
#URL Encode &status_trading_sold_out=1 Designates Sold items
import requests, re, time, fileinput,sys,csv
from lxml import html
import mercDB,os

requests.packages.urllib3.disable_warnings()
'''
SELECT title, sum(qty) AS Qty FROM `titlesQty` 
WHERE 1
group by title, Qty
order by 2 desc
'''

#&status_trading_sold_out=1  Boolean sold out status.
#&price_min=1000&price_max=2000 Price, $10 - $20
#&keyword=  Specific Keywords
#&category_root= Numerical Value for category. 7 = Electronics


def firstPass(pNum):
	global rawHtml,tree,pgs,find,items,findpages
#http://www.mercari.com/search/?page=134&status_trading_sold_out=1
	page = requests.get('http://www.mercari.com/search/?page='+str(pNum)+'&status_trading_sold_out=1')
	
	tree = html.fromstring(page.content)
	
	rawHtml = (page.content)

	#findall "items-box" 
	find = re.findall('"items-box"', rawHtml)
	
	#Count how many items on the page
	items = find.count('"items-box"')

	#findall "pager-cell"
	findpages = re.findall('"pager-cell"', rawHtml)
	
	#Count how many pages are found
	pgs = findpages.count('"pager-cell"')
	
	x = 0
	
	while (x < items):
		
		t1 = tree.xpath('/html/body/div/main/div[1]/section/div/section['+str(x)+']/a/div/h3/text()')
		text_file.write("%s\n" % t1)
		
		
		
		sql_insert = "(INSERT INTO Products"
		"(title)"
		"VALUES (%s)"
		
		print "Pushing to DB."+str(t1)+""
		
		
		
		#print(t1)
		x = x + 1
		#text_file.write("==================PAGE===============" + str(PageNumber))




 
text_file = open("titles.txt","wb")

PageNumber = 1	
	
firstPass(PageNumber)
	

while PageNumber < 100: 
	PageNumber = PageNumber + 1
	firstPass(PageNumber)
	time.sleep(1)
	print("Processed............ " +str(PageNumber))
	
if PageNumber == 100:
	print("Processed " +str(PageNumber) + " pages.")

text_file.close()

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)	
		

print "CLEAN UP WILL BEGIN"
time.sleep(2)
print "Removing [ "
replaceAll("titles.txt","[","")

print "Removing ] "
replaceAll("titles.txt","]","")

print "Removing ' "
replaceAll("titles.txt","'","")
print "Removing , "
replaceAll("titles.txt",",","")
print "Removing \ "
replaceAll("titles.txt","\\","")
time.sleep(2)
os.system('cls')
print "Upload to DB will begin in 5 seconds"
time.sleep(5)

'''mercDB.MercSQL()'''


