import re

import toml

unicode = str
class KnioTaskEncoder(toml.encoder.TomlEncoder):
  def __init__(self):
    super(KnioTaskEncoder, self).__init__(dict, True)
    self.dump_funcs[str] = self.dump_str

  def dump_sections(self, o, sup):
    retstr = ""
    if sup != "" and sup[-1] != ".":
        sup += '.'
    retdict = self._dict()
    arraystr = ""
    for section in o:
        section = unicode(section)
        qsection = section
        value = o[section]
        if not re.match(r'^[A-Za-z0-9_-]+$', section):
            qsection = self.dump_value(section)
        if not isinstance(value, dict):
            arrayoftables = False
            if isinstance(value, list):
                for a in value:
                    if isinstance(a, dict):
                        arrayoftables = True
            if arrayoftables:
                for a in value:
                    arraytabstr = "\n"
                    arraystr += "[[" + sup + qsection + "]]\n"
                    s, d = self.dump_sections(a, sup + qsection)
                    if s:
                        if s[0] == "[":
                            arraytabstr += s
                        else:
                            arraystr += s
                    while d:
                        newd = self._dict()
                        for dsec in d:
                            s1, d1 = self.dump_sections(d[dsec], sup +
                                                        qsection + "." +
                                                        dsec)
                            if s1:
                                arraytabstr += ("[" + sup + qsection +
                                                "." + dsec + "]\n")
                                arraytabstr += s1
                            for s1 in d1:
                                newd[dsec + "." + s1] = d1[s1]
                        d = newd
                    arraystr += arraytabstr
            else:
                if value is not None:
                    # kniodo edit
                    if section == "body":
                        retstr += '\n' + ('#' * 40) + '\n'
                    retstr += (qsection + " = " +
                               unicode(self.dump_value(value)) + '\n')
                    # kniodo edit
                    if section == "body":
                        retstr += '\n' + ('#' * 79)

        elif self.preserve and isinstance(value, toml.encoder.InlineTableDict):
            retstr += (qsection + " = " +
                       self.dump_inline_table(value))
        else:
            retdict[qsection] = value
    retstr += arraystr
    return (retstr, retdict)

  def dump_str(self, v):
    nl = v.count('\n')
    if nl <= 2:
      return toml.encoder._dump_str(v)
    # raw string with """ replaced
    v = v.replace('"""', r"\u0022\u0022\u0022")
    return '"""\n' + v + '"""\n'


def load(f):
    return toml.load(open(f, encoding='utf8'))

def dump(data, f):
    return toml.dump(data, open(f, 'w', encoding='utf8'), encoder=KnioTaskEncoder())
