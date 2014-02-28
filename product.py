class Product:
	def putName(self, productName):
		self.name = productName
	def putStyleId(self, styleId):
		try:
			self.styleId.append(styleId)
		except NameError:
			self.styleId = []
			self.styleId.append(styleId)
	def putProductId(self, productId):
		self.productId = productId
	def putPrice(self, price):
		self.price = float(price)
	def __init__(self,productId, name, price):
		self.styleId = []
		self.productId = productId
		self.price = float(price)
		self.name = name

		
