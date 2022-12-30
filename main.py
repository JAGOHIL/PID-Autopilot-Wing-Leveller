import sys
import xpc
import PID
from datetime import datetime, timedelta

update_interval = 0.100
start = datetime.now()
last_update = start

P = 0.1
I = P/10
D = 0

roll_PID = PID.PID(P,I,D)

pitch_PID = PID.PID(P,I,D)

desired_roll = 0
desired_pitch = 2

roll_PID.SetPoint = desired_roll
pitch_PID.SetPoint = desired_pitch


def monitor():
    global last_update
    with xpc.XPlaneConnect() as client:
        while True:
            if (datetime.now() > last_update + timedelta(milliseconds=update_interval*1000)):
                last_update = datetime.now()
                print(f"loop start - {datetime.now()}")
                posi = client.getPOSI();
                ctrl = client.getCTRL();

                current_roll = posi[4]
                current_pitch = posi[3]

                roll_PID.update(current_roll)
                pitch_PID.update(current_pitch)

                ctrl = [new_ele_ctrl, new_all_ctrl, 0.0,-998]
                client.sendCTRL(ctrl)

                new_all_ctrl = roll_PID.output
                new_ele_ctrl = pitch_PID.output



                output = f"current values -- roll:{current_roll:0.3f},pitch: {current_pitch:0.3f}"

                output = output + "\n" + f"PID outputs       -- roll: {roll_PID.output:0.3f},   pitch:{pitch_PID.output}"
                output = output + "\n"
                print(output)







if __name__ == "__main__":
    monitor()

