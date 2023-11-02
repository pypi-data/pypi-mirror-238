import refractfs

import pkg_resources
packages = pkg_resources.working_set
packages_list = ["%s==%s" % (i.key, i.version) for i in packages]

if 'refractfs==1.0.0' in packages_list:
    print("There is my boy")
else:
    print("Where is my boy??")
# print(packages_list)