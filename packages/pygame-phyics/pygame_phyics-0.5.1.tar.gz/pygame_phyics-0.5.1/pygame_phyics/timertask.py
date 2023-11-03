import inspect
from pygame import time
from pygame_phyics.error import FunctionError

class TimerTask:
    def __init__(self, tick, event, *value, **kwargs):
        self.tick = tick
        self.last_update = 0
        print(type(event), inspect.ismethod(event))
        if inspect.ismethod(event) and inspect.isfunction(event):
            raise FunctionError(f"입력받은 값은 는 함수가 아닙니다")
        self.event = event
        self.value = value
        self.kwargs = kwargs
        
    def run_periodic_task(self):
        if time.get_ticks() - self.last_update > self.tick:
            self.last_update = time.get_ticks()
            self.event(*self.value, **self.kwargs)
            return True
        return False
    
    def reset(self):
        self.last_update = time.get_ticks()
        
class OnceTimerTask(TimerTask):
    def __init__(self, tick, event, *value, **kwargs):
        super().__init__(tick, event, *value, **kwargs)
        self.once = False
    
    def run_periodic_task(self):
        if time.get_ticks() - self.last_update > self.tick and not self.once:
            self.event(*self.value, **self.kwargs)
            self.once = True
            return True
        return False