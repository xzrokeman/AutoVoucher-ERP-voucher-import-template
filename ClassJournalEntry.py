from attr import attrs, attrib, fields, validators

@attrs
class JournalEntry():
    Icode = attrib(validator=validators.instance_of(int))
    fattachment = attrib(validator=validators.instance_of(int))
    fabstract = attrib()
    faccount = attrib(validator=validators.instance_of(int))
    fdebit = attrib(validator=validators.instance_of(float))
    fcredit = attrib(validator=validators.instance_of(float))
    
if __name__ == '__main__':
    journalentry = JournalEntry(1, 3,"广交会差旅费", 6602008, 540.00, 0.00 )
    print(journalentry)

journalentry.__dict__
