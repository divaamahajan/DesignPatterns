from abc import ABC, abstractmethod

# Receiver class
class Document:
    def __init__(self):
        self.text = ""

    def insert(self, text, position):
        self.text = self.text[:position] + text + self.text[position:]

    def delete(self, position, length):
        self.text = self.text[:position] + self.text[position + length:]

    def __str__(self):
        return self.text

# Define the Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass
    
    @abstractmethod
    def redo(self):
        pass

#  Implement Concrete Command Classes
class InsertTextCommand(Command):
    def __init__(self, document, text):
        self.document = document
        self.text = " "+text
        self.position = len(self.document.text)  # Always append at the end

    def execute(self):
        self.document.insert(self.text, self.position)

    def undo(self):
        self.document.delete(self.position, len(self.text))

    def redo(self):
        self.execute()

class DeleteTextCommand(Command):
    def __init__(self, document, length):
        self.document = document
        self.length = length
        self.position = len(self.document.text) - length
        self.deleted_text = ""

    def execute(self):
        self.deleted_text = self.document.text[self.position:self.position + self.length]
        self.document.delete(self.position, self.length)

    def undo(self):
        self.document.insert(self.deleted_text, self.position)

    def redo(self):
        self.execute()

#  Implement an Invoker(Sender) Class
class CommandManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def execute_command(self, command:Command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.redo()
            self.undo_stack.append(command)

if __name__ == "__main__":
    document = Document()
    text_editor = CommandManager()

    print("Initial text:", document)

    # Insert "Hello"
    insert_command = InsertTextCommand(document, "Hello")
    text_editor.execute_command(insert_command)
    print("After inserting 'Hello':", document)

    # Insert " World"
    insert_command = InsertTextCommand(document, "World")
    text_editor.execute_command(insert_command)
    print("After inserting 'World':", document)

    # Insert " Dear"
    insert_command = InsertTextCommand(document, "Dear")
    text_editor.execute_command(insert_command)
    print("After inserting 'Dear':", document)

    # Insert " Old"
    insert_command = InsertTextCommand(document, "Old")
    text_editor.execute_command(insert_command)
    print("After inserting 'Old':", document)

    # Insert " friend"
    insert_command = InsertTextCommand(document, "friend")
    text_editor.execute_command(insert_command)
    print("After inserting 'friend':", document)

    # Undo last command
    text_editor.undo()
    print("After undo:", document)

    # Undo last command
    text_editor.undo()
    print("After undo:", document)

    # Undo last command
    text_editor.undo()
    print("After undo:", document)

    # Redo last command
    text_editor.redo()
    print("After redo:", document)

    # Redo last command
    text_editor.redo()
    print("After redo:", document)

    # Delete last 6 characters 
    delete_command = DeleteTextCommand(document, 6)
    text_editor.execute_command(delete_command)
    print("After deleting ' last 6 characters':", document)

    # Undo delete command
    text_editor.undo()
    print("After undo delete:", document)


    # Undo delete command
    text_editor.undo()
    print("After undo previous command:", document)