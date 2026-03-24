# Raspberry Pi 5 Drone Detection
# Roni Bandini @RoniBandini
# March 2026
# MIT License

import subprocess
import time
import json
import re
from gpiozero import LED

banner = """
🚁 DRONE DETECTOR 🚁

██████╗ ██████╗  ██████╗ ███╗   ██╗███████╗
██╔══██╗██╔══██╗██╔═══██╗████╗  ██║██╔════╝
██║  ██║██████╔╝██║   ██║██╔██╗ ██║█████╗  
██║  ██║██╔══██╗██║   ██║██║╚██╗██║██╔══╝  
██████╔╝██║  ██║╚██████╔╝██║ ╚████║███████╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
"""

print(banner)

print("Roni Bandini, March 2026, Argentina, @RoniBandini")
print("Machine Learning via Edge Impulse 🤖")
print("Monitoring for drone presence... 👀")
print("Stop with CTRL-C")
print("")

# Settings
CONFIDENCE_THRESHOLD = 75.0
GPIO_PIN = 17   # BCM GPIO17 (pin físico 11)
LED_ON_TIME = 3

output_file = open('output.txt', 'w')

# Initialize GPIO using gpiozero
try:
    led = LED(GPIO_PIN)
    led.off()
    print(f"✓ GPIO {GPIO_PIN} initialized with gpiozero 🟢")
except Exception as e:
    led = None
    print(f"⚠️ GPIO init error {GPIO_PIN}: {e}")

print("")

RUNNER_PATH = "edge-impulse-linux-runner"
subprocess.Popen([RUNNER_PATH], stdout=output_file)

try:
    with open("output.txt", "r") as f:
        lines_seen = set()
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            
            if "[]" in line:
                continue
            
            match = re.search(r"classifyRes \d+ms\. ({.*})", line)
            if match and line not in lines_seen:
                raw = match.group(1)
                
                raw_fixed = raw.replace("'", '"')
                raw_fixed = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', raw_fixed)
                
                try:
                    classifications = json.loads(raw_fixed)
                    
                    print("\n--- Inference ---")
                    for label, score in classifications.items():
                        pct = score * 100.0
                        print(f" {label}: {pct:.2f}%")
                    
                    if 'drone' in classifications:
                        drone_confidence = classifications['drone'] * 100.0
                        
                        if drone_confidence >= CONFIDENCE_THRESHOLD:
                            print(f"\n🚨 DRONE DETECTED! ({drone_confidence:.2f}%)")
                            
                            if led:
                                try:
                                    led.on()
                                    print(f"🟢 GPIO {GPIO_PIN} ON")
                                    time.sleep(LED_ON_TIME)
                                    led.off()
                                    print(f"🔴 GPIO {GPIO_PIN} OFF\n")
                                except Exception as e:
                                    print(f"GPIO error: {e}")
                            else:
                                print("⚠️ GPIO not initialized\n")
                
                except json.JSONDecodeError as e:
                    print("JSON decode error:", e)
                    print("Attempted to parse:", raw_fixed)
                
                lines_seen.add(line)

except KeyboardInterrupt:
    print("\n\nStopping drone detection (CTRL-C). 🛑")
except Exception as e:
    print(f"\nError: {e}")
finally:
    try:
        if led:
            led.off()
            led.close()
            print(f"GPIO {GPIO_PIN} released.")
    except Exception:
        pass

    output_file.close()
    print("Execution ended. ✅")