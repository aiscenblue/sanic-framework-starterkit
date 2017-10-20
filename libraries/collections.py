# TODO :: collections library for element filtering


class Collections:

    D = {'key1': {'key2': {'key3': 'value3', 'key4': 'value4', 'key7': {'key8': 'value8'}}, 'key5': 'value5'}, 'key6': 'value6'}

    def multipart_key(self, d):
        dd = {}
        for k in d:
            if isinstance(d[k], dict):
                inner = self.multipart_key(d[k])
                for kk in inner:
                    dd[k+chr(124)+kk] = inner[kk]
            else:
                dd[k] = d[k]
        return dd

    def exclude(self, lists_to_be_excluded):
        key_list = ['key3', 'key7']

        DD = self.multipart_key(lists_to_be_excluded)
        newDD = DD.copy()

        for k in DD:
            for kk in k.split(chr(124)):
                if kk in key_list:
                    del newDD[k]
                    break

# print(DD)
# {'key1|key2|key3': 'value3', 'key1|key5': 'value5', 'key6': 'value6', 'key1|key2|key7|key8': 'value8', 'key1|key2|key4': 'value4'}

# print(newDD)
# {'key1|key5': 'value5', 'key6': 'value6', 'key1|key2|key4': 'value4'}