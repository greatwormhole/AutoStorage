from decimal import Decimal

from storage_planning.py3dbp import Packer, Bin, Item, Painter
from main.models import DEFAULT_CRATE_MASS

def cast_sizes(width: Decimal, height: Decimal, depth: Decimal, pos_arr: list):
    return [
        pos_arr[0] + width / 2,
        pos_arr[1] + height / 2,
        pos_arr[2] + depth / 2,
    ]

def calculate(crate_list: list, cell_size: list, cell_weight: float, surface_ratio: float = 0.9):

    # print(crate_list)
    # print(cell_size)
    # print(cell_weight)

    packer = Packer()

    cell = Bin(
        partno='Cell',
        WHD=cell_size,
        max_weight=cell_weight,
    )
    packer.addBin(cell)

    for idx, crate in enumerate(crate_list):
        item = Item(
            partno='Rectangle#' + crate.get('text_id', 'MissingId'),
            name='Crate#' + crate.get('text_id', 'MissingId'),
            typeof='cube',
            WHD=crate.get('size'),
            weight=crate.get('weight'),
            level=crate.get('priority', 1),
            loadbear=crate.get('loadbear', 100),
            updown=True,
            color='red'
        )
        packer.addItem(item)
        packer_item = packer.items[idx]
        match packer_item.rotation_type:
            case 1: 
                packer_item.rotation_type = 0
                temp = packer_item.width
                packer_item.width = packer_item.height
                packer_item.height = temp
            case 2: 
                packer_item.rotation_type = 0
                temp = packer_item.width
                packer_item.width = packer_item.height
                packer_item.height = packer_item.depth
                packer_item.depth = temp
            case 3: 
                packer_item.rotation_type = 0
                temp = packer_item.width
                packer_item.width = packer_item.depth
                packer_item.depth = temp
            case 4: 
                packer_item.rotation_type = 0
                temp = packer_item.width
                packer_item.width = packer_item.depth
                packer_item.depth = packer_item.height
                packer_item.height = temp
            case 5: 
                packer_item.rotation_type = 0
                temp = packer_item.height
                packer_item.height = packer_item.depth
                packer_item.depth = temp
            case _: continue

    packer.pack(
        distribute_items=False,
        support_surface_ratio=surface_ratio,
    )

    packer.putOrder()

    return [
        {
            'name': item.name,
            'position': cast_sizes(
                width=item.width,
                height=item.height,
                depth=item.depth,
                pos_arr=[*map(Decimal, item.position)]),
            'size': [
                Decimal(item.width),
                Decimal(item.height),
                Decimal(item.depth),
            ],
        }
        for item in packer.bins[0].items
    ] if packer.unfit_items is not None else None

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
            alpha=0.2,
            write_num=True,
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

    fig.show()

def handle_calculations(cell, crates):

    sorting_crate_list = [
        {
            'text_id': crate.text_id,
            'size': [*map(float, crate.size.split('x'))],
            'weight': crate.amount if crate.nomenclature.units == 'кг' else DEFAULT_CRATE_MASS

        }
        for crate in crates
    ]
    cell_size = [*map(float, cell.cell_size.split('x'))]

    try:
        return {
            'geometry': calculate(
                crate_list=sorting_crate_list,
                cell_size=cell_size,
                cell_weight=cell.mass
            ),
            'cell_id': cell.adress
        }
    except ZeroDivisionError:
        return None