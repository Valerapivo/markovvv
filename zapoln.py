import sys
import os
from collections import defaultdict
import math

def process_file(input_file, max_context=13):
    symbols = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?')
    
    for order in range(1, max_context + 1):
        context_counts = defaultdict(lambda: defaultdict(int))
        
        with open(input_file, 'r', encoding='utf-8', buffering=8192) as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            f.seek(0)
            
            buffer = ''
            context = ''
            
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                buffer += chunk.lower()
                
                i = 0
                while i < len(buffer):
                    ch = buffer[i]
                    if ch in symbols:
                        if len(context) == order:
                            context_counts[context][ch] += 1
                            context = context[1:] + ch
                        else:
                            context += ch
                    else:
                        context = ''
                    i += 1
                
                buffer = buffer[i:]
                
                progress = (f.tell() / file_size) * 100
                print(f"\symbol {order}: {progress:.1f}%", end='')
        
        print(f"\n saving {order} symbol...")
        with open(f"{sys.argv[2]}{order}.csv", 'w', encoding='utf-8') as f:
            f.write('order,context,symbol,probability\n')
            for ctx, char_counts in context_counts.items():
                total = sum(char_counts.values())
                for ch, count in char_counts.items():
                    f.write(f'{order},"{ctx}","{ch}",{count/total:.10f}\n')
        
        context_counts.clear()

def process_general(input_file):
    symbols = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?')
    char_counts = defaultdict(int)
    
    with open(input_file, 'r', encoding='utf-8', buffering=8192) as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0)
        
        buffer = ''
        total_chars = 0
        
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            buffer += chunk.lower()
            
            i = 0
            while i < len(buffer):
                ch = buffer[i]
                if ch in symbols:
                    char_counts[ch] += 1
                    total_chars += 1
                i += 1
            
            buffer = buffer[i:]
            
            progress = (f.tell() / file_size) * 100
            print(f"\ symbol 0: {progress:.1f}%", end='')
    
    print("\saving 0 symbol...")
    with open(f"{sys.argv[2]}0.csv", 'w', encoding='utf-8') as f:
        f.write('order,context,symbol,probability\n')
        for ch, count in char_counts.items():
            f.write(f'0,"","{ch}",{count/total_chars:.10f}\n')

def main():
    if len(sys.argv) != 3:
        print(f"usage: python {sys.argv[0]} <input_file> <output_prefix>")
        sys.exit(1)
    
    input_file, output_prefix = sys.argv[1], sys.argv[2]
    
    process_general(input_file)
    process_file(input_file)

if __name__ == "__main__":
    main()