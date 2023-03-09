from checker.units.controller import Controller


class Converter(Controller):
    def __init__(self, data: str):
        super().__init__(data)
        self.output = super().__call__()

    def get_text_description(self):
        if isinstance(self.output, dict):
            return "{0}\t|\t{1}\t|\t{2}\t|\t{3}\t|\t???\t".format(
                *self.output.values()
            )
        elif isinstance(self.output, list):
            result = ""
            for output in self.output:
                result += "{0}\t|\t{1}\t|\t{2}\t|\t0.0\t|\t{3:.3} ms\t|\t{4}\t|\t{5}\n".format(
                    *output.values()
                )
            if result[-1:] == "\n":
                return result[:-1]
            return result
        return self.output

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.data)
