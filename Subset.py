import itertools
import product


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