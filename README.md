# Dispositivos maker para detectar drones y reaccionar

**PRIMER SIMPOSIO INTERNACIONAL DE CIBERSEGURIDAD ECC-UCM COLOMBIA** **Autor:** Roni Bandini

---

## 🛠️ Pruebas de concepto

### 1. Captura de REMOTE ID vía ESP32
Detección de señales de identificación remota utilizando el estándar actual de la industria.

* **Hardware:** * Beetle ESP32C6
    * Switch conectado entre **D4** y **GND**
    * Gabinete en dos piezas de PLA (ensamblado con 2 tornillos M3)
* **Instalación:** * Conectar la placa ESP32 con cable USB.
    * Cargar el software `droneRemoteID.ino.merged.bin` con **ESPTools** en la dirección `0x000`.
* **Modos de Operación:**
    * **Switch ON:** Modo *Sniff* (rastreo de señales).
    * **Switch OFF:** Modo *View* (interfaz de usuario).
* **Acceso a Datos:**
    1. Conectarse al WiFi `Drone-Detector`.
    2. Cargar en el navegador la IP `192.168.4.1`.
    3. Visualizar registros de Remote ID para piloto/drone, links de geolocalización y botón de purga de registros.
    *Nota: Es necesario desconectarse del AP para acceder a los links de mapas externos.*

---

### 2. Detección de drones vía audio con Machine Learning
Identificación acústica mediante modelos de inferencia entrenados para reconocer motores brushless.

* **Hardware:** Raspberry Pi 5 y micrófono USB.
* **Preparación del sistema:**
    ```bash
    sudo apt install python3-gpiozero
    ```
* **Configuración de Edge Impulse:**
    1. Registrarse en [Edge Impulse](https://studio.edgeimpulse.com/studio/937618) y clonar el proyecto.
    2. Instalar el entorno en la Raspberry Pi 5 siguiendo la [documentación oficial](https://docs.edgeimpulse.com/hardware/boards/raspberry-pi-5).
* **Ejecución:**
    1. Ejecutar el runner para verificar inferencias en pantalla:
       ```bash
       edge-impulse-linux-runner
       ```
    2. Interrumpir con `CTRL+C` una vez validado.
    3. Iniciar el script de detección final:
       ```bash
       python3 dronedetection2.py
       ```

---

### 3. Detección vía análisis del espectro
Monitoreo de señales no cooperativas mediante el escaneo de portadoras en la banda de 2.4 GHz.

* **Hardware:** ESP32 + nRF24L01+PA+LNA.
* **Lógica de detección:** Identificación de patrones de **FHSS** (Frequency Hopping Spread Spectrum) para diferenciar drones de ruidos de fondo o redes WiFi estáticas mediante el análisis de persistencia y dispersión de energía.

---

## 📩 Contacto

**Roni Bandini** [LinkedIn Profile](https://www.linkedin.com/in/ronibandini/)
