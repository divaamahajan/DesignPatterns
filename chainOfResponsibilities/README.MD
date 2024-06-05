## Chain of Responsibility Pattern

The Chain of Responsibility pattern allows a request to be passed through a chain of handlers, with each handler deciding either to process the request or to pass it to the next handler. This pattern promotes loose coupling and flexibility in handling requests dynamically at runtime.

### Simple Explanation

Think of the Chain of Responsibility like passing a message along a line of people. Let's say you have a problem and you're not sure who can solve it. You start by asking the first person in line. If they can't help, they pass it to the next person, and so on until someone can solve it or until you've asked everyone.

In programming, it's similar. You have a task or request, and you pass it to the first "handler" in the chain. If that handler can't handle it, they pass it to the next handler, and so on until someone can deal with it. It's a way to handle requests without knowing in advance who will handle them, making your code more flexible and easy to change later on.

Here's how it works:

1. **Request**: An initial request is made by a client or sender.
2. **Handler**: Each handler in the chain contains logic to process the request or pass it to the next handler.
3. **Chain**: Handlers are linked together to form a chain. When a request is made, it's passed along this chain until one of the handlers decides to handle it.
4. **Processing**: Handlers in the chain can either handle the request themselves or delegate it to the next handler in the chain.
5. **Termination**: The chain continues until a handler successfully processes the request or until the end of the chain is reached without any handler handling the request.

![Chain of Responsibility Pattern](https://upload.wikimedia.org/wikipedia/commons/6/6a/W3sDesign_Chain_of_Responsibility_Design_Pattern_UML.jpg)
*Image credit: W3sDesign - Chain of Responsibility Design Pattern UML*

This pattern is useful when the processing logic for a request may vary and needs to be determined dynamically. It simplifies adding or removing processing logic without affecting other parts of the system.


## Example

1. **ATM Example**:
   - Imagine you're at an ATM and you want to withdraw money. You insert your card and enter the amount.
   - The ATM needs to check if it has enough bills of various denominations to dispense the requested amount.
   - The Chain of Responsibility pattern could be applied here: 
     - The ATM first checks if it has enough $100 bills. If it does, it dispenses them and completes the transaction.
     - If not, it passes the request to the next handler, which checks for $50 bills.
     - If still not enough, it passes to the next handler for $20 bills, and so on until $1 bills.
     - If none of the handlers can fulfill the request, the ATM displays an error message saying it cannot dispense the requested amount.

   [ATM Chain of Responsibility Example Code](https://github.com/divaamahajan/DesignPatterns/blob/main/chainOfResponsibilities/ATM.py)



2. **Logger Example**:
   - Suppose you have a logging system where different types of messages need to be logged at different levels (e.g., info, warning, error).
   - Each logger has a different threshold level it can handle. If a message's severity level is below this threshold, the logger handles it; otherwise, it passes it to the next logger.
   - For example:
     - An error logger handles messages with severity "error" or higher.
     - A warning logger handles messages with severity "warning" or higher.
     - An info logger handles all messages.
   - If a message comes in with severity "error", it's handled by the error logger. If it's "warning", it's handled by the warning logger, and so on.
   - If none of the loggers can handle the message (e.g., it's below the threshold for all loggers), it's not logged.

   [Logger Chain of Responsibility Example Code](https://github.com/divaamahajan/DesignPatterns/blob/main/chainOfResponsibilities/Logger.py)


In both cases, the Chain of Responsibility pattern allows for flexible handling of requests or messages without knowing in advance which component will handle them, making the systems easy to extend and maintain.


### Pseudo-code

```python
# Define a handler interface
interface Handler:
    method handleRequest(request)

# Define concrete handler classes
class ConcreteHandlerA implements Handler:
    method handleRequest(request):
        if canHandle(request):
            processRequest(request)
        else:
            if nextHandler != null:
                nextHandler.handleRequest(request)

class ConcreteHandlerB implements Handler:
    method handleRequest(request):
        if canHandle(request):
            processRequest(request)
        else:
            if nextHandler != null:
                nextHandler.handleRequest(request)

# Define a client class to initiate the request
class Client:
    property handlerChain

    method setHandlerChain(handlerChain):
        this.handlerChain = handlerChain

    method sendRequest(request):
        handlerChain.handleRequest(request)

# Usage example
handlerA = ConcreteHandlerA()
handlerB = ConcreteHandlerB()

# Set up the chain
handlerA.setNext(handlerB)

# Create a client and set the handler chain
client = Client()
client.setHandlerChain(handlerA)

# Send requests through the chain
client.sendRequest(request)
```

In this pseudo-code:

- We define a `Handler` interface with a method `handleRequest(request)` to handle the request.
- Concrete handler classes `ConcreteHandlerA` and `ConcreteHandlerB` implement the `Handler` interface. Each handler decides whether it can handle the request or passes it to the next handler in the chain.
- The `Client` class initiates the request and sets up the handler chain.
- Finally, we create instances of concrete handlers, set up the chain, and send requests through the chain using the client.

This template demonstrates the basic structure of implementing the Chain of Responsibility pattern in pseudocode. You can adapt and expand upon it based on your specific requirements and programming language.