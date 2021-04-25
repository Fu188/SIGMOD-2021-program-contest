import pandas as pd
import re

brand_list = ["intenso", "pny", "lexar", "sony", "sandisk", "kingston", "samsung", "toshiba", "transcend"]

intenso_type = ["basic", "rainbow", "high speed", "speed", "premium", "alu", "business", "micro",
                "imobile", "cmobile", "mini", "ultra", "slim", "flash", "mobile"]

colors = ['midnight black', 'prism white', 'prism black', 'red', 'black', 'blue', 'white', 'silver', 'gold']


def clean_x4(Xdata):
    names = Xdata.filter(items=['name'], axis=1).fillna('')
    prices = Xdata.filter(items=['price'], axis=1).fillna('')
    sizes = Xdata.filter(items=['size'], axis=1).fillna('')
    brands = Xdata.filter(items=['brand'], axis=1).fillna('')
    instance_ids = Xdata.filter(items=['instance_id'], axis=1)
    names = names.values.tolist()
    prices = prices.values.tolist()
    sizes = sizes.values.tolist()
    brands = brands.values.tolist()
    instance_ids = instance_ids.values.tolist()

    result = []

    for row in range(len(instance_ids)):
        nameinfo = names[row][0].lower()

        size = '0'
        price = '0'
        mem_type = '0'
        brand = '0'
        type = '0'
        model = '0'
        item_code = '0'

        if sizes[row][0] != '':
            size = sizes[row][0].lower().replace(' ', '')
        else:
            size_model = re.search(r'[0-9]{1,4}[ ]*[gt][bo]', nameinfo)
            if size_model is not None:
                size = size_model.group()[:].lower().replace(' ', '')

        if prices[row][0] != '':
            price = prices[row][0]

        if brands[row][0] != '':
            brand = brands[row][0].lower()
        else:
            for b in brands:
                if b in nameinfo:
                    brand = b
                    break

        mem_model = re.search(r'ssd', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'micro[- ]?sd[hx]?c?', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'sd[hx]c', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'usb', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'sd(?!cz)', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'secure digital', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'xqd', nameinfo)
        if mem_model is None:
            mem_model = re.search(r'ljd', nameinfo)
        if mem_model is not None:
            mem_type = mem_model.group()
            if mem_type not in ('ssd', 'usb', 'xqd'):
                if 'micro' in mem_type:
                    mem_type = 'microsd'
                elif 'ljd' in mem_type:
                    mem_type = 'usb'
                else:
                    mem_type = 'sd'

        item_code_model = re.search(r'\((mk)?[0-9]{6,10}\)', nameinfo)
        if item_code_model is not None:
            item_code = item_code_model.group()[1:-1]

        if brand == "intenso":
            model_model = re.search(r'[0-9]{7}', nameinfo)
            if model_model is not None:
                model = model_model.group()[:]

            type_model = re.search(r'(high\s)?[a-z]+\s(?=line)', nameinfo)
            if type_model is not None:
                type = type_model.group()[:].replace(' ', '')
            else:
                for t in intenso_type:
                    if t in nameinfo:
                        type = t.replace(' ', '')
                        break

        elif brand == "lexar":
            type_model = re.search(r'((jd)|[\s])[a-wy-z][0-9]{2}[a-z]?', nameinfo)
            if type_model is None:
                type_model = re.search(r'[\s][0-9]+x(?![a-z0-9])', nameinfo)
            if type_model is None:
                type_model = re.search(r'(([\s][x])|(beu))[0-9]+', nameinfo)
            if type_model is not None:
                type = type_model.group().strip() \
                    .replace('x', '').replace('l', '').replace('j', '').replace('d', '') \
                    .replace('b', '').replace('e', '').replace('u', '')

            if mem_type == '0':
                if 'drive' in nameinfo:
                    mem_type = 'usb'

        # judge type and model

        elif brand == 'sony':
            if mem_type == '0':
                if ('ux' in nameinfo) or ('uy' in nameinfo) or ('sr' in nameinfo):
                    mem_type = 'microsd'
                elif ('uf' in nameinfo):
                    mem_type = 'sd'
                elif ('usm' in nameinfo):
                    mem_type = 'usb'

            type_model = re.search(r'((sf)|(usm))[-]?[0-9a-z]{1,6}', nameinfo)
            if type_model is not None:
                type = type_model.group().replace('-', '').replace('g', '')
                for c in range(ord('0'), ord('9')):
                    type = type.replace(chr(c), '')
        # 1024: 1 TB
        # 256: ssd
        # 128: usmqx usb
        # 128: microsd
        # 64: usb
        # 32: usmqx
        # 32: sd | microsd
        # 32: usmr & usb | usb
        # 16: sd
        # 16: usb
        # 8: sd
        # 8: microsd
        # 8: usmqx usb
        # 4: usmr
        # 4: usmmp | usb

        elif brand == 'sandisk':
            model_model = re.search(r'ext.*(\s)?((plus)|(pro)|\+)', nameinfo)
            if model_model is not None:
                model = 'ext+'
            else:
                model_model = re.search(r'ext(reme)?', nameinfo)
                if model_model is not None:
                    model = 'ext'
                else:
                    model_model = re.search(r'fit', nameinfo)
                    if model_model is None:
                        model_model = re.search(r'glide', nameinfo)
                    if model_model is None:
                        model_model = re.search(r'blade', nameinfo)
                    if model_model is not None:
                        model = model_model.group()
                    else:
                        model_model = re.search(r'ultra(\s)?((plus)|(pro)|\+|(performance)|(android))', nameinfo)
                        if model_model is None:
                            model_model = re.search(r'sandisk 8gb ultra sdhc memory card, class 10, read speed up to 80 mb/s \+ sd adapter', nameinfo)
                        if model_model is None:
                            model_model = re.search(r'sandisk sdhc [0-9]+gb 80mb/s cl10\\n', nameinfo)
                        if model_model is not None:
                            model = 'ultra+'
                        else:
                            model_model = re.search(r'ultra', nameinfo)
                            if model_model is not None:
                                model = 'ultra'
                            else:
                                model_model = re.search(r'dual', nameinfo)
                                if model_model is None:
                                    model_model = re.search(r'double connect.*', nameinfo)
                                if model_model is not None:
                                    model = 'ultra'

            if 'accessoires montres' in nameinfo:
                if 'extreme' in nameinfo:
                    mem_type = 'microsd'
                    model = 'ultra+'
                elif 'ext pro' in nameinfo:
                    mem_type = 'microsd'
                    model = 'ext+'
            if 'adapter' in nameinfo or 'adaptateur' in nameinfo:
                mem_type = 'microsd'
            if mem_type == '0':
                if 'drive' in nameinfo:
                    mem_type = 'usb'
                elif 'cruzer' in nameinfo:
                    mem_type = 'usb'
                elif model in ('glide','fit'):
                    mem_type = 'usb'

        elif brand == 'pny':
            type_model = re.search(r'att.*?[3-4]', nameinfo)
            if type_model is not None:
                type = type_model.group().replace(' ', '').replace('-', '')
                type = 'att' + list(filter(lambda ch: ch in '0123456789', type))[0]
                if mem_type == '0':
                    mem_type = 'usb'


        elif brand == 'kingston':
            if mem_type == '0':
                if ('savage' in nameinfo) or ('hx' in nameinfo) or ('hyperx' in nameinfo):
                    mem_type = 'usb'
                elif ('ultimate' in nameinfo):
                    mem_type = 'sd'
            model_model = re.search(r'(dt[i1]0?1?)|(data[ ]?traveler)', nameinfo)
            if model_model is not None:
                model = 'data traveler'
                type_model = re.search(r'(g[24])|(gen[ ]?[24])', nameinfo)
                if type_model is not None:
                    type = type_model.group()[-1:]
        # 512, 256, 128: judge by memtype
        # 64: g2, g4
        # 32: g2
        # 16: microsd, sd, usb ????
        # 8: microsd, usb

        elif brand == 'samsung':
            if 'lte' in nameinfo:
                model_model = re.search(r'[\s][a-z][0-9]{1,2}[a-z]?[\s]', nameinfo)
                if model_model is None:
                    model_model = re.search(r'[\s]note[\s]?[0-9]{1,2}\+?[\s]?(ultra)?', nameinfo)
                if model_model is None:
                    model_model = re.search(r'prime[ ]?((plus)|\+)', nameinfo)
                if model_model is None:
                    model_model = re.search(r'prime', nameinfo)
                if model_model is not None:
                    model = model_model.group().replace(' ', '').replace('plus', '+')
            elif 'tv' in nameinfo:
                model_model = re.search(r'[0-9]{1,2}-inch', nameinfo)
                if model_model is not None:
                    model = model_model.group().strip()
            for c in colors:
                if c in nameinfo:
                    type = c
                    break
        # LTE: color(type), gb, model
        # TV: color(type), inch(model)
        # others: gb

        elif brand == 'toshiba':
            model_model = re.search(r'[\s\-n][umn][0-9]{3}', nameinfo)
            if model_model is not None:
                model = model_model.group()[1:]
                if mem_type == '0':
                    ch = model[0]
                    if ch == 'u':
                        mem_type = 'usb'
                    elif ch == 'n':
                        mem_type = 'sd'
                    elif ch == 'm':
                        mem_type = 'microsd'
            if mem_type == 'usb' and model == '0':
                model_model = re.search(r'ex[\s-]?ii', nameinfo)
                if model_model is not None:
                    model = model_model.group()[:2]
            if mem_type != 'usb':
                type_model = re.search(r'exceria[ ]?((high)|(plus)|(pro))?', nameinfo)
                if type_model is not None:
                    type = type_model.group().replace(' ', '').replace('exceria', 'x')
                elif size != '0':
                    type_model = re.search(r'x[ ]?((high)|(plus)|(pro))?'+size[:-2], nameinfo)
                    if type_model is not None:
                        type = type_model.group().replace(' ', '')[:-(len(size)-2)]
                if type == 'xpro' and mem_type == '0':
                    mem_type = 'sd'
                if type == 'xhigh' and mem_type == '0':
                    mem_type = 'microsd'
            if 'transmemory' in nameinfo:
                if mem_type == '0':
                    mem_type = 'usb'
            speed_model = re.search(r'[1-9][0-9]{1,2}[\s]?mb\\s', nameinfo)
            if speed_model is not None:
                speed = re.search(r'[0-9]{2,3}', speed_model.group()).group()
                if (speed == '260' or speed == '270') and type == '0':
                    type = 'xpro'


        elif brand == 'transcend':
            pass

        result.append([
            instance_ids[row][0],
            brand,
            size,
            price,
            mem_type,
            type,
            model,
            item_code,
            nameinfo
        ])
    # mp = {}
    # cnt = 0
    # for i in range(len(result)):
    #     if result[i][1] is None:
    #         result[i][1] = 0
    #     else:
    #         if result[i][1] not in mp:
    #             cnt += 1
    #             mp[result[i][1]] = cnt
    #         result[i][1] = mp[result[i][1]]

    result = pd.DataFrame(result)

    name = ['instance_id', 'brand', 'capacity', 'price', 'mem_type', 'type', 'model', 'item_code', 'title']
    for i in range(len(name)):
        result.rename({i: name[i]}, inplace=True, axis=1)

    #
    # for i in range(result.shape[0]):
    #     print(result.iloc[i].values.tolist())
    return result