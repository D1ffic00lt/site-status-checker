from checker.units.sitestatuschecker import SiteStatusChecker

if __name__ == "__main__":
    print("start")
    checker_ = SiteStatusChecker("checker/units/test.csv")
    checker_.IGNORE_ERRORS = False
    checker_.YIELD_ERRORS = False
    for i in checker_():
        print(i)

    print("stop")
