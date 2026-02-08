from dataclasses import dataclass, fields

@dataclass
class Header:
    id: str
    qr: str
    opcode: str
    aa: str
    tc: str 
    rd: str
    ra: str
    z: str
    rcode: str
    qdcount: str
    ancount: str
    nscount: str
    arcount: str

@dataclass
class Question: 
    qtype: str
    qclass: str

def message_builder(header: Header, question: Question):
    bit_str = ""
    # header part reds each header value like id,qdcount
    for field in fields(header):
        field_name = field.name
        if(field_name == "id"):
            continue
        # converts the qdcount inot binary 4 hex values  and append to bit_str
        if(field_name == "qdcount"):
            bit_str = format(int(bit_str, 2), '04x')
        # itreate the reaimng header values dynamicaly and append to the bit_str
        field_value = getattr(header,field_name)
        bit_str += field_value
    # this is the qeustion paert goes through each quwrtions value and append to the query varible 
    query = ""
    for field in fields(question):
        field_name = field.name
        field_value = getattr(question,field_name)
        query += field_value
    # put the id as front and appent with bit_str and send the meassge + query to upd sockt 
    # so the finaly thng is like ID + FLAGS + COUNTS + QNAME + QTYPE + QCLASS
    id = getattr(header, "id")
    message = id + bit_str
    return message , query

def encode_domain(domain):
    encoded_name = b""
    #encods the domain name form www.google.com to  03 www 06 google 03 com 00
    # by . valeu its lenght and name return in Returns hex string
    labels = domain.split('.')
    for label in labels:
        encoded_name += bytes([len(label)])
        encoded_name += label.encode()
    encoded_name += b"\x00"
    return encoded_name.hex()

