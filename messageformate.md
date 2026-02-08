DNS in one mental model (keep this in your head)

Think of DNS as:

A structured binary protocol over UDP

Not text. Not HTTP. Just bytes.

Every DNS message looks like:

+---------+
| Header  |  (fixed size: 12 bytes)
+---------+
| Question(s) |
+---------+
| Answer(s)   |
+---------+
| Authority   |
+---------+
| Additional  |
+---------+


For a query, only Header + Question are filled.
For a response, Answer/Authority/Additional may be filled.

Step 1 – Building a DNS query (the heart of this challenge)
1️⃣ DNS Header (12 bytes)

Defined in RFC 1035 – Section 4.1.1

The header fields are:

Field	Size	Meaning
ID	16 bits	Random number to match request & response
Flags	16 bits	QR, RD, etc
QDCOUNT	16 bits	Number of questions
ANCOUNT	16 bits	Number of answers
NSCOUNT	16 bits	Authority records
ARCOUNT	16 bits	Additional records

For your first query:

ID → random (example: 22)

Flags → Recursion Desired = 1

QDCOUNT → 1

ANCOUNT → 0

NSCOUNT → 0

ARCOUNT → 0

That’s exactly 12 bytes.

2️⃣ Flags – important bit

Flags are a bit field.

You don’t need all of them now. Only this matters:

Bit	Name	Meaning
RD	Recursion Desired	Ask resolver to recurse for you

In Step 1–3 → RD = 1

In Step 4 → RD = 0 (you do recursion yourself)

Everything else can be zero.

3️⃣ Question section

Defined in RFC 1035 – Section 4.1.2

A question has 3 parts:

a) QNAME (encoded domain name)

This part trips everyone at first.

Domain:

dns.google.com


Encoding rule:

Split by .

Each label becomes:

<length byte><label bytes>


End with 0

So:

dns.google.com
↓
3 dns
6 google
3 com
0


In bytes:

03 64 6e 73
06 67 6f 6f 67 6c 65
03 63 6f 6d
00


This is why you see:

3dns6google3com0

b) QTYPE (2 bytes)

1 = A record (IPv4 address)

c) QCLASS (2 bytes)

1 = IN (Internet)

4️⃣ Full query message (assembled)

Put everything together in this exact order:

[Header]
[QNAME]
[QTYPE]
[QCLASS]


All numbers:

Big-endian

Network byte order

Example hex (from your description):

0016        ← ID
0100        ← Flags (RD = 1)
0001        ← QDCOUNT
0000        ← ANCOUNT
0000        ← NSCOUNT
0000        ← ARCOUNT
03 64 6e 73 06 67 6f 6f 67 6c 65 03 63 6f 6d 00
0001        ← QTYPE
0001        ← QCLASS


When hex-joined:

00160100000100000000000003646e7306676f6f676c6503636f6d0000010001


At this point you’ve built a valid DNS query 💥

Step 2 – Send it & receive response

Here the goal is not parsing yet.

What happens:

Create a UDP socket

Send query bytes to:

IP: 8.8.8.8
Port: 53