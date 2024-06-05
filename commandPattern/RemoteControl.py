
### 1. Define the Command Interface

from abc import ABC, abstractmethod

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


### 2. Implement Concrete Command Classes

class TurnOnCommand(Command):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_on()

    def undo(self):
        self.device.turn_off()

    def redo(self):
        self.execute()

class TurnOffCommand(Command):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_off()

    def undo(self):
        self.device.turn_on()

    def redo(self):
        self.execute()

class AdjustVolumeCommand(Command):
    def __init__(self, ipod, volume):
        self.ipod = ipod
        self.volume = volume
        self.previous_volume = ipod.volume

    def execute(self):
        self.previous_volume = self.ipod.volume
        self.ipod.adjust_volume(self.volume)

    def undo(self):
        self.ipod.adjust_volume(self.previous_volume)

    def redo(self):
        self.execute()

class ChangeChannelCommand(Command):
    def __init__(self, tv, channel):
        self.tv = tv
        self.channel = channel
        self.previous_channel = tv.channel

    def execute(self):
        self.previous_channel = self.tv.channel
        self.tv.change_channel(self.channel)

    def undo(self):
        self.tv.change_channel(self.previous_channel)

    def redo(self):
        self.execute()


### 3. Create Receiver Classes

class TV:
    def __init__(self):
        self.channel = 1

    def turn_on(self):
        print("TV is now on")

    def turn_off(self):
        print("TV is now off")

    def change_channel(self, channel):
        self.channel = channel
        print(f"Channel changed to {channel}")

class Ipod:
    def __init__(self):
        self.volume = 5

    def turn_on(self):
        print("Ipod is now on")

    def turn_off(self):
        print("Ipod is now off")

    def adjust_volume(self, volume):
        self.volume = volume
        print(f"Volume adjusted to {volume}")

class Fan:
    def __init__(self):
        self.speed = 0

    def turn_on(self):
        print("Fan is now on")

    def turn_off(self):
        print("Fan is now off")

    def adjust_speed(self, speed):
        self.speed = speed
        print(f"Fan speed adjusted to {speed}")


### 4. Implement an Invoker Class

class RemoteControl:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def set_command(self, command):
        self.command = command

    def press_button(self):
        self.command.execute()
        self.undo_stack.append(self.command)
        self.redo_stack.clear()

    def press_undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def press_redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.redo()
            self.undo_stack.append(command)


### 5. Putting It All Together

if __name__ == "__main__":
    # Create devices
    tv = TV()
    ipod = Ipod()
    fan = Fan()

    # Create command objects
    turn_on_tv = TurnOnCommand(tv)
    turn_off_tv = TurnOffCommand(tv)
    adjust_volume_ipod = AdjustVolumeCommand(ipod, 10)
    change_channel_tv = ChangeChannelCommand(tv, 5)
    turn_on_fan = TurnOnCommand(fan)
    adjust_speed_fan = AdjustVolumeCommand(fan, 3)

    # Create remote control
    remote = RemoteControl()

    # Set and execute commands
    remote.set_command(turn_on_tv)
    remote.press_button()  # Outputs: TV is now on

    remote.set_command(adjust_volume_ipod)
    remote.press_button()  # Outputs: Volume adjusted to 10

    remote.set_command(change_channel_tv)
    remote.press_button()  # Outputs: Channel changed to 5

    remote.set_command(turn_on_fan)
    remote.press_button()  # Outputs: Fan is now on

    remote.set_command(adjust_speed_fan)
    remote.press_button()  # Outputs: Fan speed adjusted to 3

    # Undo the last command
    remote.press_undo()  # Outputs: Fan speed adjusted to 0

    # Redo the last undone command
    remote.press_redo()  # Outputs: Fan speed adjusted to 3
