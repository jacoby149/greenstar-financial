## Get That Money

### 1. Objective

1. Design a systematic way of forming visual receipts for the future, with choice level of detail, also preventing double payment.
2. Have this system be separate from manufacturing. Existing platforms generically bundle in manufacturing.
3. Instead send a signal that makes "manufacturing" happen.
4. Design a systematic way of accepting payments online for the future. Easily integrate this system into any site, Html, Squarespace, etc. Just by injecting html code.



### 2. Accepting Payments

1. There is a page with login, that allows the Stripe token of a receipt page to be modified.

2. The page allows adding of entries :

   item_name : ...

   ​	base_price :

   ​	recurring_pay:

   ​	description :

   ​	option_name: ...

   ​		picture:

   ​		description:

   ​		added_price:

   ​		recurring_pay:

   An easy implementations can add items from an external source into this receipt system.

   Don't need to keep track of competing options, because we are only interested in summing up costs. 

   ​		 

### 2. Receipts

1. Receipts hold a list of items, with pictographs of those items and descriptions of item options, or just descriptions.
2. Receipts have a paid or not paid status, and a link to pay the receipt if not paid.
3. The payment goes to a specified stripe token.