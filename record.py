import time
import threading
import pickle
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

# 全局变量定义
rec = {}
start_time = 0

# OSC消息处理函数（已修正 startswith 拼写错误）
def osc_handler(address, *args):
    global rec, start_time
    if address.startswith('/avatar/parameters/v2'):
        recorded_time = time.time() - start_time
        if recorded_time not in rec:
            rec[recorded_time] = {}
        rec[recorded_time][address] = args

def record(record_time, file_name, ip="127.0.0.1", port=9000):
    global rec, start_time
    # 重置记录器和计时器
    rec = {}
    start_time = time.time()
    
    # 配置分发器
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(osc_handler)
    
    # 创建线程化服务器
    server = ThreadingOSCUDPServer((ip, port), dispatcher)
    
    # 在子线程中启动服务器
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True  # 设置为守护线程
    server_thread.start()
    
    print(f"开始监听 {ip}:{port}，持续 {record_time} 秒...")
    time.sleep(record_time)  # 阻塞等待指定时间
    
    # 关闭服务器
    server.shutdown()
    server.server_close()
    
    print("\n录制结束，结果如下：")
    # print(rec)
    with open(file_name, "wb") as f:
        pickle.dump(rec, f)

# 使用示例
if __name__ == "__main__":
    record(20,'rec.pkl')
