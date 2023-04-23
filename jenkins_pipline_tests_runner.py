from unittest import TestLoader
import HtmlTestRunner

def run_tests():
    test_loader = TestLoader()

    test_directory = ".\\tests"

    test_suite = test_loader.discover(test_directory, pattern='test_*.py')

    runner = HtmlTestRunner.HTMLTestRunner(verbosity=5, report_name="unittest_pro_110822", add_timestamp=False, combine_reports=True, output='\\reports\\unittest')
    runner_result = runner.run(test_suite)

    if runner_result.wasSuccessful():
        print('RESULT:SUCESS')

    else:
        print("===========================================================================")
        print("ERRORS:")
        for error in runner_result.errors:
            print(error)
        print("===========================================================================")


        print("===========================================================================")
        print("FAILUERS:")
        for failure in runner_result.failures:
            print(failure)
        print("===========================================================================")
        print('RESULT:FAILED')
        

if __name__ == '__main__':
    run_tests()