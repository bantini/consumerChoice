consumerChoice
==============
This uses the Zappos API to display the products which add to the input budget. 2 inputs are taken through the command line, the budget for shopping and the number of products required within this budget. 

Input:  Budget: Float
        Number of Products: Int
Output: List of products which add up to this price range

Program to display optimal options for consumers

Usage : python zappos.py budget number_of_products
E.g: python zappos.py 150.0 5

PS:It uses an approximation algorithm which does not really add up to the exact amount
I am not sure if the API key is public.
