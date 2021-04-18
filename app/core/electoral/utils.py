
def calculate_age(born):
    from datetime import date
    today = date.today()
    #((today.month, today.day) < (born.month, born.day)) That can be done much simpler 
    # considering that int(True) is 1 and int(False) is 0:
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))