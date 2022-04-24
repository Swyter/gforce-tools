import string

# swy: pretty ugly, but does the trick
filename = "./make_auto_text_hashcodes_msc_text_db_english_hashcode_oneliner_src.txt"

with open(f"{filename}", "r",encoding='utf8') as f:
    b=f.read()

b = b.split("\n")
database  = set()
hashcodes = set()

for line in b:
    elem=line.split("`; `")

    try:
        hc  = int(elem[0].strip("`"), 16)
        txt = elem[1].replace("\\n","\n").strip("`")
    except:
        pass

    # swy: get rid of apostrophes
    txt=txt.replace('\'', '').replace("’", "") #.lower()
    #print(int(elem[0].strip("`"), 16), elem[1].strip("`").replace(" ", "_"))
    rec=''
    in_crap=False

#    if (hc != 0x43002fc7):
#        continue

    # swy: make the first one always uppercase
    txt = txt[:1].upper() + txt[1:]

    # swy: heuristically make some longer words lowercase; at least the ones we know aren't FBI
    txt_delower = []
    for word in txt.split():
        if word.upper() == word and len(word) > 5:
            word = word[:1] + word.lower()[1:]

        txt_delower.append(word)

    txt = " ".join(txt_delower)

    for i, c in enumerate(txt):
        # swy: skip the <TEB 1124091129> dummy thing, the numbers inside seem like text hashcodes (1124091129 = 0x430044f9)
        if not in_crap and c == '<':
            in_crap = True
        elif in_crap and c == '>':
            in_crap = False

        if in_crap:
            continue

        # swy: skip anything not in the A-Z 0-9 range
        if (c.lower() not in string.ascii_lowercase or c in [' ', '.', ',']) and c not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            continue

        # swy: make the first letter of a word uppercase
        #if txt[i-1] in [' ', '.', ','] or i == 0: # or txt[i-1].lower() not in string.ascii_lowercase:
        if txt[i-1].lower() not in string.ascii_lowercase:
            c = c.upper()

        rec += c

    # swy: skip three repeated letters in a row
    recb = ""
    for i, c in enumerate(rec):
        lenn = len(rec)
        if lenn >= (i+3):
            if rec[i+1] == rec[i+2] == c:
                continue
        recb += c

    # swy: ignore duplicated hashcode numbers; we've already done this
    if hc in hashcodes:
        continue

    hashcodes.add(hc)

    # --

    # swy: add a suffix to tags that already exist to make them unique; important
    count = 0
    while recb.lower() in database:
        recb += "_" + chr(ord('A') + count)
        count += 1

    database.add(recb.lower())

    print(hex(hc), f'#define HT_Text_{recb}		  0x{hc:06x}')