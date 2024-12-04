# Centralized log handling in Python

This is a simple example of how to handle logs in a centralized way using Python. The example uses the `logging` module.
It's just a PoC project for myself to try how to handle logs in a centralized way. How the `logging.handlers.SockerHandler` 
works and how to can I make it more robust with some additional features like TCP keep-alive and reconnect if some network 
error occurs.

In the project I implemented a simple TCP server that receives the logs from the client and writes them to STDOUT and a
client that sends the logs to the server. The client uses a modified `SocketHandler` the `ReconnectionSocketHandler`.

## What is that byte order thing?

The **byte order** refers to how multi-byte data (e.g., integers, floating-point numbers) is stored in memory or 
transmitted over a network. The two main types of byte order are **big-endian** and **little-endian**.

---

### **1. What is Byte Order?**
When representing multi-byte numbers, the order of bytes matters. For example, the number `305419896` in hexadecimal is 
`0x12345678`. This can be stored in memory in two main ways:

- **Big-Endian:** The **most significant byte (MSB)** comes first.
    - Memory: `0x12 0x34 0x56 0x78`
- **Little-Endian:** The **least significant byte (LSB)** comes first.
    - Memory: `0x78 0x56 0x34 0x12`

The choice of byte order is important when data is transferred between systems or written to files.

---

### **2. Big-Endian**
- **Definition:** The most significant byte (the "biggest" part) is stored first, at the lowest memory address.
- **Example:**
    - Number: `0x12345678` (305419896 in decimal)
    - Memory (Big-Endian): `0x12 0x34 0x56 0x78`
- **Use Case:**
    - Commonly used in **network protocols** (referred to as "network byte order").
    - Some CPUs like PowerPC and SPARC use this as their native byte order.

---

### **3. Little-Endian**
- **Definition:** The least significant byte (the "smallest" part) is stored first, at the lowest memory address.
- **Example:**
    - Number: `0x12345678` (305419896 in decimal)
    - Memory (Little-Endian): `0x78 0x56 0x34 0x12`
- **Use Case:**
    - Used by most modern CPUs like **x86** and **ARM** processors.

---

### **4. Why Does Byte Order Matter?**
1. **Data Interoperability:**
    - When systems with different byte orders communicate (e.g., over a network), they must agree on how to interpret 
      multi-byte data.
    - For example, network protocols use big-endian ("network byte order"), so systems must convert if their native 
      format is little-endian.

2. **File Formats:**
    - File formats often specify a particular byte order to ensure compatibility across platforms.

3. **Performance:**
    - Some operations may be more efficient on hardware that uses the same byte order as the data format.

---

### **5. Python and Byte Order**
Python provides tools to handle byte order explicitly, especially for network communication or binary file parsing.

#### **`struct` Module**
The `struct` module is used to convert between Python objects and byte data, allowing you to specify byte order:

- **Big-Endian (`>`):**
  ```python
  import struct

  # Pack an integer (big-endian)
  big_endian_data = struct.pack('>I', 305419896)
  print(big_endian_data)  # Output: b'\x12\x34\x56\x78'

  # Unpack the data
  unpacked = struct.unpack('>I', big_endian_data)[0]
  print(unpacked)  # Output: 305419896
  ```

- **Little-Endian (`<`):**
  ```python
  # Pack an integer (little-endian)
  little_endian_data = struct.pack('<I', 305419896)
  print(little_endian_data)  # Output: b'\x78\x56\x34\x12'

  # Unpack the data
  unpacked = struct.unpack('<I', little_endian_data)[0]
  print(unpacked)  # Output: 305419896
  ```

---

### **6. Practical Example: Byte Order in Networking**
Suppose you send an integer over a TCP connection. To ensure compatibility, you use big-endian format
(network byte order):

#### Sender:
```python
import socket
import struct

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))

# Integer to send
number = 305419896

# Pack the integer in big-endian format and send
data = struct.pack('>I', number)
client_socket.send(data)
client_socket.close()
```

#### Receiver:
```python
import socket
import struct

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(1)

# Accept a connection
conn, addr = server_socket.accept()

# Receive 4 bytes and unpack as big-endian
data = conn.recv(4)
number = struct.unpack('>I', data)[0]
print(number)  # Output: 305419896
conn.close()
server_socket.close()
```