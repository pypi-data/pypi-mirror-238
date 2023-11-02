class Helpers(object):
    @staticmethod
    def toml_dict_to_string(dict):
        returned_string = ""
        for key, value in dict.items():
            returned_string = '{}\t{} = "{}"\n'.format(returned_string, key, value)
        return returned_string
