from cave_utils.api import LogObject

x = LogObject()

x.add(path=["test"], msg="Some test error", level="error")
x.add(path=["test"], msg="Some test warning", level="warning")
x.write_logs(path="./logs/test_log.txt")
x.print_logs()