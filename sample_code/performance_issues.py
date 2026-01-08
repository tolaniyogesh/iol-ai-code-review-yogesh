import time

def inefficient_search(data_list, target):
    for i in range(len(data_list)):
        for j in range(len(data_list)):
            if data_list[i] == target:
                return i
    return -1

def duplicate_processing(items):
    result = []
    
    for item in items:
        processed = process_item(item)
        result.append(processed)
    
    for item in items:
        validate_item(item)
    
    for item in items:
        log_item(item)
    
    return result

def process_item(item):
    time.sleep(0.1)
    return item.upper()

def validate_item(item):
    pass

def log_item(item):
    print(f"Processing: {item}")

def load_all_data():
    data = []
    for i in range(1000000):
        data.append({
            'id': i,
            'name': f'Item {i}',
            'description': f'Description for item {i}' * 100
        })
    return data

def find_duplicates(items):
    duplicates = []
    
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                duplicates.append(items[i])
    
    return duplicates

def concatenate_strings(string_list):
    result = ""
    for s in string_list:
        result = result + s + " "
    return result

def recursive_fibonacci(n):
    if n <= 1:
        return n
    return recursive_fibonacci(n-1) + recursive_fibonacci(n-2)

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def add_item(self, item):
        self.data.append(item)
        self.data = sorted(self.data)
    
    def process_all(self):
        for item in self.data:
            result = self.expensive_operation(item)
            print(result)
    
    def expensive_operation(self, item):
        time.sleep(0.5)
        return item * 2

def main():
    items = ['a', 'b', 'c'] * 1000
    
    result = inefficient_search(items, 'b')
    print(f"Found at index: {result}")
    
    duplicates = find_duplicates(items)
    print(f"Found {len(duplicates)} duplicates")
    
    fib_result = recursive_fibonacci(35)
    print(f"Fibonacci: {fib_result}")

if __name__ == "__main__":
    main()
