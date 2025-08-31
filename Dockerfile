# Raspberry Pi OS Bullseye userspace (arm32)
FROM arm32v7/debian:bullseye-slim
ENV DEBIAN_FRONTEND=noninteractive

# -------- Base tools
RUN set -eux; \
  apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg pkg-config build-essential git \
    python3 python3-pip python3-setuptools python3-wheel python3-dev \
  && rm -rf /var/lib/apt/lists/*

# -------- Add Raspberry Pi repo (Bullseye) with signed-by keyring
RUN set -eux; \
  curl -fsSL https://archive.raspberrypi.org/debian/raspberrypi.gpg.key \
    | gpg --dearmor -o /usr/share/keyrings/raspberrypi-archive-keyring.gpg; \
  echo "deb [signed-by=/usr/share/keyrings/raspberrypi-archive-keyring.gpg] http://archive.raspberrypi.org/debian/ bullseye main" \
    > /etc/apt/sources.list.d/raspi.list

# -------- Prefer RPi builds for libcamera/picamera2
RUN set -eux; \
  printf "Package: libcamera*\nPin: origin archive.raspberrypi.org\nPin-Priority: 1001\n\n\
Package: python3-picamera2 python3-libcamera libcamera-apps\nPin: origin archive.raspberrypi.org\nPin-Priority: 1001\n" \
    > /etc/apt/preferences.d/raspi-libcamera.pref

# -------- Camera + GPIO/I2C/SPI/UART/PWM
RUN set -eux; \
  apt-get update && apt-get install -y --no-install-recommends \
    python3-picamera2 python3-libcamera libcamera-apps python3-numpy \
    v4l-utils i2c-tools \
    libjpeg-dev libatlas-base-dev \
    python3-rpi.gpio python3-gpiozero \
    python3-smbus python3-spidev python3-serial \
    pigpio python3-pigpio \
  && rm -rf /var/lib/apt/lists/*

# -------- Legacy SPI-Py (HAL needs it)
RUN set -eux; \
  git clone https://github.com/lthiery/SPI-Py.git /tmp/SPI-Py; \
  cd /tmp/SPI-Py && python3 setup.py install; \
  rm -rf /tmp/SPI-Py

# -------- App setup
WORKDIR /app
COPY requirements.txt /app/requirements.txt

# Install Python deps (skip hardware libs installed via apt)
RUN set -eux; \
  python3 -m pip install --no-cache-dir --upgrade pip; \
  (grep -vE '^(numpy|picamera2|RPi\.GPIO|smbus2|spidev)(==.*)?$' requirements.txt > req.txt || true); \
  if [ -s req.txt ]; then python3 -m pip install --no-cache-dir -r req.txt; fi

# Copy your source
COPY . /app

# Optional: folders your code expects
RUN set -eux; \
  mkdir -p /app/logs /app/data; \
  chmod +x /app/src/Main.py || true; \
  chmod +x /app/Main.py || true

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

# Start pigpio daemon, run hardware loop in background if present,
# then serve Flask via Gunicorn (auto-detect module path).
CMD bash -lc '\
  pigpiod || true; \
  if [ -f /app/src/Main.py ]; then python3 /app/src/Main.py & \
  elif [ -f /app/Main.py ]; then python3 /app/Main.py & fi; \
  if python3 -c "import importlib; importlib.import_module(\"src.App\")" 2>/dev/null; then \
      APP_MOD=src.App:app; \
  else \
      APP_MOD=App:app; \
  fi; \
  exec gunicorn -b 0.0.0.0:5000 "$APP_MOD" \
'
