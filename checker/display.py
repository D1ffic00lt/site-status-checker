import schedule
import os

from checker.sitestatuschecker import SiteStatusChecker

class Display(object):
    def __init__(self):
        self.worker = None
        self.get_file_name()

    def get_file_name(self):
        filename = input("Enter filename (csv): ")
        if not os.path.exists(filename):
            print("File is not exists")
            self.get_file_name()
        ignore_errors = True if input("Ignore errors in csv? (Y/N): ").lower() == "y" else False
        print_errors = False
        if ignore_errors:
            print_errors = True if input("Print errors? (Y/N): ").lower() == "y" else False

        worker = SiteStatusChecker(filename)
        worker.IGNORE_ERRORS = ignore_errors
        worker.YIELD_ERRORS = print_errors

        self.worker = worker
        print("Worker created")

    def create_schedule(self):
        self.show()
        schedule.every().hour.do(self.show)
        while True:
            schedule.run_pending()

    def show(self):
        print("\nCheck starting...\n")
        for i in self.worker():
            if i is not None:
                print(i)
        print("\nCheck completed!")