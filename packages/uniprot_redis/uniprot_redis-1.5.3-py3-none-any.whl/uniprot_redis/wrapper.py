from pyrediscore.redantic import StoreKeyNotFound
class Collector:
    """
    A single collection wrapper for easy multi type access
        constructor : uniprot_redis_store, collection name
        __getitem__ :
            str   : expects uniprotAC, returns corresponding UniprotDatum if any
            int   : returns the uniprotDatum at position if any
            slice : returns a list of UniprotDatum if slice limits are within collection size
    """
    def __init__(self, store, coll_name):
        self.store = store
        self.name = coll_name
        self.uniprot_acs = None

        colls =  self.store.list_collection()
        if not colls:
            raise ValueError("Store has no collection")
        for coll_id, coll_elems in colls:
            if coll_id == coll_name:
                self.uniprot_acs = coll_elems
                return
        raise StoreKeyNotFound(f"No collection named {coll_name} in provided store")
       

    def __len__(self):
        return len(self.uniprot_acs)

    def __getitem__(self, subscript):
        if type(subscript) is str:
            if not subscript in self.uniprot_acs:
                raise KeyError(f"{subscript} not in collection {self.name}")
            _ = self.store.get_protein(subscript)
            return _
        
        iterator =  self.store.get_protein_collection(self.name)
        i = 0
        results = []
        size = 0
        for datum in iterator:
            size += 1
            if isinstance(subscript, slice):
                if i >= subscript.start and i < subscript.stop:
                    results.append(datum)
                if i == subscript.stop:
                    return results
            else:
                if i == subscript:
                    return datum
            i += 1
        if isinstance(subscript, slice):
            if not results:
                raise IndexError(f"lower bound slice {subscript.start} is greater than iterable {size}")
            raise IndexError(f"higher bound slice {subscript.stop} is greater than iterable {size}")
        raise IndexError(f"index {subscript} is greater than iterable {size}")

    def __iter__(self):
        self.icurr_ac = 0
        return self
    def __next__(self):
        if self.icurr_ac >= len(self.uniprot_acs):
            raise StopIteration
        curr_ac = self.uniprot_acs[self.icurr_ac]
        self.icurr_ac += 1
        return self.store.get_protein(curr_ac)

        #return self.store.get_protein_collection(self.name)
