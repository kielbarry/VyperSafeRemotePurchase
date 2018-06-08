#Safe Remote Purchase
#Originally from
#https://github.com/ethereum/solidity/blob/develop/docs/solidity-by-example.rst
#ported to vyper and optimized

#Rundown of the transaction:
#1. Seller posts item for sale and posts safety deposit of double the item value.
# Balance is 2*value.
#(1.1. Seller can reclaim deposit and close the sale as long as nothing was purchased.)
#2. Buyer purchases item (value) plus posts an additional safety deposit (Item value).
# Balance is 4*value.
#3. Seller ships item.
#4. Buyer confirms receiving the item. Buyer's deposit (value) is returned.
#Seller's deposit (2*value) + items value is returned. Balance is 0.


value: public(wei_value)
seller: public(address)
buyer: public(address)
unlocked: public(bool)
#@constant
#def unlocked() -> bool: #Is a refund possible for the seller?
#    return (self.balance == self.value*2)

@public
@payable
def __init__():
	assert (msg.value % 2) == 0
	self.value = msg.value
	self.seller = msg.sender
	self.unlocked = True

@public
def abort():
	assert self.unlocked
	assert msg.sender == self.seller
	selfdestruct(self.seller)

@public
@payable
def purchase():
	assert self.unlocked
	assert msg.value == (2 * self.value)
	self.buyer = msg.sender
	self.unlocked = False

@public
def received():
	assert not self.unlocked 
	assert msg.sender == self.buyer
	send(self.buyer, self.value)
	selfdestruct(self.seller)
