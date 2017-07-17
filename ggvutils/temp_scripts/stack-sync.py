# stack-sync.py
import json
from slidestacks.models import SlideStack

json_file = '/home/ubuntu/mismatched-stacks.txt'
f = open(json_file)
stack_fixes = json.loads(f.read())
f.close()

#  update the asset string in each slidestack according stack_fixes data.

for i in stack_fixes:
    stack = SlideStack.objects.get(pk=i[0])
    print stack.asset, '==>',
    stack.asset = i[2]
    print stack.asset
    stack.save()




# stacks_prod = SlideStack.objects.all().order_by('asset')
# stack_list = []
# null_stacks = []

# for i in stacks_prod:
#     try:
#         pos = stack3.index(i.asset)
#         stack_list.append([i.id, i.asset, True])
#     except:
#         stack_list.append([i.id, i.asset, False])
#         null_stacks.append(i.asset)

# for i in stack_fix: print i