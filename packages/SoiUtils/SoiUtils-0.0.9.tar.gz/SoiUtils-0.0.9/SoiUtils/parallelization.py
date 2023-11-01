import multiprocessing
class _ParallelizationWraper:
    def __init__(self,func,in_queue:multiprocessing.Queue,out_queue:multiprocessing.Queue):
        self.func = func
        self.in_queue =  in_queue
        self.out_queue =  out_queue
        self.worker = multiprocessing.Process(target=self)
        self.worker.start()

    def __call__(self):
        while True: 
            input = self.in_queue.get()
            if input is not None:
                self.out_queue.put(self.func(input))
            else:
                self.out_queue.put(None)
                break

class ParallelizedPipeline:
    def __init__(self,pipeline_funcs:list):
        self.parallelized_pipeline = []
        in_queue = multiprocessing.Queue()
        for func in pipeline_funcs:
            out_queue = multiprocessing.Queue()
            self.parallelized_pipeline.append(_ParallelizationWraper(func,in_queue,out_queue))
            in_queue = out_queue
        

    def write(self,to_write):
        self.parallelized_pipeline[0].in_queue.put(to_write)
    
    def read(self):
        return self.parallelized_pipeline[-1].out_queue.get()
    
    def stop_all(self):
        self.write(None)
        
