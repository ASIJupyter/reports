import SentinelUtils
import dateutil

class read(object):
    result = SentinelUtils.ConfigReader.read_config_values("C:\\Users\\zhzhao\\source\\repos\\PythonSDK\\PythonSDK\\json_parser\\asi_config.json")
    print(result)

class check(object):
    check = SentinelUtils.version_management.ModuleVersionCheck()
    result = check.validate_python('3.6.0')
    print(result)
    result = check.validate_installed_modules(['Kqlmagic>=0.1.92', 'pip>=9.0.2'])

    print(result[1].requirement_met)
    print(result[1].name)
