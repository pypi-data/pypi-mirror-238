"""Main module."""
from astropy.io import fits, ascii
from pkg_resources import resource_filename
import numpy as np
from astropy.table import Table


dqdatPath = resource_filename('explaintheDQ','jwst_dq_table.csv')
dqdat = ascii.read(dqdatPath)

def DQtab(dqValue):
    t = Table()
    dq_flags = []
    for oneInd in np.arange(len(dqdat)):
        dq_is_true = (dqValue & 2**dqdat['Bit'][oneInd]) > 0
        dq_flags.append(dq_is_true)
    t['Name'] = dqdat['Name']
    t['Flag'] = dq_flags
    t['Bit'] = dqdat['Bit']
    t['Description'] = dqdat['Description']
    
    outData = Table.pprint(t,max_lines=100)
    return outData
    