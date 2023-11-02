import colorama


class ProgressBar:
    """
    A simple text-based progress bar class that uses Colorama for colored output.
    """

    def __init__(
        self,
        total,
        progress=0,
        counter=1,
        color=colorama.Fore.YELLOW,
        end_color=colorama.Fore.GREEN,
    ):
        """
        Initializes a ProgressBar instance.

        Args:
            total (int): The total number of items in the task.
            progress (int, optional): The current progress value (default is 0).
            counter (int, optional): The amount by which the progress increases in each update (default is 1).
            color (str, optional): The color to use for the progress bar (default is colorama.Fore.YELLOW).
            end_color (str, optional): The color to use for the progress bar when it reaches 100% (default is colorama.Fore.GREEN).
        """
        self.total = total
        self.progress = progress
        self.counter = counter
        self.color = color
        self.end_color = end_color

    def update(self):
        """
        Updates the progress bar and displays it in the console.

        This method increases the progress by the counter value, calculates the percentage of completion, and
        prints a text-based progress bar to the console using colored output.
        """
        self.progress += self.counter
        percent = 100 * (self.progress / float(self.total))
        # "█" <- alt + (2 + 1 + 9) from num pad
        bar = "█" * int(percent) + "-" * (100 - int(percent))

        if int(percent) < 100:
            print(self.color + f"\r|{bar}|{percent:.2f}%", end="\r")
        else:
            print(
                self.end_color + f"\r|{bar}|{percent:.2f}%" + colorama.Fore.RESET,
                end="\n",
            )
