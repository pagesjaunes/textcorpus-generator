


def standardization(item:str) -> str:
    #remove(bla bla)
    item = item.replace("\\(.*\\)", "")
    # remove.,; \
    item = item.replace("\\.|,|;|\\\\", "")

    return item;