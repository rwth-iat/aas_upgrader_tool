from basyx2.basyx.aas.examples.data.example_aas import create_full_example as create_full_exampleV2
from aas_upgrader.upgrader import AAS_Classes_Upgrader


objstore_v2 = create_full_exampleV2()
objstore_v3 = AAS_Classes_Upgrader.upgrade_obj_store(objstore_v2)

a = [i for i in objstore_v3]
print(a)

