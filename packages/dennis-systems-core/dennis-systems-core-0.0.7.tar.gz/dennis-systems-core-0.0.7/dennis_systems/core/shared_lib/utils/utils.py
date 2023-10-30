class file_utils:
    @staticmethod
    def read_from_file(path):
        file = open(path, "r")
        content = file.read()
        file.close()
        return content
