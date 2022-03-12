import subprocess as t
import platform as p
import sys

platform = p.system()

if platform == 'Windows':
    adb = './adb.exe'
elif platform == 'Linux':
    if hasattr(sys, 'getandroidapilevel'):
        adb = 'fakeroot adb'
        print('Termux의 초기 설정을 시작합니다.')
        t.Popen('pkg update && apt upgrade -y', shell=True).wait(timeout=None)
        t.Popen('apt install -y fakeroot', shell=True).wait(timeout=None)
        t.Popen('apt install -y android-tools', shell=True).wait(timeout=None)
        print('Termux 초기 설정이 완료되었습니다.\n')

        onADB = t.check_output(['fakeroot', 'adb', 'devices'])
        onADB = onADB.splitlines()
        if len(onADB) <= 2:
            while True:
                print("1. 화면분할로 설정앱을 띄우세요.\n2. '설정' 앱에서 '개발자 옵션'을 띄우세요.")
                print("3. 무선 디버깅을 찾아 활성화하신 후 들어가주세요.\n4. '페어링 코드로 기기 페어링'을 눌러주세요.")
                ip = input("5. termux 창을 다시 누른 후 'IP 주소 및 포트'라고 적힌 부분의 아래 내용을 그대로 입력해주세요.\n")
                paircode = input("'Wi-Fi 페어링 코드'라고 적힌 부분의 아래 6자리 숫자를 입력해주세요.\n")
                if input('위의 설정을 완료하셨습니까? (y/n) ') in ['y', 'Y', 'yes', 'Yes', 'YES']:
                    t.Popen(f'{adb} pair {ip} {paircode}', shell=True).wait(timeout=None)
                    ip = input("설정창에 보이는 'IP 주소 및 포트'라고 적힌 부분의 아래 내용을 그대로 입력해주세요.\n")
                    t.Popen(f'{adb} connect {ip}', shell=True).wait(timeout=None)
                    break
                else:
                    print('위의 설정을 완료해주세요.')
    else:
        adb = './adb_linux'
elif platform == 'Darwin':
    adb = './adb_mac'

devices = t.Popen(f"{adb} devices", shell=True, stdout=t.PIPE).stdout.read().split()
for i in [b'List', b'of', b'devices', b'attached', b'daemon', b'not', b'running;',
          b'starting', b'now', b'at', b'localfilesystem:/data/data/com.termux/files/adb_socket', b'*',
          b'started', b'successfully']:
    if i in devices:
        devices.remove(i)

print('해제하시려는 기기의 One UI 버전이 필요합니다. 안내에 따라 One UI 버전을 확인하여 입력해주세요.')
print('1. 설정앱에 들어갑니다.\n2. 가장 아래로 내려 휴대전화 정보에 들어갑니다.')
print('3. 소프트웨어 정보에 들어갑니다.\n4. 가장 위에 있는 One UI 버전을 확인합니다.')
print('\n⚠️ 상기된 안내에 따라 진행하실 수 없으신 경우 번거로우시겠지만 버전의 확인 방법을 찾아 진행해주세요. 구형기기의 경우 One UI가 탑재되지 않았을 수도 있습니다.')

