import unittest

TEST_FOLDER = "tests"

def test_group_by_dst(loader):


    group_by_dst = loader.discover(TEST_FOLDER, pattern="Test_group*.py")

    return group_by_dst

def test_average_f107(loader):

    return loader.discover(TEST_FOLDER, pattern="Test_average_f107.py")

  
def main():
    loader = unittest.TestLoader()

    #test_group = test_group_by_dst(loader)
    test_group = test_average_f107(loader)

    runner = unittest.TextTestRunner()
    runner.run(test_group)

if __name__=="__main__":
    main()
