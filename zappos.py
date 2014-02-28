import urllib2
import json
import re
import product
import itertools
import sys
import argparse


#http://stackoverflow.com/questions/4632322/finding-all-possible-combinations-of-numbers-to-reach-a-given-sum
#Finding all sets of items which add approximately to the given value
def subset_sum(listOfItems, listOfPrices, size, numbers, target, partial=[]):
	try:
		s = sum(partial)

		# check if the partial sum is equals to target
		if s == target and len(partial) == size:
			print "Ready to display final list...please wait for a moment"
			finalListOfProducts = []
			for prices in partial:
				listOfProductsOfParticularPrice = []
				productIdsFromDictionary = listOfPrices[prices]
				for productIdFromDictionary in productIdsFromDictionary:
					productObject = listOfItems[productIdFromDictionary]
					name = productObject.name
					price = productObject.price
					listOfProductsOfParticularPrice.append(name+":"+str(price))
				finalListOfProducts.append(listOfProductsOfParticularPrice)
				finalListForUsers = list(itertools.product(*finalListOfProducts))
				for combinationOfProduct in finalListForUsers:
					total = 0
					for product in combinationOfProduct:
						productSplit = product.split(":")
						price = float(productSplit[1])
						total +=price
					if total <target:
						for product in combinationOfProduct:
							print product
						print "Total: $"+str(total)
					print "\n"
		if s >= target:
			return  # if we reach the number why bother to continue
		for i in range(len(numbers)):
			n = numbers[i]
			remaining = numbers[i+1:]
			subset_sum(listOfItems, listOfPrices, size, remaining, target, partial + [n]) 
	except Exception, e:
		print e



#To take command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("budget", type=float, help="Your total budget")
parser.add_argument("number", type=int, help="The total number of items you need")
args = parser.parse_args()

#Defining the variables
key = "12c3302e49b9b40ab8a222d7cf79a69ad11ffd78"
order = "{\"price\":\"asc\"}"
url = "http://api.zappos.com/Search?key="+key+"&sort="+order+"&limit=100&includes=[\"pageCount\"]"
listOfItems = {}#Dictionary with productId as key and details as value
listOfPrices = {}#Dictionary with Price as key and list of productIds as value
pagecount=0
maxPrice = args.budget
flag = True
size = args.number
try:#Initial url call for 1st page. This also gives the pagecount which we use later
	print "Initial url call \n"
	response = urllib2.urlopen(url).read()
	jsonResponse = json.loads(response)
	pagecountFromResponse = jsonResponse['pageCount']
	pagecount = int(pagecountFromResponse)	
	items = jsonResponse['results']
	for item in items:
		name = item['productName']
		productId = item['productId']
		styleId = item['styleId']
		price = item['price']
		price = price.lstrip('$')
		floatPrice = float(price)
		intPrice = int(floatPrice)
		if floatPrice>maxPrice:
			break
		numberOfCents = floatPrice%1
		#Approximating the values of product by increasing the dollar value by 1 whose number of cents exceeds 49 cents
		if numberOfCents > 0.49 and numberOfCents < 1.0:
			intPrice = intPrice+1
			if intPrice in listOfPrices:
				productList = listOfPrices[intPrice]
				if productId in productList:
					pass
				else:
					productList.append(productId)
					listOfPrices[intPrice] = productList
			else:
				listOfProductId = []
				listOfProductId.append(productId)
				listOfPrices[intPrice] =  listOfProductId
		else:#Just taking the dollar value of the products and creating the listOfPrices dictionary
			if intPrice in listOfPrices:
				productList = listOfPrices[intPrice]
				if productId in productList:
					pass
				else:
					productList.append(productId)
					listOfPrices[intPrice] = productList
			else:
				listOfProductId = []
				listOfProductId.append(productId)
				listOfPrices[floatPrice] = listOfProductId
			

		#Creating the dictionary for listOfItems dictionary
		
		if productId in listOfItems and float(price) == listOfItems[productId].price:
			productObject = listOfItems[productId]
			productObject.putStyleId(styleId)
			listOfItems[productId] = productObject
		else:
			productObject = product.Product(productId, name, price)
			productObject.putStyleId(styleId)
			listOfItems[productId] = productObject
except Exception, e:
	print e
#Subsequent url calls till the price of items exceeds our budget
print "Next set of url calls...might take some time \n"
for x in range(2,pagecount):
	if flag:
		try:
			response = urllib2.urlopen(url+"&page="+str(x)).read()
			jsonResponse = json.loads(response)
			items = jsonResponse['results']
			for item in items:
				itemPrice = item['price']
				itemPrice = itemPrice.lstrip('$')
				itemPrice = float(itemPrice)
				intPrice = int(itemPrice)
				numberOfCents = itemPrice%1
				#Approximating to extra dollar value for cents exceeding 49 cents
				if numberOfCents > .49 and numberOfCents < .99:
					intPrice = intPrice+1
					if intPrice in listOfPrices:
						productList = listOfPrices[intPrice]
						if productId in productList:
							pass
						else:
							productList.append(productId)
							listOfPrices[intPrice] = productList
					else:
						listOfProductId = []
						listOfProductId.append(productId)
						listOfPrices[intPrice] =  listOfProductId
				else:#Just taking the dollar value
					if intPrice in listOfPrices:
						productList = listOfPrices[intPrice]
						if productId in productList:
							pass
						else:
							productList.append(productId)
							listOfPrices[intPrice] = productList
					else:
						listOfProductId = []
						listOfProductId.append(productId)
						listOfPrices[intPrice] = listOfProductId
					
					
				if itemPrice > maxPrice:
					flag = False
					break
				else:
					name = item['productName']
                			productId = item['productId']
                			styleId = item['styleId']
                			price = item['price']
                			price = price.lstrip('$')
                #price = float(price)
                			if productId in listOfItems and itemPrice == listOfItems[productId].price:
                        			productObject = listOfItems[productId]
                        			productObject.putStyleId(styleId)
                       	 			listOfItems[productId] = productObject
                			else:
                       				productObject = product.Product(productId, name, price)
                       				productObject.putStyleId(styleId)
                       				listOfItems[productId] = productObject
						
		except Exception, e:
			print e
	else:
		break
try:		
	print "URL calls made...calculating best combination"
	listOfKeys = list(listOfPrices.keys())
	subset_sum(listOfItems,listOfPrices, size,listOfKeys,maxPrice)
except Exception, e:
	print e
		
		
