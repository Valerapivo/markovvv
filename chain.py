import sys
import random
import csv

def load_probabilities(prefix, max_order=13):
    probabilities = {0: {}}
    
    for order in range(max_order, 0, -1):
        try:
            with open(f"{prefix}{order}.csv", 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                order_probs = {}
                for row in reader:
                    if int(row['order']) == order:
                        context = row['context']
                        symbol = row['symbol']
                        prob = float(row['probability'])
                        
                        if context not in order_probs:
                            order_probs[context] = {}
                        order_probs[context][symbol] = prob
                probabilities[order] = order_probs
                print(f"{order} symbol file loaded")
        except FileNotFoundError:
            print(f"no {order} symbol file")
            probabilities[order] = {}
    
    try:
        with open(f"{prefix}0.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['order']) == 0:
                    symbol = row['symbol']
                    prob = float(row['probability'])
                    probabilities[0][symbol] = prob
        print("0 symbol file loaded")
    except FileNotFoundError:
        print("no 0 symbol file")
        probabilities[0] = {}
    
    return probabilities

def generate_text(start_text, probabilities, num_chars=1000):
    generated = list(start_text)
    
    symbols = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?')
    
    for i in range(num_chars):
        found = False
        
        for order in range(13, 0, -1):
            if len(generated) < order:
                continue
                
            context = ''.join(generated[-order:])
            
            if order in probabilities and context in probabilities[order]:
                symbol_probs = probabilities[order][context]
                symbols_list = list(symbol_probs.keys())
                probs_list = list(symbol_probs.values())
                
                next_char = random.choices(symbols_list, weights=probs_list, k=1)[0]
                generated.append(next_char)
                found = True
                break
        
        if not found and probabilities[0]:
            symbols_list = list(probabilities[0].keys())
            probs_list = list(probabilities[0].values())
            next_char = random.choices(symbols_list, weights=probs_list, k=1)[0]
            generated.append(next_char)
            found = True
        
        if not found:
            next_char = random.choice(list(symbols))
            generated.append(next_char)
        
        if (i + 1) % 100 == 0:
            print(f"\rammount of generated symbols: {i + 1}/{num_chars}", end='')
    
    print(f"\rammount of generated symbols: {num_chars}/{num_chars}")
    
    continuation = ''.join(generated[len(start_text):len(start_text) + num_chars])
    return start_text + continuation

def main():
    if len(sys.argv) != 5:
        print(f"usage: python {sys.argv[0]} <input_text> <probabilities_prefix> <output_file> <num_chars>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    prefix = sys.argv[2]
    output_file = sys.argv[3]
    num_chars = int(sys.argv[4])
    
    with open(input_file, 'r', encoding='utf-8') as f:
        start_text = f.read()
    
    print("loading probalilities...")
    probabilities = load_probabilities(prefix)
    
    print("genering text...")
    result = generate_text(start_text, probabilities, num_chars)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"save {output_file}")

if __name__ == "__main__":
    main()