
class RankerDB():
    
    def __init__(self) -> None:
        self.all_instances = {}
        self.instance_ranks = {}

    def get_max_rank(self):
        return len(self.instance_ranks.keys())