import unittest

TEST_FOLDER = "tests"

def test_group_by_dst():

    loader = unittest.TestLoader()
    group_by_dst = loader.discover(TEST_FOLDER, pattern="Test_group*.py")

    return group_by_dst
  
def main():
    

    loader = test_group_by_dst()    

    runner = unittest.TextTestRunner()
    runner.run(loader)

if __name__=="__main__":
    main()
