from storage_planning.py3dbp import Packer, Bin, Item, Painter
from .utils import fast_convert

DEBUG = False

class NotPackedError(Exception):
    
    def __init__(self, message):
        super().__init__(message)
        
def calculate(
    crate_list: list,
    cell_size: list,
    cell_weight: float,
    surface_ratio: float = 0.1 ,
    show_volume_left: bool = False
):

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
            loadbear=crate.get('loadbear', 1e10),
            updown=True,
            color='red'
        )
        packer.addItem(item)
        packer_item = packer.items[idx]
        match packer_item.rotation_type:
            case 1: 
                packer.items[idx].rotation_type = 0
                temp = packer.items[idx].width
                packer.items[idx].width = packer.items[idx].height
                packer.items[idx].height = temp
                break
            case 2: 
                packer.items[idx].rotation_type = 0
                temp = packer.items[idx].width
                packer.items[idx].width = packer.items[idx].height
                packer.items[idx].height = packer.items[idx].depth
                packer.items[idx].depth = temp
                break
            case 3: 
                packer.items[idx].rotation_type = 0
                temp = packer.items[idx].width
                packer.items[idx].width = packer.items[idx].depth
                packer.items[idx].depth = temp
                break
            case 4: 
                packer.items[idx].rotation_type = 0
                temp = packer.items[idx].width
                packer.items[idx].width = packer.items[idx].depth
                packer.items[idx].depth = packer.items[idx].height
                packer.items[idx].height = temp
                break
            case 5: 
                packer.items[idx].rotation_type = 0
                temp = packer.items[idx].height
                packer.items[idx].height = packer.items[idx].depth
                packer.items[idx].depth = temp
                break
            case _: continue

    packer.pack(
        bigger_first=True,
        distribute_items=True,
        support_surface_ratio=surface_ratio,
    )
    
    packer.putOrder()
    
    res = []
    
    # print(*map(lambda i: i.name, packer.bins[0].items))
    
    for item in packer.bins[0].items:
        
        # print(item.name, item.position, item.rotation_type, cell_size, '\n')
        
        match item.rotation_type:
            case 1: 
                item.rotation_type = 0
                temp = item.width
                item.width = item.height
                item.height = temp
            case 2: 
                item.rotation_type = 0
                temp = item.width
                item.width = item.height
                item.height = item.depth
                item.depth = temp
            case 3: 
                item.rotation_type = 0
                temp = item.width
                item.width = item.depth
                item.depth = temp
            case 4: 
                item.rotation_type = 0
                temp = item.width
                item.width = item.depth
                item.depth = item.height
                item.height = temp
            case 5: 
                item.rotation_type = 0
                temp = item.height
                item.height = item.depth
                item.depth = temp
            case _:
                pass
            
        # print(item.name, item.position, item.rotation_type, cell_size)
        # print('\n\n\n\n')
        
        res.append(
            {
                'position': {
                    'x': float(item.position[0] + item.width / 2),
                    'y': float(item.position[1] + item.height / 2), 
                    'z': float(item.position[2] + item.depth / 2),
                    'rot': item.rotation_type
                },
                'width': float(item.width),
                'height': float(item.height),
                'depth': float(item.depth),
                'img': fast_convert(item.name, bg_color='#ad8762')
            }
        )
    # print(len(res), len(crate_list), sep='*******')
    if not DEBUG:
        if len(res) == len(crate_list) and not show_volume_left:
            return res
        elif len(res) == len(crate_list) and show_volume_left:
            volume_t = 0
            for item in packer.bins[0].items:
                volume_t += item.getVolume()
            return [float(packer.bins[0].getVolume() - volume_t), len(res)]
        else:
            raise NotPackedError('Не удалось разместить коробки')

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
    fig.savefig()

def handle_calculations(cell, crates, show_volume_left: bool = False):
    
    sorting_crate_list = [
        {
            'text_id': crate.text_id,
            'size': [*map(float, crate.size.split('x'))],
            'weight': crate.amount if crate.nomenclature.units == 'кг' else crate.amount * crate.nomenclature.mass
        }
        for crate in crates
    ]
    # cell_size = [*map(float, cell.cell_size.split('x'))]

    if show_volume_left:
        try:
            return calculate(
                crate_list=sorting_crate_list,
                cell_size=(
                        cell.x_cell_size,
                        cell.y_cell_size,
                        cell.z_cell_size,    
                ),
                cell_weight=cell.mass,
                show_volume_left=True
            )
        except (ZeroDivisionError, NotPackedError):
            return None
        
    try:
        return {
            'status': True,
            'listBoxes': calculate(
                crate_list=sorting_crate_list,
                cell_size=(
                    cell.x_cell_size,
                    cell.y_cell_size,
                    cell.z_cell_size,    
                ),
                cell_weight=cell.mass
            ),
            'bin': {
                'id': cell.adress,
                'width': cell.x_cell_size,
                'height': cell.y_cell_size,
                'depth': cell.z_cell_size,
                # 'x_cell_coord'
            },
        }
    except (ZeroDivisionError, NotPackedError):
        return None