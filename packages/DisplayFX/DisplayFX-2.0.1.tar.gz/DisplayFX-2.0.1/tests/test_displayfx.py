from beetools import msg as beemsg

from displayfx.displayfx import DisplayFx


def basic_test():
    '''Basic and mandatory scenario tests for certification of the class'''
    success = True
    bar_len_list = [10, 30, 50, 100]
    # bar_len_list = [ 100 ]
    max_val_list = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 50000]
    # max_val_list = [ 0 ]
    max_bar_len_list_len = len(str(max(bar_len_list)))
    max_vax_val_list_len = len(str(max(max_val_list)))
    for bar_len in bar_len_list:
        for max_val in max_val_list:
            subject = beemsg.display(
                'Bar {: >{x}}, Max {: >{y}}'.format(bar_len, max_val, x=max_bar_len_list_len, y=max_vax_val_list_len),
                p_len=23,
            )
            t_displayfx = DisplayFx(max_val, p_msg=subject, p_bar_len=bar_len)
            for x in range(0, max_val):
                t_displayfx.update(x)
    return success
