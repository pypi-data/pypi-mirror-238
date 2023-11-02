from redisz import Redisz

rdz = Redisz('localhost')
lock = rdz.lock('my_lock',timeout=1000)
print(lock.acquire())
# with rdz.lock('my_lock'):
#     print('abc')
# print(lock.acquire())

# lock.release()