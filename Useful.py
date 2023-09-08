

def sec2time(sec):
    min=sec//60
    sec-=min*60
    hour=min//60
    min-=hour*60
    days=hour//24
    hour-=days*24

    if days!=0:
        return "{:.0f} {:.0f}:{:.0f}:{:.2f}".format(days,hour,min,sec)
    elif hour!=0:
        return "{:.0f}:{:.0f}:{:.2f}".format(hour,min,sec)
    elif min!=0:
        return "{:.0f}:{:.2f}".format(min,sec)
    else:
        return "{:.2f}".format(sec)