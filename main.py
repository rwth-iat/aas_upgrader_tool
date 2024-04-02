from basyx.aas.examples.data.example_aas import create_full_example as create_full_exampleV3
from basyx2.aas.examples.data.example_aas import create_full_example as create_full_exampleV2

import basyx.aas.adapter.json
import basyx2.aas.adapter.json

from aas_upgrader.upgrader import AAS_Classes_Upgrader

objstore_v2 = create_full_exampleV2()

#with open('aasV2.json', 'w', encoding='utf-8') as json_file:
#    basyx2.aas.adapter.json.write_aas_json_file(json_file, objstore_v2)

with open('aasV2.json', 'r', encoding='utf-8') as json_file:
    objstore_v2 = basyx2.aas.adapter.json.read_aas_json_file(json_file)


objstore_v3 = AAS_Classes_Upgrader.upgrade_obj_store(objstore_v2)

with open('aasV3.json', 'w', encoding='utf-8') as json_file:
    basyx.aas.adapter.json.write_aas_json_file(json_file, objstore_v3)


a = [i for i in objstore_v3]
print(a)

