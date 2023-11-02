import datetime

from cstriggers.core.trigger import QuartzCron


class Trigger:
    """
    Trigger class for scheduling events based on Quartz Cron expressions.
    """

    def __init__(
        self,
        quartz_expression,
        infinite=True,
        start_date=None,
        end_date=None,
        default_week_delta=208,
    ) -> None:
        """
        Initialize a Trigger instance.

        Args:
            quartz_expression (str): A Quartz Cron expression.
            infinite (bool): Whether the trigger should run infinitely.
            start_date (datetime.datetime, optional): The start date for the trigger.
            end_date (datetime.datetime, optional): The end date for a finite run.
            default_week_delta (int, optional): The default number of weeks to run.

        Raises:
            ValueError: If the parameters are invalid.
        """
        if start_date is not None:
            if not isinstance(start_date, datetime.datetime):
                raise ValueError("Start date must be a datetime.datetime obj or none")

        if quartz_expression is None:
            raise ValueError("Must have and expression")

        if start_date is None:
            start_date = datetime.datetime.now()

        if infinite == False:
            if end_date is None:
                raise ValueError(
                    "End date must be a datetime.datetime obj for finite run"
                )
            elif end_date is not None:
                if not isinstance(end_date, datetime.datetime):
                    raise ValueError(
                        "End date must be a datetime.datetime obj for finite run"
                    )
            elif start_date >= end_date:
                raise ValueError("End date must be smaller than start date")

        self.default_week_delta = default_week_delta
        self.start_date = start_date
        self.end_date = start_date + datetime.timedelta(weeks=self.default_week_delta)
        self.current_trigger = start_date
        self.quartz_expression = quartz_expression
        self.infinite = infinite
        self.check_expression_and_assign()

        if self.cron is None:
            raise ValueError("Invalid cron expression")

    def check_expression_and_assign(self):
        """
        Check the Quartz Cron expression and assign the QuartzCron instance.

        Raises:
            ValueError: If the Quartz Cron expression is invalid.
        """
        try:
            self.cron = QuartzCron(
                self.quartz_expression,
                start_date=self.start_date,
                end_date=self.end_date,
            )
        except Exception as e:
            self.cron = None

    @classmethod
    def check_valid_cron_or_not(cls, quartz_expression):
        """
        Check if a given Quartz Cron expression is valid.

        Args:
            quartz_expression (str): A Quartz Cron expression.

        Returns:
            bool: True if the expression is valid, False otherwise.
        """
        try:
            Trigger(quartz_expression).get_next()
            return True
        except:
            return False

    def get_next(self):
        """
        Get the next trigger date based on the Quartz Cron expression.
        if it is not infinite then return None on its end

        Returns:
            datetime.datetime: The next trigger date.
        """
        while True:
            try:
                self.current_trigger = datetime.datetime.strptime(
                    self.cron.next_trigger(isoformat=True), "%Y-%m-%dT%H:%M:%S.%f"
                ).replace(microsecond=0)

                return self.current_trigger

            except Exception as e:
                if self.infinite == False:
                    return None

                self.start_date = self.end_date
                self.end_date = self.start_date + datetime.timedelta(
                    weeks=self.default_week_delta
                )
                del self.cron
                self.check_expression_and_assign()
                if self.cron is None:
                    raise ValueError("Invalid cron expression")
