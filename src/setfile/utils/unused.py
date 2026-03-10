import os
import time

def unused(folder,days):
    now = time.time()
    threshold = days * 86400

    unused_files = []

    for file in os.listdir(folder):
        path = os.path.join(folder,file)

        if os.path.isfile(path):
            last_access = os.stat(path).st_atime
            age = now - last_access

            if age > threshold:
                unused_files.append((file,int(age/86400)))
    
    unused_files.sort(key=lambda x: x[1], reverse=True)

    return unused_files