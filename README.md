# 퍼스널컬러 관리 서버
## DB 스키마
```
{
  "_id": ObjectID(),
  "ClientName": str,
  "data": {
    "CustomerName": str,
    "ColorCode": str
  },
  "status": "waiting" | "inprogress1" | "inprogress2" | "done",
  "assignedAt": 0 | 1 | 2
}
```

## 라즈베리파이 서버
[allocateManager.py](https://github.com/ShinsungPRON/server/blob/main/server/allocateManager.py)를 사용합니다. <br>
```
// allocatemgr.conf
ColorCombinator1Addr: 사용할 1번 색조합기의 주소입니다.
ColorCombinator1Port: 사용할 1번 색조합기의 포트 번호입니다. 

ColorCombinator2Addr: 사용할 2번 색조합기의 주소입니다.
ColorCombinator2Port: 사용할 2번 색조합기의 포트 번호입니다.

SignalAddr: 없어질 예정입니다.
SignalPort: 없어질 예정입니다. 
```

### 서버 → 색조합기 통신
```
{
  "_id": str  // 작업의 _id를 문자열로 보냅니다.
  "code": str // 색상 컬러코드입니다. 
}
```

### 색조합기 → 서버 통신
```
{
  "_id": str, // 완료한 작업의 id입니다.
  "status": "done" | "error",
  "device": int // 보내는 색조합기 번호입니다. 
}
```

## 색조합기 서버
[allocator.py](https://github.com/ShinsungPRON/server/blob/main/serialCommunicator/allocator.py)를 사용합니다. <br>
미완성입니다. <br>
* **테스트 코드**
```py
from pprint import pprint
import socket
import threading
import json
import time
import sys


def connect(soc):
    try:
        while True:
            msg = soc.recv(1024).decode()
            data = json.loads(msg)

            pprint(data)
            time.sleep(5)

            soc.send(
                json.dumps(
                    {
                        "_id": data["_id"],
                        "status": "done",
                        "device": 1
                    }
                ).encode()
            )

    except Exception:
        return


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("localhost", int(sys.argv[1])))
soc.listen(1)

while True:
    sock, addr = soc.accept()
    print("connection established with", addr)
    threading.Thread(target=connect, args=(sock,)).start()
```

## 크롬북
[client.py](https://github.com/ShinsungPRON/server/blob/main/client/client.py)를 사용합니다. <br>
```
// conf.conf
ClientName: 크롬북의 ID입니다. (ex: CHROMEBOOK_01)
ServerAddr: 라즈베리파이 서버의 주소입니다. 
ServerPort: 라즈베리파이 서버의 포트입니다
```
```
// data.dat (예시)
이름           // 이름을 입력합니다. data의 CustomerName 값이 됩니다. 
FFFFFF        // 색상코드를 입력합니다. data의 ColorCode 값이 됩니다.
```

### 크롬북 → 서버 통신
```
{
    "ClientName": str,
    "data": {
        "CustomerName": str,
        "ColorCode": str
    }
}
```