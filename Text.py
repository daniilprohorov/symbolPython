import re


def const_or_symbol(val, process):
    match = re.match('[-+]?[\d]+', val)
    index = process.index_gen()
    if match:
        process.const(index, int(val))
    else:
        process.symbol(index, val)
    return index


def text_to_index(text_list, local_dict, process):
    out = []
    for text in text_list:
        if len(text) == 1:
            block = text[0]
            if block in local_dict:
                out.append(local_dict[block])
            elif block in process.context:
                out.append(block)
            else:
                index = const_or_symbol(block, process)
                out.append(index)
        elif type(text) is str:
            block = text
            if block in local_dict:
                out.append(local_dict[block])
            elif block in process.context:
                out.append(block)
            else:
                index = const_or_symbol(block, process)
                out.append(index)
        else:
            index = process.index_gen()
            func_name = text[0]
            args_indexes = [text_to_index([block], local_dict, process)[0] for block in text[1:]]
            process.func(index, func_name, args_indexes)
            out.append(index)
    return out
