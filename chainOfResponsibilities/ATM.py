from abc import ABC, abstractmethod

class BillsCounter:
    def __init__(self, one, two, five, ten, twenty, fifty, hundred):
        self.one = one
        self.two = two
        self.five = five
        self.ten = ten
        self.twenty = twenty
        self.fifty = fifty
        self.hundred = hundred

class DollarBill(ABC):
    def __init__(self, next_bill=None):
        self.next_bill = next_bill
        self.amount = 0

    def set_next(self, next_bill):
        self.next_bill = next_bill

    def despense(self, bills_counts: BillsCounter, amount: int):
        self._despense(bills_counts, amount)
        if self.amount > 0 and self.next_bill:
            self.next_bill.despense(bills_counts, self.amount)
        elif self.amount > 0:
            print(f"Not enough bills to despense remaining ${self.amount}")

    @abstractmethod
    def _despense(self, bills_counts: BillsCounter, amount: int):
        pass

class Dollar100Bill(DollarBill):
    def _despense(self, bills_counts: BillsCounter, amount: int):
        bills_required = amount // 100
        bills_available=  bills_counts.hundred
        if bills_required > 0 and  bills_available>0:
            give = min(bills_available, bills_required)
            bills_counts.hundred -= give
            amount -= give * 100
            print(f"$100 Bills: {give}")
        self.amount = amount

class Dollar50Bill(DollarBill):
    def _despense(self, bills_counts: BillsCounter, amount: int):
        bills_required = amount // 50
        if bills_required > 0 and bills_counts.fifty > 0:
            give = min(bills_counts.fifty, bills_required)
            bills_counts.fifty -= give
            amount -= give * 50
            print(f"$50 Bills: {give}")
        self.amount = amount

class Dollar20Bill(DollarBill):
    def _despense(self, bills_counts: BillsCounter, amount: int):
        bills_required = amount // 20
        if bills_required > 0 and bills_counts.twenty > 0:
            give = min(bills_counts.twenty, bills_required)
            bills_counts.twenty -= give
            amount -= give * 20
            print(f"$20 Bills: {give}")
        self.amount = amount

class Dollar10Bill(DollarBill):
    def _despense(self, bills_counts: BillsCounter, amount: int):
        bills_required = amount // 10
        if bills_required > 0 and bills_counts.ten > 0:
            give = min(bills_counts.ten, bills_required)
            bills_counts.ten -= give
            amount -= give * 10
            print(f"$10 Bills: {give}")
        self.amount = amount

class Dollar5Bill(DollarBill):
    def _despense(self, bills_counts: BillsCounter, amount: int):
        bills_required = amount // 5
        if bills_required > 0 and bills_counts.five> 0:
            give = min(bills_counts.five, bills_required)
            bills_counts.five -= give
            amount -= give * 5
            print(f"$5 Bills: {give}")
        self.amount = amount

class Dollar2Bill(DollarBill):
    def _despense(self, bills_counts: BillsCounter, amount: int):
        bills_required = amount // 2
        if bills_required > 0 and bills_counts.two> 0:
            give = min(bills_counts.two, bills_required)
            bills_counts.two -= give
            amount -= give * 2
            print(f"$2 Bills: {give}")
        self.amount = amount

class Dollar1Bill(DollarBill):
    def _despense(self, bills_counts: BillsCounter, amount: int):
        bills_required = amount
        if bills_required > 0 and bills_counts.one> 0:
            give = min(bills_counts.one, bills_required)
            bills_counts.one -= give
            amount -= give
            print(f"$1 Bills: {give}")
        self.amount = amount

class ATM():
    def __init__(self, bills: BillsCounter):
        self.bills_count = bills

    def configure_bill_chain(self):
        one_dollar = Dollar1Bill()
        two_dollar = Dollar2Bill(one_dollar)
        five_dollar = Dollar5Bill(two_dollar)
        ten_dollar = Dollar10Bill(five_dollar)
        twenty_dollar = Dollar20Bill(ten_dollar)
        fifty_dollar = Dollar50Bill(twenty_dollar)
        hundred_dollar = Dollar100Bill(fifty_dollar)
        return hundred_dollar

    def withdraw(self, amount):
        billsObject = self.configure_bill_chain()
        billsObject.despense(self.bills_count, amount)

# Example Usage
if __name__ == "__main__":
    bills = BillsCounter(0, 2, 2, 1, 5, 2, 1)
    atmObject = ATM(bills)
    atmObject.withdraw(288)
