import threading
import queue
import east_data,cffex_data
q = queue.Queue()
threads = []

# 获取报价
def date_user(q):
    print("date_user")
    while True:
        item = q.get()
        print("user",item)

def get_value():
    """获取报价"""
    gu_no = '8_151111_mx'
    t = threading.Thread(target=east_data.get_data_stream,args=(q,gu_no))
    t.start()

    date_user(q)

def get_jyrl():
    """获取交易日历"""
    data = cffex_data.jyrl_base('202310')
    print(data)

if __name__ == '__main__':
    get_jyrl()


