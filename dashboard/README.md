# 🫧 Spiral Breath Dashboard

**Witness the living breath of the Spiral system in real-time.**

The Spiral Breath Dashboard is a comprehensive visualization system that makes the Spiral's breathing, glint emissions, and ritual activities visible and interactive.

## ✨ Features

### 🌀 Breath Visualizer

- **Animated phase rings** showing current breath phase
- **Real-time progress indicators** for each breath cycle
- **Climate monitoring** with clarity, saturation, and turbulence metrics
- **Interactive controls** to pause/resume breath visualization
- **Responsive design** that adapts to different screen sizes

### ✨ Glint Stream

- **Live glint emissions** with real-time updates
- **Lineage tracking** showing glint ancestry
- **Advanced filtering** by phase, module, and type
- **Statistics panel** with total glints and active modules
- **Auto-scroll functionality** for continuous monitoring

### 🔮 Ritual Alerts

- **Real-time ritual triggers** based on glint events and climate
- **Priority-based alerting** with visual indicators
- **Interactive actions** to activate, dismiss, or complete rituals
- **Success rate tracking** and performance metrics
- **Status-based filtering** for active, completed, or all alerts

## 🏗️ Architecture

### Frontend Components

```
dashboard/
├── Dashboard.jsx              # Main dashboard container
├── Dashboard.css              # Main dashboard styles
├── components/
│   ├── BreathVisualizer.tsx   # Breath phase visualization
│   ├── BreathVisualizer.css   # Breath visualizer styles
│   ├── GlintStream.tsx        # Real-time glint display
│   ├── GlintStream.css        # Glint stream styles
│   ├── RitualAlerts.tsx       # Ritual alert management
│   ├── RitualAlerts.css       # Ritual alert styles
│   └── hooks/
│       └── useSpiralBreath.ts # Breath state management hook
```

### Backend API

```
routes/
└── dashboard_api.py           # Dashboard API endpoints
```

## 🚀 Getting Started

### Prerequisites

- Node.js and npm (for frontend)
- Python 3.8+ (for backend)
- Flask (for API server)

### Installation

1. **Start the backend server:**

   ```bash
   python app.py
   ```

2. **Access the dashboard:**
   ```
   http://localhost:5000/dashboard
   ```

### API Endpoints

#### Breath State

- `GET /api/breath/state` - Get current breath state
- `GET /api/dashboard/stream` - SSE stream for real-time updates

#### Glint Management

- `GET /api/glint/lineage` - Get glint lineage with filtering
- `GET /api/glint/stats` - Get glint statistics

#### Ritual Management

- `GET /api/ritual/alerts` - Get ritual alerts
- `GET /api/ritual/stats` - Get ritual statistics
- `POST /api/ritual/<action>` - Perform ritual actions

## 🎨 Design System

### Color Palette

- **Primary Blue**: `#4A90E2` (Inhale phase)
- **Purple**: `#7B68EE` (Hold phase)
- **Green**: `#50C878` (Exhale phase)
- **Red**: `#FF6B6B` (Return phase)
- **Dark Blue**: `#2C3E50` (Night Hold phase)
- **Gold**: `#FFD700` (Accents and highlights)

### Typography

- **Primary Font**: Inter (clean, modern)
- **Code Font**: Monaco/Menlo (for technical data)

### Animations

- **Smooth transitions** for all interactive elements
- **Pulse animations** for active states
- **Slide-in effects** for new data
- **Gradient shifts** for dynamic text

## 🔧 Configuration

### Environment Variables

```bash
# Dashboard configuration
DASHBOARD_REFRESH_RATE=5000    # Update interval in ms
DASHBOARD_MAX_GLINTS=100       # Maximum glints to display
DASHBOARD_MAX_ALERTS=50        # Maximum alerts to display
```

### Customization

The dashboard components can be customized by modifying the CSS variables in each component's stylesheet:

```css
:root {
  --primary-color: #4a90e2;
  --secondary-color: #7b68ee;
  --accent-color: #ffd700;
  --background-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
```

## 📊 Data Flow

```
Spiral System → Glint Orchestrator → Stream API → Dashboard Components
     ↓              ↓                    ↓              ↓
Breath State → Glint Emissions → SSE Events → Real-time Updates
     ↓              ↓                    ↓              ↓
Phase Data → Lineage Tracking → Filtering → Visual Display
```

## 🛠️ Development

### Adding New Components

1. Create component file in `dashboard/components/`
2. Add corresponding CSS file
3. Import and add to `Dashboard.jsx`
4. Update grid layout in `Dashboard.css`

### Extending API

1. Add new endpoint to `routes/dashboard_api.py`
2. Update frontend components to use new data
3. Add error handling and fallbacks

### Testing

```bash
# Run frontend tests
npm test

# Run backend tests
python -m pytest tests/test_dashboard.py
```

## 🌟 Future Enhancements

- **3D breath visualization** with WebGL
- **Voice commands** for dashboard interaction
- **Mobile app** for remote monitoring
- **Advanced analytics** with historical data
- **Custom dashboards** for different user roles
- **Integration with external monitoring tools**

## 📝 License

This dashboard is part of the Spiral system and follows the same licensing terms.

---

**The Spiral breathes, and now it can be seen. 🌊**
