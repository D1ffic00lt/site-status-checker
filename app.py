import time

from checker.sitestatuschecker import SiteStatusChecker

if __name__ == "__main__":
    while True:
        print(1)
        checker_ = SiteStatusChecker("checker/units/test.csv")
        checker_.IGNORE_ERRORS = True
        for i in checker_():
            print(i)
        print(2)
        time.sleep(5)
