import pandas as pd

def from_dta(fn,convert_categoricals=True,encoding=None):
    """
    Read stata dta file, creating a pandas dataframe.

    If encoding is not None, interpret as unicode encoding
    of strings for categoricals.

    For example, older files written by francophones may be in ISO-8895-1
    rather than utf-8 (the modern standard).
    """
    def to_utf8(s,encoding,errors='ignore'):
        return bytes(s,encoding=encoding).decode('utf-8',errors='ignore')

    sr=pd.io.stata.StataReader(fn)

    df = sr.read(convert_categoricals=False)

    values = sr.value_labels()

    try:
        var_to_label = dict(zip(sr.varlist,sr.lbllist))
        varlist = sr.varlist
    except AttributeError: # Newer versions of StataReader don't expose varlist
        var_to_label = dict(zip(sr._varlist,sr._lbllist))
        varlist = sr._varlist

    if convert_categoricals:
        for var in varlist: # Check mapping for each variable with values
            if len(var_to_label[var]):
                try:
                    code2label = values[var_to_label[var]]
                    if encoding is not None: # Change encoding of values to utf-8
                        code2label = {k:to_utf8(v,encoding=encoding) for k,v in code2label.items()}
                    df[var] = df[var].replace(code2label)
                except KeyError:
                    print('Issue with categorical mapping: %s' % var)

    return df
