from abc import ABC, abstractmethod

class Coin:
    def __init__(self, value):
        self.value = value

class Item:
    def __init__(self, name, price, code):
        self.name = name
        self.price = price
        self.code = code

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item, count):
        self.items[item.code] = {'item': item, 'count': count}

    def get_item(self, code):
        if code in self.items:
            return self.items[code]['item']
        return None

    def get_item_count(self, code):
        if code in self.items:
            return self.items[code]['count']
        return 0

    def update_inventory(self, code):
        if code in self.items:
            self.items[code]['count'] -= 1

class VendingMachine:
    def __init__(self):
        self.state = NoCoinState(self)
        self.balance = 0
        self.selected_product_code = None
        self.inventory = Inventory()

    def set_state(self, state):
        self.state = state

    def add_coin(self, coin):
        self.balance += coin.value
        print(f"Coin inserted: {coin.value} cents. New balance: ", self.balance)

    def insert_coin(self, coin):
        self.state.insert_coin(coin)

    def select_product(self, code):
        self.state.select_product(code)

    def cancel_and_refund(self):
        if self.balance > 0:
            print(f"Returning change: {self.balance} cents.")
            self.balance = 0
        else:
            print("No money to return.")
        self.set_state(NoCoinState(self))

    def dispense_product(self):
        self.state.dispense_product()

    def update_inventory(self, code):
        self.inventory.update_inventory(code)

class State(ABC):
    def __init__(self, vending_machine: VendingMachine):
        self.vending_machine = vending_machine

    @abstractmethod
    def insert_coin(self, coin):
        pass

    @abstractmethod
    def select_product(self, code):
        pass


    @abstractmethod
    def dispense_product(self):
        pass

class NoCoinState(State):
    def insert_coin(self, coin):
        self.vending_machine.add_coin(coin)
        self.vending_machine.set_state(HasCoinState(self.vending_machine))

    def select_product(self, code):
        print("Please insert a coin first.")

    def dispense_product(self):
        print("Please select a product first.")

class HasCoinState(State):
    def insert_coin(self, coin):
        self.vending_machine.add_coin(coin)

    def select_product(self, code):
        item = self.vending_machine.inventory.get_item(code)
        if item is not None:
            print(f"Selected product: {item.name} - Price: {item.price} cents.")
            self.vending_machine.selected_product_code = code
            self.vending_machine.set_state(ProductSelectedState(self.vending_machine))
        else:
            print("Invalid product code.")


    def dispense_product(self):
        print("Please select a product first.")

class ProductSelectedState(State):
    def insert_coin(self, coin):
        self.vending_machine.add_coin(coin)

    def select_product(self, code):
        item = self.vending_machine.inventory.get_item(code)
        print(f"Product {item.name} already selected. Dispense or cancel to continue.")


    def dispense_product(self):
        code = self.vending_machine.selected_product_code
        item = self.vending_machine.inventory.get_item(code)
        if item is not None:
            if self.vending_machine.inventory.get_item_count(code) > 0:
                if self.vending_machine.balance >= item.price:
                    print(f"Dispensing {item.name}")
                    self.vending_machine.balance -= item.price
                    self.vending_machine.update_inventory(code)
                    print(f"Dispensed {item.name}")
                    self.vending_machine.cancel_and_refund()
                else:
                    print("Insufficient balance. Please insert more coins.")
            else:
                print("Product out of stock. Please collect your refund.")
                self.vending_machine.cancel_and_refund()
        else:
            print("Invalid product code.")

# Example Usage
if __name__ == "__main__":
    vending_machine = VendingMachine()
    coin1 = Coin(25)
    coin3 = Coin(25)
    coin2 = Coin(50)
    vending_machine.inventory.add_item(Item("Coke", 50, 1), 1)
    vending_machine.inventory.add_item(Item("Pepsi", 45, 2), 5)


    # insufficient Fund Amount
    vending_machine.insert_coin(coin1)
    vending_machine.select_product(1)
    vending_machine.dispense_product()
    print()

    # success
    vending_machine.insert_coin(coin3)
    vending_machine.insert_coin(coin2)
    vending_machine.select_product(1)
    vending_machine.dispense_product()
    print()

    # out of stock
    vending_machine.insert_coin(coin2)
    vending_machine.select_product(1)
    vending_machine.dispense_product()
    print()