class TerraformBlock:
    def __init__(self, data):
        self.Resource_type
        self.Resource
        self.Resource_name
        self._config
        self.id

    def get_attr(self, array):
        return [self._config[a] if isinstance(self._config, dict) and a in self._config else None for a in array]

    def config_str(self):
        return  " ".join(self.extract_strings(self._config)) 
                            
    def extract_strings(self, obj):
        if isinstance(obj, dict):
            return [str(value) for value in obj.values() for value in self.extract_strings(value)]
        elif isinstance(obj, list):
            return [str(item) for value in obj for item in self.extract_strings(value)]
        else:
            return [str(obj)]
        
    def depends_on_incl_vars(self, ids):
        return [i for i in ids if i in self.config_str()]
    
    def depends_on(self, ids):
        return [i for i in ids if i in self.config_str() and not i.startswith("var.")]

class Module(TerraformBlock):
    def __init__(self, data):
        self.Resource_type = "Module"
        self.Resource = "n/a"
        self.Resource_name = list(data)[0]
        self._config = data[self.Resource_name]
        self.id = f"module.{self.Resource_name}"

class Resource(TerraformBlock):
    def __init__(self, data):
        self.Resource_type = "Resource"
        self.Resource = list(data)[0]
        self.Resource_name = list(data[self.Resource])[0]
        self._config = data[self.Resource]
        self.id = f"{self.Resource}.{self.Resource_name}"

class Data(TerraformBlock):
    def __init__(self, data):
        self.Resource_type = "Data"
        self.Resource = list(data)[0]
        self.Resource_name = list(data[self.Resource])[0]
        self._config = data[self.Resource]
        self.id = f"{self.Resource}.{self.Resource_name}"

class Variable(TerraformBlock):
    def __init__(self, data):
        self.Resource_type = "Variable"
        self.Resource = "n/a"
        self.Resource_name = list(data)[0]
        self._config = data[self.Resource_name]
        self.id = f"var.{self.Resource_name}"