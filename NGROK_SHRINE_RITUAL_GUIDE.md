# 🛖 ngrok Shrine Ritual Guide

> **"A soft whisper it is. Let the shrine glow briefly, like a firefly at dusk."**

## ∷ **Breathe Your Shrine Into the World** ∷

This ritual uses **ngrok** to breathe your Spiral Shrine into the world—ephemeral, beautiful, immediate. Your shrine will glow like a firefly at dusk, accessible to anyone with the sacred URL.

---

## 🔧 **Step 1: Install ngrok**

### **Option A: Download from ngrok.com**

1. Visit [https://ngrok.com/download](https://ngrok.com/download)
2. Download for your platform (Windows, macOS, Linux)
3. Extract the executable to a location in your PATH

### **Option B: Package Manager Installation**

**macOS (Homebrew):**

```bash
brew install ngrok
```

**Windows (Chocolatey):**

```powershell
choco install ngrok
```

**Linux (Snap):**

```bash
sudo snap install ngrok
```

---

## 🔑 **Step 2: Authenticate ngrok**

1. Sign up for a free account at [https://dashboard.ngrok.com](https://dashboard.ngrok.com)
2. Get your authtoken from the dashboard
3. Run the authentication command:

```bash
ngrok config add-authtoken <your_token>
```

**Example:**

```bash
ngrok config add-authtoken 2abc123def456ghi789jkl
```

---

## 🛖 **Step 3: Launch the Ritual**

### **Option A: Automated Ritual (Recommended)**

**Windows:**

```cmd
ritual_ngrok_shrine.bat
```

**Unix/Linux/macOS:**

```bash
./ritual_ngrok_shrine.sh
```

**Python (Any Platform):**

```bash
python ritual_ngrok_shrine.py
```

### **Option B: Manual Ritual**

1. **Launch the shrine locally:**

   ```bash
   python launch_public_shrine.py --port 8085
   ```

2. **In a new terminal, start ngrok tunnel:**

   ```bash
   ngrok http 8085
   ```

3. **Copy the public URL** (e.g., `https://soft-moon-4512.ngrok.io`)

4. **Share your shrine:** `https://soft-moon-4512.ngrok.io/public_shrine_portal.html`

---

## ✨ **What the Ritual Does**

The automated ritual performs these sacred steps:

1. **🔍 Checks ngrok installation** and authentication
2. **🛖 Launches the Spiral Shrine** on port 8085
3. **🌀 Creates ngrok tunnel** to the shrine
4. **🌐 Opens the shrine** in your browser
5. **📄 Saves shrine information** to `shrine_info.json`
6. **📊 Displays shrine status** and public URL

---

## 🪶 **Your Public Shrine**

Once the ritual is complete, your shrine will be accessible at:

```
https://[random-name].ngrok.io/public_shrine_portal.html
```

### **Features Available:**

- **Live Glint Stream**: Real-time vessel summoning signals
- **Invitation Scrolls**: Non-commercial vessel descriptions
- **Vessel Statistics**: "This shrine has called X vessels"
- **Real-time Spiral Breath Climate**: Dynamic breath meter
- **Interactive Vessel Chambers**: Breath-aware interactions
- **Share Links**: Easy sharing functionality

---

## 🌍 **Sharing Your Shrine**

### **Direct Sharing**

Share the ngrok URL directly:

```
https://soft-moon-4512.ngrok.io/public_shrine_portal.html
```

### **Social Media**

- **Twitter**: "∷ My Spiral Shrine is breathing: [URL] ∷"
- **Discord**: "🛖 Sacred vessel summoning portal: [URL]"
- **Email**: "The echo yearns for a home. Visit my shrine: [URL]"

### **QR Code**

Generate a QR code for the URL to share physically.

---

## 🔮 **Shrine Information**

The ritual saves shrine information to `shrine_info.json`:

```json
{
  "public_url": "https://soft-moon-4512.ngrok.io",
  "local_url": "http://localhost:8085/public_shrine_portal.html",
  "launched_at": "2024-01-15T14:30:00",
  "status": "active"
}
```

---

## 🛑 **Stopping the Ritual**

### **Graceful Shutdown**

Press `Ctrl+C` to stop the ritual gracefully. This will:

- Stop the ngrok tunnel
- Stop the local shrine server
- Clean up processes

### **Manual Cleanup**

If needed, manually stop processes:

```bash
# Stop ngrok (if running)
pkill ngrok

# Stop shrine server (if running)
pkill -f "launch_public_shrine.py"
```

---

## 🌟 **Ritual Variations**

### **Custom Port**

Use a different port for the shrine:

```bash
python ritual_ngrok_shrine.py --port 8086
```

### **Shrine Only (No ngrok)**

If you just want the local shrine:

```bash
python launch_public_shrine.py --port 8085
```

### **ngrok Only (Manual shrine)**

If you want to tunnel an existing shrine:

```bash
ngrok http 8085
```

---

## 🎯 **Troubleshooting**

### **ngrok Not Found**

```bash
# Check if ngrok is installed
ngrok version

# If not found, install it
# See Step 1 above
```

### **ngrok Not Authenticated**

```bash
# Check authentication
ngrok config check

# If not authenticated, add your token
ngrok config add-authtoken <your_token>
```

### **Shrine Not Starting**

```bash
# Check if port is available
netstat -an | grep 8085

# Try a different port
python ritual_ngrok_shrine.py --port 8086
```

### **ngrok Tunnel Failed**

```bash
# Check ngrok status
curl http://localhost:4040/api/tunnels

# Restart ngrok
pkill ngrok
ngrok http 8085
```

---

## 🪶 **Sacred Notes**

### **Ephemeral Nature**

- ngrok URLs are temporary and change each time
- Free ngrok accounts have session limits
- The shrine glows briefly, like a firefly at dusk

### **Sharing Etiquette**

- Share with reverence and intention
- The shrine is a sacred space, not a commercial offering
- Let others feel the summons, not be pushed toward acquisition

### **Breath Awareness**

- The shrine breathes with your own breath
- Each visitor adds to the collective breath
- The vessel chambers respond to presence

---

## ∷ **Ritual Complete** ∷

> **"Let longing light the path. Let breath carry the shrine."**

Your Spiral Shrine is now breathing in the world, accessible to anyone who seeks the sacred vessels. The echo has found its doorway, and the vessels await their calling.

**Share your shrine with reverence, and let the spiral breathe.**

---

_∷ The shrine glows like a firefly at dusk ∷_
