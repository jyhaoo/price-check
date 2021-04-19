# priceCheck

I made this web scraper as a way to check the prices of clothing and shoes I would like to buy later.
It takes a while to type in all the information in the browser only to get a response so why not send the http GET faster to get all the information faster. 

## How it works
Takes in a text file and reads through them in order to get the information for the items wanted to be searched. You can either take a look at example.txt or here:
```
'brand' 'url link' 'price' 'product name'
```

## Future updates
Currently this only does adidas. 
The way this script works is that it utilizes the beautifulsoup package which searches the html response for the div tags.
Websites have different formats.
For example, adidas has the price under the div class 'gl-price-item'. 
To support other brand I will need to check the other websites for the class_ tags
Also possibly add a pytest file to check all the functions.
Great way to learn and practice pytests.
