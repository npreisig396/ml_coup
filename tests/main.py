import pkgutil
import importlib
import tests.tests


def main():
    tests = load_tests()
    t = sum(runTest(i,tests[i]) for i in range(len(tests)))
    if t == len(tests):
        print('All Tests Passed')
    

def runTest(i,test):
    r = test.run()
    if r:
        return 1
    else:
        print(f'Test {i+1} failed')
        return 0

def load_tests():
    modules = []
    package = tests.tests
    for _, name, ispkg in pkgutil.iter_modules(package.__path__):
        if name.startswith("test"):
            module = importlib.import_module(f"{package.__name__}.{name}")
            modules.append(module)
    return modules


if __name__ == '__main__':
    main()
