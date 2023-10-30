from pyrediscore.redantic import KeyStoreError, StoreKeyNotFound
from pyproteinsext import uniprot as pExt
from .schemas import GODatum, UniprotDatum, SecondaryId, UniprotCollection, UniprotAC
from typing import Union, Iterator

class UniprotStoreDummy():
    """ Mockup implementation, all dict of UniProtStore
    """
    def __init__(self):
        self.wipe_all()
        print("Youppi")
    
    def wipe_all(self):
        self._store = { 'GO_data'            : {},
                        'UniProt_data'       : {},
                        'SecondaryIds'       : {},
                        'UniprotCollections' : {}
        }
    def add(self, obj:Union[GODatum, UniprotDatum, SecondaryId, UniprotCollection]):
        end_point = None
        id        = None
        narrow_me =  dict(obj)

        if 'evidence' in narrow_me:
            end_point = self._store['GO_data']
            id = obj.id
        elif 'full_name' in narrow_me:
            end_point = self._store['UniProt_data']
            id = obj.id
        elif 'parent_id' in narrow_me:
            end_point = self._store['SecondaryIds']
            id = obj.id
        elif 'comments' in narrow_me:
            id = obj.comments
            end_point = self._store['UniprotCollections']
        else:
            raise TypeError(f"Unregistred type {type(obj)}")

        if id in end_point:
            raise KeyStoreError(f"{id} already in db")
        
        end_point[id] = obj
            
    def save_collection(self, comments:str, uniprot_ids:list[UniprotAC]):
        coll = UniprotCollection(comments=comments, content=uniprot_ids)
        try:
            self.add(coll)
            #print(coll.comments, "added")
        except KeyStoreError:
            print("Already in db", coll.comments, file=stderr)

    def load_uniprot_xml(self, file=None, stream=None):
        inserted_ok = []
        if not file and not stream:
            raise ValueError("please provide XML source with the file or stream arguments")
        if file:   
            collection = pExt.EntrySet(collectionXML=file)
        else:
            collection = pExt.EntrySet(streamXML=stream)
            
        for prot in collection:
            #print(prot.id, prot.AC)
            #print(prot)
            gos = []
            for go in prot.GO:
                go_obj = GODatum(id = go.id, evidence = go.evidence, term = go.term)
                gos.append(go_obj)
                try:                    
                    self.add(go_obj)
                   
                except KeyStoreError:
                    #print("Already in db", go.id)
                    pass
            try :
                obj = UniprotDatum(id=prot.id, 
                    full_name=prot.fullName, 
                    name=prot.name, 
                    gene_name=prot.geneName,
                    taxid=prot.taxid,
                    sequence=prot.sequence,
                    go = gos,
                    subcellular_location = prot.subcellular_location)
            except ValidationError as e:
                print(f"Validation failed for {prot.id}: {str(e)}", file=stderr)
                continue
            
            for sec_id in prot.AC:
                correspondance_obj = SecondaryId(id=sec_id, parent_id=prot.id)
                try:
                    self.add(correspondance_obj)
                    #print(sec_id, "mapping added")
                except KeyStoreError:
                    #print("Already in db", sec_id)
                    pass

            try:
                self.add(obj)
                #print(prot.id, "added")
            except KeyStoreError:
                #print("Already in db", prot.id)
                pass
            inserted_ok.append(prot.id)
            #print(f"{prot.id} now in db")
        print(f"{len(inserted_ok)} entries added to store")
        return inserted_ok

    def list_collection(self):
        col_summary = []
        for col_key, col_data in self._store['UniprotCollections'].items():
            col_summary.append( (col_data.comments, col_data.content) )
        return col_summary

    def get_protein_collection(self, collection_id_as_comment)->Iterator[UniprotDatum]:        
        if not collection_id_as_comment in self._store['UniprotCollections']:
            print(f"Collection \"{collection_id_as_comment}\" not found", file=stderr)
            return None
        collection = self._store['UniprotCollections'][collection_id_as_comment]
        for uniprot_id in collection.content:
            try:
                _ = self.get_protein(uniprot_id)
                yield _
            except StoreKeyNotFound:
                print(f"uniprot AC {uniprot_id} not found", file=stderr)
          

    def get_protein(self, uniprot_id:UniprotAC):
        """automatic forwarding of secondaryACs"""
        correspondance_obj = None
        try :     
            correspondance_obj = self._store['SecondaryIds'][uniprot_id]
            obj = self._store['UniProt_data'][correspondance_obj.parent_id]
            return obj

        except KeyError as e:
            if not correspondance_obj is None:
                msg = f"You provided an obsolete entry, but the actual Uniprot identifier {correspondance_obj.parent_id} was not found "
            else:
                msg = f"Uniprot identifier {uniprot_id} was not found"
            raise StoreKeyNotFound(msg)