for i in devices:
    ver = int(input('버전을 선택하세요.\n1. One UI 4.0 이상\n2. One UI 4.0 미만 혹은 One UI 미탑재 기기\n3. 종료\n>> '))
    if ver not in [1, 2]:
        print('프로그램을 종료합니다.')
        exit()

    curses = {
        'gos': 'GOS',
        'gamehome': '게임런처',
        'gameboosterplus': '게임부스터 플러스',
        'gametools': '게임부스터',
        # 게임우선모드는 영어로 뭐라 검색해야 나오냐 도대체
    }

    theCursedOnes = {}

    for i in range(0, len(devices), 2):
        device = devices[i].decode('utf-8')
        brand = t.Popen(
            f"{adb} -s " + device + " shell getprop ro.product.brand", shell=True, stdout=t.PIPE
        ).stdout.read().decode('utf-8').splitlines()[0]
        if brand == "samsung":
            theCursedOnes[brand] = t.Popen(
                f"{adb} -s " + device + " shell getprop ro.product.model", shell=True, stdout=t.PIPE
            ).stdout.read().decode('utf-8').splitlines()[0]

    adb += ' shell'

    if ver == '1':
        #print(f'\n선행 작업이 필요합니다. automate에서 선행작업을 완료해주세요.')

        #while True:
            #pre = input('선행작업을 완료하였습니까? (y/n)')
            #if pre in ['y', 'Y', 'yes', 'Yes', 'YES']:
                #break
            #else:
                #print('선행작업을 완료해주세요.')

        for cursedOne in theCursedOnes:
            print('\n' + theCursedOnes[cursedOne] + '의 작업시작\n')

            if len(devices)/2:
                base = 'com.samsung.android.game.'
                for app in curses.keys():
                    exist = t.Popen(f'{adb} pm list packages {base}{app}', shell=True, stdout=t.PIPE).stdout.read().split()
                    if len(exist):
                        clear = t.Popen(f'{adb} pm clear {base}{app}', shell=True, stdout=t.PIPE).stdout.read().split()
                        if clear[0] == b'Success':
                            print(f'{curses[app]} cleared')

            if input('기기를 지금 재부팅 하시겠습니까? (y/n)') in ['y', 'Y', 'yes', 'Yes', 'YES']:
                #while True:
                    #if input('Wi-Fi를 비활성화 하셨습니까? (y/n)') in ['y', 'Y', 'yes', 'Yes', 'YES']:
                        #break
                    #else:
                        #print('Wi-Fi를 꺼주세요.')
                t.Popen(f'{adb} "svc data disable && reboot && svc wifi disable"', shell=True, stdout=t.PIPE).stdout.read()
                print('재부팅 시작')
            else:
                print('재부팅 취소')
                print('\n' + theCursedOnes[cursedOne] + '의 작업완료\n')
                continue

            if input('기기 재부팅 후 잠금화면 해제 전에 엔터를 입력해주세요.') == '':
                while True:
                    gamelauncherkill = t.Popen(f'{adb} ps | grep com.samsung.android.game', shell=True, stdout=t.PIPE).stdout.read().split()
                    if len(gamelauncherkill):
                        for i in range(8, len(gamelauncherkill), 9):
                            i = gamelauncherkill[i].decode()
                            gamelauncherkill = t.Popen(f'{adb} am force-stop {i}', shell=True, stdout=t.PIPE).stdout.read().split()
                            appname = curses[i.split('.')[-1]]
                            print(f'{appname} 종료')
                        break

            if input('잠금화면 해제 후에 게임런처 아이콘을 보신 후 엔터를 입력해주세요.') == '':
                print('게임런처는 계속 다시 실행되니 되도록 게임런처 아이콘을 길게 눌러서 사용중지를 눌러 비활성화 하시길 바랍니다.')
                while True:
                    gamelauncherkill = t.Popen(f'{adb} ps | grep com.samsung.android.game', shell=True, stdout=t.PIPE).stdout.read().split()
                    if len(gamelauncherkill):
                        for i in range(8, len(gamelauncherkill), 9):
                            i = gamelauncherkill[i].decode()
                            gamelauncherkill = t.Popen(f'{adb} am force-stop {i}', shell=True, stdout=t.PIPE).stdout.read().split()
                            appname = curses[i.split('.')[-1]]
                            print(f'{appname} 종료')
                        break

            print('\n' + theCursedOnes[cursedOne] + '의 작업완료\n')
    elif ver == '2':
        print('\n' + theCursedOnes[cursedOne] + '의 작업시작\n')

        for curse in curses:
            t.Popen(f"{adb} pm disable-user --user 0 com.samsung.android.game.{curse}", shell=True).wait(timeout=None)
            print(f'{curse} 비활성화')

        print('\n' + theCursedOnes[cursedOne] + '의 작업완료\n')
