# Fender Mustang LT25 Smart Footswitch: Deployment & Stage Hardening Guide

This guide provides instructions for provisioning the **Raspberry Pi Zero 2 W**, configuring peripheral drivers, establishing system services, and locking down the filesystem with **OverlayFS** for cold-pull stage power immunity.

---

## 1. Operating System Provisioning

### 1.1 Flashing Raspberry Pi OS Lite
1. Insert a 16GB or 32GB Class 10 / A1 MicroSD card into your computer.
2. Launch the **Raspberry Pi Imager** (`rpi-imager`).
3. Select:
   * **Device:** Raspberry Pi Zero 2 W
   * **Operating System:** Raspberry Pi OS Lite (64-bit) (Debian Bookworm)
4. Click **Next** and edit OS Customization settings:
   * **Hostname:** `lt25-pedal`
   * **Username:** `pi`
   * **Password:** Set a secure password.
   * **Wireless LAN:** Configure your Wi-Fi SSID and PSK (enables SSH debugging on stage).
   * **Services:** Check **Enable SSH** (use password authentication or public key).
5. Flash and verify the card.

### 1.2 Boot Configuration (`config.txt`)
Before ejecting the card, open the `boot` (or `bootfs` / `firmware`) partition on your computer and edit `config.txt`:

```ini
# Enable Hardware I2C (Bus 1) for 1.3" OLED Display (400 kHz Fast Mode)
dtparam=i2c_arm=on
dtparam=i2c_arm_baudrate=400000

# Disable onboard audio to prevent DMA conflicts with WS2812B PWM0
dtparam=audio=off

# Disable Bluetooth to maximize power efficiency and reduce boot time (optional)
dtoverlay=disable-bt

# Enable USB Host Mode on OTG port
dtoverlay=dwc2,dr_mode=host
```

---

## 2. Core Dependencies & Driver Installation

Power up the Pi Zero 2 W and connect via SSH:
```bash
ssh pi@lt25-pedal.local
```

### 2.1 System Packages & Build Tooling
Update Debian repositories and install required C headers, USB libraries, and I2C tools:

```bash
sudo apt update && sudo apt install -y \
    git \
    python3-pip \
    python3-dev \
    libhidapi-dev \
    libusb-1.0-0-dev \
    i2c-tools \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    overlayroot
```

### 2.2 Python Package Installation
Install the necessary hardware abstraction and protocol parsing packages into the system Python environment:

```bash
sudo pip3 install --break-system-packages \
    hidapi \
    protobuf \
    RPi.GPIO \
    adafruit-circuitpython-ssd1306 \
    adafruit-circuitpython-sh1106 \
    luma.oled \
    pillow \
    rpi_ws281x
```

### 2.3 USB udev Security Rules
Grant non-root processes access to the Fender Mustang LT25 USB HID raw interface:

```bash
sudo bash -c 'cat << EOF > /etc/udev/rules.d/99-fender-lt25.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="1ed8", ATTRS{idProduct}=="0037", MODE="0666"
KERNEL=="hidraw*", ATTRS{idVendor}=="1ed8", ATTRS{idProduct}=="0037", MODE="0666"
EOF'

sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 2.4 TrueType Stage Font Deployment
To ensure the colossal 64pt numbers and preset names render with stage-ready clarity, copy a clean TrueType font (e.g. Roboto Bold, Montserrat, or DejaVu Sans Bold) to `/home/pi/font_stage.ttf`:

```bash
sudo cp /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf /home/pi/font_stage.ttf
```

---

## 3. Controller Software Deployment

### 3.1 Installing the Codebase
Clone the repository or copy the project files to the `/home/pi` directory:

```bash
cd /home/pi
git clone https://github.com/user/fender-mustang-lt25-smart-pedal.git .
```

Verify that the following files are present:
* `/home/pi/lt25_smart_pedal.py`
* `/home/pi/ltamp/` (protocol driver and compiled protobuf files)
* `/home/pi/font_stage.ttf`

### 3.2 Testing Peripheral Functionality
Run an interactive test to verify hardware before setting up the background service:

```bash
sudo python3 /home/pi/lt25_smart_pedal.py
```

* **OLED:** Should light up showing `01 Fender Clean` with a 64pt colossal number.
* **LEDs:** LED 1 should illuminate in Emerald Green; LEDs 2–5 should glow Dim White.
* **Rotary Knob:** Rotating should cycle presets `01` through `60` with instant OLED updating.
* **Footswitches:** Pressing switches 1–5 should switch presets; re-pressing active preset should invert OLED and turn LED Fiery Red (Solo Boost).

Press `Ctrl+C` to terminate the manual test.

---

## 4. Production Daemon Configuration (`systemd`)

To run the controller autonomously on boot with zero operator intervention, register it with `systemd`.

### 4.1 Installing the Service Unit
The systemd unit configuration is defined in [`systemd/lt25-pedal.service`](../systemd/lt25-pedal.service):

```ini
[Unit]
Description=Fender Mustang LT25 Smart Footswitch Controller Daemon
Documentation=https://github.com/user/fender-mustang-lt25-smart-pedal
After=network.target sound.target
Wants=sound.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/lt25_smart_pedal.py
Restart=always
RestartSec=3
KillSignal=SIGINT
TimeoutStopSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=lt25-pedal
Environment=PYTHONUNBUFFERED=1

# Hardware access security relaxations for rpi_ws281x DMA/PWM memory access
LimitMEMLOCK=infinity

