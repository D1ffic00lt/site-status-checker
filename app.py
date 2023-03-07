from checker.sitestatuschecker import SiteStatusChecker

if __name__ == "__main__":
    print("start")
    checker_ = SiteStatusChecker("checker/units/test.csv")
    checker_.IGNORE_ERRORS = True
    checker_.YIELD_ERRORS = True
    for i in checker_():
        print(i)

    print("stop")
