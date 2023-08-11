
class BrimoTest:
    def __init__(self):
        self.command = {}
        self.run = True
        import threading
        t = threading.Thread(target=self.wait_for_command, args=())
        t.start()
        
    def exit_test(self):
        import os
        import time
        for i in range(2):
            os.system("taskkill /im python.exe")
            time.sleep(1)
        self.run = False
        
    def stirrer_test(self):
        print('****** stirrer_test')
        c = int(input('[0 -> stop motor][1 -> start motor][2 -> move motor]: '))
        if c == 0:
            print('****** stop_motor')
            KN_STOP_SIG = 44
            QSpy._sendEvt(13, KN_STOP_SIG)
        if c == 1:
            print('****** start_motor')
            pack_info = "i"
            KN_RUN_SIG = 43
            speed = int(input('Speed [0-1000]: '))
            speed = speed * 65536
            QSpy._sendEvt(13, KN_RUN_SIG, pack(pack_info, speed))
        if c == 2:
            print('****** move_motor')
            pack_info = "ii"
            POS_RUN_SIG = 47
            ref_pos = 300
            ref_speed = int(input('Speed [0-1000]: '))
            print(ref_pos, ref_speed)
            ref_pos = ref_pos * 65536
            ref_speed = ref_speed * 65536
            QSpy._sendEvt(20, POS_RUN_SIG, pack(pack_info, ref_pos, ref_speed))
            

    def dispense_test(self):
        self.dispense_pack_info = "BBB"
        DISPENSE_TEST_SIG = 16
        self.commandId = 0
        self.ioPin = 0
        self.ioVal = 0
        debounce = 1
        print("****** dispense_test")
        print("         0 -> test OUTPUT pin")
        print("         1 -> test INPUT pin")
        print("         2 -> stirrer servo clock")
        print("         3 -> stirrer servo anti-clock")
        print("         4 -> get current loadcell")
        print("         5 -> get water temp sensor")
        self.commandId = int(input('Choose command [0-100]: '))
        if self.commandId == 0:
            print("test output pin")
            self.ioPin = int(input('Choose pin [0-100]: '))
            self.ioVal = int(input('Choose val [0-1]: '))
        elif self.commandId == 1:
            print("test input pin")
            self.ioPin = int(input('Choose pin [0-100]: '))
            debounce = 100
        elif self.commandId == 2 or self.commandId == 3:
            pass
        elif self.commandId == 4:
            debounce = 100
        elif self.commandId == 5:
            debounce = 200
        
        print(self.commandId, self.ioPin, self.ioVal)
        for i in range(debounce):
            QSpy._sendEvt(15, DISPENSE_TEST_SIG, pack(self.dispense_pack_info, self.commandId, self.ioPin, self.ioVal))

    def heater_test(self):
        print('****** heater_test')
        pack_info = "Bii"
        HEATER_CLOSE_LOOP_SIG = 47
        ht_id = 0
        begin_pid = 0
        ref_temp = int(input('Temperature [0-400]: '))
        ref_temp = ref_temp * 65536
        begin_pid = begin_pid * 65536
        QSpy._sendEvt(26, HEATER_CLOSE_LOOP_SIG, pack(pack_info, ht_id, ref_temp, begin_pid))

    def init_command(self):
        self.command[1] = self.stirrer_test
        self.command[2] = self.heater_test
        self.command[3] = self.dispense_test
        self.command[44] = self.exit_test
        
    def init_data(self):
        ####### dispensor ###########
        pass

    def wait_for_command(self):
        self.init_command()
        self.init_data()
        
        while self.run:
            print('List all commands:')
            print(' -> 1:  Test Stirrer Motor')
            print(' -> 2:  Test Heater')
            print(' -> 3:  Test Dispensor')
            print(' -> 44: Exit')
            c = int(input('Enter your command:'))
            if c in list(self.command.keys()):
                try:
                    self.command[c]()
                except Exception as e:
                    print("exception: " + str(e))
                    self.exit_test()
                
    
    def QS_USER_00(self, packet):
        unpacked = qunpack("xxTxZ", packet)
        time = unpacked[0]
        data = unpacked[1]
        if data.startswith("stirrer"):
            print(data)
        if data.startswith("water_level_sensor"):
            print(data)
        if data.startswith("current_weight_scale"):
            print(data)
        if data.startswith("water_temp_sensor"):
            print(data)

QView.customize(BrimoTest())
