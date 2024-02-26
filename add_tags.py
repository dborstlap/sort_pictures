
import pythoncom
from win32com.propsys import propsys
from win32com.shell import shellcon

# get PROPERTYKEY for "System.Keywords"
pk = propsys.PSGetPropertyKeyFromName("System.Keywords")

path = "T:\Pictures\project mama\\finished\\2006\\5\DSC02142.JPG"

# get property store for a given shell item (here a file)
ps = propsys.SHGetPropertyStoreFromParsingName(path, None, shellcon.GPS_READWRITE, propsys.IID_IPropertyStore)

# read & print existing (or not) property value, System.Keywords type is an array of string
keywords = ps.GetValue(pk).GetValue()
print(keywords)

# build an array of string type PROPVARIANT
previous_tags = keywords
new_tags = ["Vokke met 2 ks", "nogwatomtetesten"]
all_tags = previous_tags + new_tags
newValue = propsys.PROPVARIANTType(all_tags, pythoncom.VT_VECTOR | pythoncom.VT_BSTR)

# write property
ps.SetValue(pk, newValue)
ps.Commit()

ps = None
ps = propsys.SHGetPropertyStoreFromParsingName(path, None, shellcon.GPS_READWRITE, propsys.IID_IPropertyStore)
keywords = ps.GetValue(pk).GetValue()
print('2nd time', keywords)













