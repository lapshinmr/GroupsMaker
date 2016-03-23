

def bind_scroll_canv(canv, direct='Y'):
    if direct == 'X' or direct == 'x':
        canv.bind_all('<4>', lambda event: canv.xview('scroll', -1, 'units'))
        canv.bind_all('<5>', lambda event: canv.xview('scroll', 1, 'units'))
    elif direct == 'Y' or direct == 'y':
        canv.bind_all('<4>', lambda event: canv.yview('scroll', -1, 'units'))
        canv.bind_all('<5>', lambda event: canv.yview('scroll', 1, 'units'))


def unbind_scroll_canv(canv):
    canv.unbind_all('<4>')
    canv.unbind_all('<5>')


