 ## Electronics Sales Analytics
## Project overview
This Python project analyzes electronics sales from a csv file C:\lux_projects\Python\Projects\tech_hub_ke\data\electronics_sales.csv . It reads the CSV, cleans numeric values, calculates revenue and statistics, and uses pandas to verify the results.
The project came with a starter code bearing what functions should be created in it and you make the rest happen.


## Highlights
•	From the 50 rows and 7 columns only 3 rows couldn’t be calculated as intended due to errors in the quantity or the prices varying.
•	The prices of the products varied differently in the same shop and the same day for unknown reasons.
•	This are the basic numbers: 
## Rows: 50
## Columns: ['sale_id', 'sale_date', 'store', 'product', 'quantity', 'unit_price_kes', 'payment_method']
## Clean rows: 47
## Skipped rows: 3
Skipped: {'sale_id': 'S-3030', 'row_number': 31, 'reason': 'unit price is missing or invalid'}
Skipped: {'sale_id': 'S-3035', 'row_number': 36, 'reason': 'quantity is missing or invalid'}
Skipped: {'sale_id': 'S-3039', 'row_number': 40, 'reason': 'unit price is missing or invalid'}

## Total revenue: KES 1,317,210.00

## Revenue By Store
Kisumu Mega Plaza: KES 449,678.00
Nairobi CBD: KES 337,483.00 
Westgate: KES 235,979.00
Mombasa City Mall: KES 154,082.00
Nakuru Westside: KES 139,988.00

## Revenue by product:
HP 15 Laptop: KES 389,994.00
Hisense 43in Smart TV: KES 272,993.00
Lenovo Tab M10: KES 199,992.00
Tecno Spark 20: KES 161,988.00
Infinix Hot 40: KES 63,996.00
Samsung Galaxy A15: KES 56,997.00
JBL Go 3 Speaker: KES 49,491.00
Anker Power Bank 20000: KES 38,691.00
Xiaomi Redmi Buds: KES 31,990.00
Oraimo FreePods: KES 19,593.00
USB-C Charger 25W: KES 19,487.00
Safaricom Neon Ray: KES 11,998.00

## Top three products:
HP 15 Laptop: KES 389,994.00
Hisense 43in Smart TV: KES 272,993.00
Lenovo Tab M10: KES 199,992.00

## Sales at or above KES 50,000.00:
1.	S-3022 | HP 15 Laptop | Nairobi CBD | KES 259,996.00
2.	S-3017 | Hisense 43in Smart TV | Kisumu Mega Plaza | KES 155,996.00
3.	S-3048 | HP 15 Laptop | Kisumu Mega Plaza | KES 129,998.00
4.	S-3013 | Lenovo Tab M10 | Westgate | KES 99,996.00
5.	S-3036 | Tecno Spark 20 | Nakuru Westside | KES 53,996.00

## The Numbers
Mean transaction revenue: KES 28,025.74
Median transaction revenue: KES 10,998.00
Minimum transaction revenue: KES 1,499.00
Maximum transaction revenue: KES 259,996.00


## Data cleaning rules
The program applies these rules to “quantity” and “unit_price_kes”:
•	Trims whitespace around values.
•	Removes commas used as separators in thousands place value, so “38,999” becomes “38999”.
•	Removes the leading “KES “from prices, so “KES 18999” becomes “18999”. This changes it to a numerical value from a string
•	Converts the word “two” to “2” for the quantity in sale “S-3006”. Uniformity in the columns thus easy calculations otherwise it would have been listed as “None”
•	 Skips rows with missing or invalid quantities or prices.
•	 Skips rows with negative quantities or prices. Zero values are allowed. 
•	Skipped rows are reported with their sale ID, CSV row number, and reason.


## Analysis
The program calculates total revenue as quantity multiplied by unit price. It reports revenue by product, store, and payment method; lists the top three products; filters transactions at or above KES 50,000; and calculates mean, median, minimum, and maximum transaction revenue.
During my research, I incorporated use of other tools such “Lambda” (allows you to create small functions without using “def”)
Found the max, min, mean, median and the mode transactions.
When product revenues tie, product names are sorted alphabetically.


## Verification
At the end of the project. I used pandas to confirm if the numbers were as they were intended to be
