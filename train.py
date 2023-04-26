import time
if __name__ == "__main__":
    
    count = 0
    while True:
        count += 1
        if count == 10:
            time.sleep(1)
            break
    
    exit(1)