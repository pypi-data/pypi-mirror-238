from tag_reader.tag_elemnts.tag_element_factory import BaseStructTagFactory, BaseAtomicFactory
from tag_reader.tag_elemnts.tag_element_list import ArrayTagElement, BlockTagElement, ResourceHandleTagElement, TagElementList
from tag_reader.tag_elemnts.tag_element_dict import RootTagElement, StructTagElement, TagElementDict
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_elemnts.tag_element import TagElement
from tag_reader.tag_layouts import TagLayouts

#StructTagElement(layout)
class TagElementReader:
    def __init__(self,atomic_factory:BaseAtomicFactory, struct_factory: BaseStructTagFactory):
        self.atomic_factory:BaseAtomicFactory = atomic_factory
        self.struct_factory:BaseStructTagFactory = struct_factory
        pass

    
    def getTagElemnt(self, layout:TagLayouts.C) -> TagElement :
        from_type = layout.T
        if from_type == TagElemntType.RootTagInstance:
            return RootTagElement(layout)
        elif from_type == TagElemntType.Struct:
            return self.struct_factory.getTagElemnt(layout)
        elif from_type == TagElemntType.Block:
            return BlockTagElement(layout)
        elif from_type == TagElemntType.Array:
            return ArrayTagElement(layout)
        elif from_type == TagElemntType.ResourceHandle:
            return ResourceHandleTagElement(layout)
        else:
            return self.atomic_factory.getTagElemnt(layout)
            
        return None

        t_e = TagElementReader.getTagElemnt(tag_template.T)
        if t_e is None:
            return
        if not self.currentElem is None:
            str_name = tag_template.N
            if tag_template.N =="":
               str_name = f"{dict_entry}_{int(tag_template.T)}"
            else: 
                if tag_template.T in [TagElemntType.Explanation, TagElemntType.Custom]:
                    str_name = f"{tag_template.N}_{int(tag_template.T)}"
            self.currentElem[2].setKeyValue(str_name,t_e)
        if tag_template.T == TagElemntType.RootTagInstance:
            self.root = t_e
            self.currentElem = (i,k,t_e)
        elif tag_template.T == TagElemntType.Struct:
            pass
        else:
            pass
          
        t_e.readTagElemnt(f,i,k,dict_entry, add_offset,entry,tag_template)

        
        pass