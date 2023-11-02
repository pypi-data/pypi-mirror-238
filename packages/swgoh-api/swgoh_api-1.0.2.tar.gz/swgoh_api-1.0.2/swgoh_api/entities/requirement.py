class Requirement(object):
    def __init__(self, data):
        self.require = data

    def add_require(self, field, value):
        '''
        Add new requirement if not exists
        '''
        if field not in self.require:
            self.require[field] = value
            return True
        return False

    def set_require(self, field, value):
        '''
        Set value of existing requirement or add new
        '''
        self.require[field] = value
        return True

    def remove_require(self, field):
        '''
        Remove requirement if exists
        '''
        if field in self.require:
            del self.require[field]
            return True
        return False
