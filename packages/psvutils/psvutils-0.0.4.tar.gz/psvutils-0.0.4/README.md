# psvutils

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Pritam Sarkar 1995 from [pritamSarkar123](https://github.com/pritamSarkar123) (c) 2023

## Examples of How To Use (Alpha Version + Buggy)

Creating A Progressbar

```python
from psvutils import Progressbar

pb = ProgressBar(total=200)

for _ in range(200):
    """main code block"""
    pb.update()

```

```
(venv) C:\***\***>python main.py
████████████████████████████████████████████████████████████████████████████████████████████████████|100.00%
```

```python
"""
    Args:
        total (int): The total number of items in the task.
        progress (int, optional): The current progress value (default is 0).
        counter (int, optional): The amount by which the progress increases in each update (default is 1).
        color (str, optional): The color to use for the progress bar (default is colorama.Fore.YELLOW).
        end_color (str, optional): The color to use for the progress bar when it reaches 100% (default is colorama.Fore.GREEN).
    Returns:
        A Progressbar instance
"""
```

Creating a quartz cron based trigger

```python
from psvutils import Trigger
tr = Trigger("0 * 0 ? * * *", start_date=datetime.datetime.now())

print(Trigger.check_valid_cron_or_not("0 * 0 ? * * *"))

for _ in range(20):
    """next 20 triggers"""
    print(tr.get_next())
```

```
(venv) C:\***\***>python main.py
True
2023-10-19 13:49:00
2023-10-19 13:50:00
2023-10-19 13:51:00
2023-10-19 13:52:00
2023-10-19 13:53:00
2023-10-19 13:54:00
2023-10-19 13:55:00
2023-10-19 13:56:00
2023-10-19 13:57:00
2023-10-19 13:58:00
2023-10-19 13:59:00
2027-10-14 13:49:00
2027-10-14 13:50:00
2027-10-14 13:51:00
2027-10-14 13:52:00
2027-10-14 13:53:00
2027-10-14 13:54:00
2027-10-14 13:55:00
2027-10-14 13:56:00
2027-10-14 13:57:00
```

```python
"""
    Args:
        quartz_expression (str): A Quartz Cron expression.
        infinite (bool): Whether the trigger should run infinitely.
        start_date (datetime.datetime, optional): The start date for the trigger.
        end_date (datetime.datetime, optional): The end date for a finite run.
        default_week_delta (int, optional): The default number of weeks to run.

    Returns:
        A Trigger instance
"""
```
