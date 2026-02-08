from dns import message

def decode_dns_responce(hex_string):
    # conversts the hex value to bytes
    byte_data = bytes.fromhex(hex_string)
    #the .from_wire Deserializer  it 
    dns_msg = message.from_wire(byte_data)
    #.answer takes up the ip directly just need to convert to text and prints here 
    if len(dns_msg.answer) > 0 :
        ans_list = []
        for i in (dns_msg.answer[0].items):
            ip_address = i.to_text()
            print(f"hey {ip_address}")
        return 0 , ans_list
    else:
        # if the no ip then prints the authority like puts the Name Servers (NS) for .com
        if len(dns_msg.authority) > 0 :
            authority_list = []
            for i in dns_msg.authority[0].items:
                ns_record = i.target.to_text()
                authority_list.append(ns_record)

            additional_list = []
            #this .additional thing has the direclty to the authoriy server name like ns1.google.com
            for i in dns_msg.additional:
                # this rdtype tel which recod like a , aaa, ns 
                if i.rdtype:
                    t = i.to_text().split()
                    if t[3] == 'A':
                        additional_list.append(t[4])
            return 1 , additional_list