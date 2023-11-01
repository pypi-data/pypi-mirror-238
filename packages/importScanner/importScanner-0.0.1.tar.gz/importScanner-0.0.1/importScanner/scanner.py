class Libraries:
    def __init__(self, libName : list) -> None:
        self.lib = list(libName)
    
    def checkImport(self, filePath : str = None):
        if filePath == None:
            raise ValueError("the 'filePath' Parameter cannot be empty")
        else:
            try:
                data = open(file=filePath, mode='r').read()
                for libs in self.lib:
                    if libs in data:
                        print(f"{libs} : True")
                    else:print(f"{libs} : False")
            except Exception as error:
                print(error)
