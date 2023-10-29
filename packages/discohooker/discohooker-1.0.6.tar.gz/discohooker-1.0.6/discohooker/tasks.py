import asyncio


class Tasks:


    def timed(second: int):
        def decorator(fun):
            while True:
                loop=asyncio.get_event_loop()
                loop.run_until_complete(fun())
                loop.run_until_complete(asyncio.sleep(second))
            return fun()
        return decorator


    def worker(fun):
        def work():
            loop=asyncio.get_event_loop()
            return loop.run_until_complete(fun())
        return work()