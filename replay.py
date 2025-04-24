import time
import pickle
from tqdm import tqdm
from pythonosc.udp_client import SimpleUDPClient

def replay(file, server = "127.0.0.1", port = 9000):
    
    client = SimpleUDPClient(server, port) 

    with open(file, 'rb') as f:
        rec = pickle.load(f)
    time_list = list(rec.keys())
    
    start_time = time.time()
    diff = 0.0
    total_delay = 0
    for next_count in tqdm(range(len(time_list))):

        while True:
            now = time.time()
            diff = now - start_time
            if diff > time_list[next_count]:
                total_delay += diff - time_list[next_count]
                for para in rec[time_list[next_count]]:
                    client.send_message(para, rec[time_list[next_count]][para])
                break

    print(f'avg_delay = {total_delay/len(time_list)}')
if __name__ == '__main__':
    replay('./rec.pkl')