[Install]
WantedBy=multi-user.target
```

Copy the unit file into the system systemd directory:

```bash
sudo cp /home/pi/systemd/lt25-pedal.service /etc/systemd/system/lt25-pedal.service
sudo chmod 644 /etc/systemd/system/lt25-pedal.service
```

### 4.2 Activating the Service
Reload systemd, enable the unit for boot execution, and start the daemon:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lt25-pedal.service
sudo systemctl start lt25-pedal.service
```

### 4.3 Monitoring Daemon Logs
View real-time telemetry, footswitch events, and USB connection status:

```bash
journalctl -u lt25-pedal.service -f
```

Example journal output:
```text
Nov 12 21:00:02 lt25-pedal systemd[1]: Started Fender Mustang LT25 Smart Footswitch Controller Daemon.
Nov 12 21:00:03 lt25-pedal lt25-pedal[482]: 1.3" SH1106 OLED initialized via luma.oled.
Nov 12 21:00:04 lt25-pedal lt25-pedal[482]: Connected to Fender Mustang LT25 via USB HID (Sync complete).
Nov 12 21:00:04 lt25-pedal lt25-pedal[482]: Synchronized with Fender LT25: Slot 1 (Fender Clean)
Nov 12 21:00:04 lt25-pedal lt25-pedal[482]: DSP Synced: OD=False, MOD=False, DLY=False, REV=True, BaseVol=-12.0dB
Nov 12 21:00:04 lt25-pedal lt25-pedal[482]: Button & Encoder Monitor loop started.
```

---

## 5. OverlayFS Hardening: Zero-Shutdown Power Safety

### 5.1 The Risk: Stage Power Outages & SD Corruption
In live concert and rehearsal environments, musicians power off guitar pedalboards by **unceremoniously yanking the 9V power cord** or killing the master power strip switch.

Standard Linux installations maintain an open `ext4` journaling filesystem. Abrupt power loss during write operations (log commits, temporary file creation, timestamp updates) inevitably results in **dirty filesystem bits, inode corruption, and boot failure** ("Kernel Panic: Unable to mount root fs").

### 5.2 The Solution: Ephemeral RAM OverlayFS
Using the Linux kernel **OverlayFS** subsystem via Debian's `overlayroot` package:
1. The physical MicroSD card root filesystem is mounted strictly **Read-Only (`ro`)**.
2. A temporary virtual RAM drive (**`tmpfs`**) is mounted as an upper read-write overlay layer.
3. Every write operation generated by Linux (systemd logs, temporary sockets) is directed solely into RAM.
4. **Physical SD Card Immobility:** Zero physical write cycles occur on the MicroSD card during operation. The 9V power cable can be ripped out at any time without risking card corruption. On next power-up, the Pi boots instantly from the pristine physical image.

### 5.3 Step-by-Step OverlayFS Configuration

#### Step 1: Configure `overlayroot`
Edit the overlayroot configuration file:
```bash
sudo nano /etc/overlayroot.conf
```

Set the driver to allocate a RAM `tmpfs` layer:
```ini
overlayroot="tmpfs"
```

#### Step 2: Lock the Boot Partition in `/etc/fstab`
Ensure the FAT32 firmware partition cannot be corrupted by changing its mount option to read-only in `/etc/fstab`:

```bash
sudo nano /etc/fstab
```

Change the `/boot/firmware` (or `/boot`) entry from `defaults` to `ro,defaults`:
```fstab
PARTUUID=xxxx-01  /boot/firmware  vfat  ro,defaults  0  2
```

#### Step 3: Reboot and Verify Immunity
Reboot the Raspberry Pi:
```bash
sudo reboot
```

After rebooting, verify that OverlayFS is active:
```bash
df -h
```
You should observe `overlayroot` mounted as the root filesystem:
```text
Filesystem      Size  Used Avail Use% Mounted on
overlayroot      14G  2.1G   12G  15% /
tmpfs           240M   12K  240M   1% /media/root-rw
/dev/mmcblk0p2   14G  2.1G   12G  15% /media/root-ro
```

---

## 6. Maintenance & Persistent Update Workflow

When OverlayFS is active, changes made to files in `/home/pi` are stored only in volatile RAM and will vanish upon reboot.

To permanently modify files (e.g. updating [`lt25_smart_pedal.py`](../lt25_smart_pedal.py) or updating presets):

### Method A: Direct Persistent Root Remount (Fastest)
The underlying read-only physical SD partition remains accessible at `/media/root-ro`. Remount it read-write, copy your updates directly, and remount read-only:

```bash
# 1. Remount physical card as Read-Write
sudo mount -o remount,rw /media/root-ro

# 2. Apply persistent modifications directly to the physical storage
sudo nano /media/root-ro/home/pi/lt25_smart_pedal.py

# 3. Flush buffers and restore physical card to Read-Only
sync
sudo mount -o remount,ro /media/root-ro

# 4. Restart service to apply changes
sudo systemctl restart lt25-pedal.service
```

### Method B: Temporary Overlay Disable (For Kernel/Package Upgrades)
When installing apt packages or system upgrades:
```bash
# Temporarily bypass overlayroot for the next boot
sudo overlayroot-chroot
```
Or edit `/boot/firmware/cmdline.txt` to remove `overlayroot=tmpfs`, perform standard upgrades with `sudo apt upgrade`, and re-enable `overlayroot=tmpfs`.
