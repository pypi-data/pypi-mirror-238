import platform


def check_os():
    os = platform.system()

    if os == 'Windows':  # Windows
        return 'win'
    elif os == 'Darwin':  # Mac
        return 'mac'
    elif os == 'Linux':  # Linux
        return 'linux'
