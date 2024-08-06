import json 
import sys
from collections import OrderedDict

TERMINATORS = 'jmp', 'br', 'ret'

def form_blocks(body):
    cur_block = []

    for instr in body:
        if 'op' in instr:
            cur_block.append(instr)
    
            #check for terminators - break happens here
            if instr['op'] in TERMINATORS:  
                yield cur_block
                cur_block = []

            #checks for actual labels in json
        else:
            yield cur_block
 
            cur_block = [instr]
    yield cur_block

def block_map(blocks):
    out = OrderedDict()
    for block in blocks:
        if 'label' in block[0]:          
            name = block[0]['label']   
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))
        out[name] = block
    return out

def get_cfg(name2block):
    """Given a name-to-block map, this function wil produce a 
    mapping from the block name to its successor"""
    out = {}
    for i, (name, block) in enumerate(name2block.items()):
        last = block[-1]
        if last['op'] in ('jmp', 'br'):
            succ = last['labels']
        elif last['op'] == 'ret':
            succ = []   
        else:
            if i == len(name2block) - 1:
                succ = []
            else:
                succ = [list(name2block.keys())[i + 1]]
        out[name] = succ
    return out

def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name2block = block_map(form_blocks(func['instrs'])) 
        #form_block generates basic blocks based on terminators
        #block_map creates a map of block name and instructions associated with a given block
        #finally get_cfg is responsible for giving structure to the OrderedDict giving the CFG.
        for name, block in name2block.items():
            print(name)
            print(' ', block)
        cfg = get_cfg(name2block)
        print(cfg)

if __name__ == '__main__':
    mycfg()

