class Question(object):
    def __init__(self, year, num, q, options, key, domain, citations, rationale):
        self.year = year # exam year
        self.num = num
        self.q = q
        self.options = options
        self.key = key
        self.domain = domain
        self.rationale = rationale
        self.citations = citations

    def __str__(self):
        ans = 'Question: year=%s  num=%s  question %s\nlen(options) %s\n' % (self.year, self.num, self.q, len(self.options))
        for o in self.options:
            ans += o[0]
        try:
            ans += 'key %s\ndomain %s\ncitations %s\nrationale %s\n' % (self.key, self.domain, self.citations, self.rationale)
        except AttributeError:
            # truncated Question objects do not have key, domain, citations or rationale
            pass
        return ans


    def __repr__(self):
        return self.__str__()
