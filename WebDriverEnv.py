import platform

# Determine the correct platform for the webdriver
def get_webdriver_path():
    system = platform.system()
    arch, _ = platform.architecture()
    if system == 'Linux':
        if arch == '64bit':
            webdriver = 'webdrivers/linux/chromedriver'
        else:
            raise Exception("Unsupported arch")
    if system == 'Windows':
        webdriver = 'webdrivers/win/chromedriver.exe'
    if system == 'Darwin':
        webdriver = 'webdrivers/mac/chromedriver'
    return webdriver