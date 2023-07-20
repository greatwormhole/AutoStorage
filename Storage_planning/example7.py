from py3dbp import Packer, Bin, Item, Painter
import time
from random import randint
start = time.time()

'''

If you have multiple boxes, you can change distribute_items to achieve different packaging purposes.
1. distribute_items=True , put the items into the box in order, if the box is full, the remaining items will continue to be loaded into the next box until all the boxes are full  or all the items are packed.
2. distribute_items=False, compare the packaging of all boxes, that is to say, each box packs all items, not the remaining items.

'''

# init packing function
packer = Packer()
#  init bin 
box = Bin('example7-Bin1', (1000, 1000, 1000), 100,0,0)
# box2 = Bin('example7-Bin2', (3, 3, 5), 100,0,0)
#  add item
# Item('item partno', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
packer.addBin(box)
# packer.addBin(box2)

data = [{
    'partno': f'Box-{i}',
    'name': f'Crate{i}',
    'typeof': 'cube',
    'WHD': (randint(100, 400),randint(100, 400),randint(100, 400)),
    'weight': 1,
    'level': 1,
    'loadbear': 1,
    'updown': True,
    'color': 'red'
    } for i in range(1, 31)]

for i in range(len(data)):
    packer.addItem(Item(**data[i]))

# calculate packing 
packer.pack(
    bigger_first=True,
    # Change distribute_items=False to compare the packing situation in multiple boxes of different capacities.
    # distribute_items=False,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=1,
    number_of_decimals=0
)

# put order
packer.putOrder()

# print result
print("***************************************************")
for idx,b in enumerate(packer.bins) :
    print("**", b.string(), "**")
    print("***************************************************")
    print("FITTED ITEMS:")
    print("***************************************************")
    volume = b.width * b.height * b.depth
    volume_t = 0
    volume_f = 0
    unfitted_name = ''
    for item in b.items:
        print("partno : ",item.partno)
        print("color : ",item.color)
        print("position : ",item.position)
        print("rotation type : ",item.rotation_type)
        print("W*H*D : ",str(item.width) +' * '+ str(item.height) +' * '+ str(item.depth))
        print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("weight : ",float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        print("***************************************************")
    
    print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
    print('residual volumn : ', float(volume) - volume_t )
    print("gravity distribution : ",b.gravity)
    print("***************************************************")
    # draw results
    painter = Painter(b)
    fig = painter.plotBoxAndItems(
        title=b.partno,
        alpha=0.8,
        write_num=False,
        fontsize=10
    )

print("***************************************************")
print("UNFITTED ITEMS:")
for item in packer.unfit_items:
    print("***************************************************")
    print('name : ',item.name)
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("W*H*D : ",str(item.width) +' * '+ str(item.height) +' * '+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.depth)
    unfitted_name += '{},'.format(item.partno)
    print("***************************************************")
print("***************************************************")
print('unpack item : ',unfitted_name)
print('unpack item volumn : ',volume_f)

stop = time.time()
print('used time : ',stop - start)

fig.show()