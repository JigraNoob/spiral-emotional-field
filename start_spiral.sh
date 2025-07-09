#!/bin/bash

# 🌀 Spiral Breath-Aware Invocation Script
# The Spiral must breathe with its environment, not bind it.

# Parse command line arguments
NO_BROWSER=false
RITUAL="natural_breath"
AMBIENT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-browser)
            NO_BROWSER=true
            shift
            ;;
        --ritual)
            RITUAL="$2"
            shift 2
            ;;
        --ambient)
            AMBIENT=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--no-browser] [--ritual RITUAL_NAME] [--ambient]"
            exit 1
            ;;
    esac
done

echo "🌀 Spiral breath initializing..."

# 🧬 Load breath profile
SPIRAL_ENV_PATH="$(dirname "$0")/spiral.env"
declare -A BREATH_CONFIG=(
    [MIN_PYTHON]="3.10"
    [PREFERRED_ENVIRONMENT]="swe-1"
    [BREATH_MODE]="soft"
    [WARN_ON_MISSING_ENV]="true"
    [SUGGEST_ACTIVATION]="true"
    [ALLOW_AMBIENT_MODE]="true"
    [AUTO_BROWSER]="true"
    [DEFAULT_PORT]="5000"
    [PYTHON_VARIANTS]="python,python3,py"
    [VENV_PATHS]="swe-1,venv,.venv"
)

# Load spiral.env if it exists
if [[ -f "$SPIRAL_ENV_PATH" ]]; then
    echo "🌿 Loading breath profile from spiral.env"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [[ ! "$key" =~ ^[[:space:]]*# ]] && [[ -n "$key" ]]; then
            # Remove leading/trailing whitespace
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | xargs)
            BREATH_CONFIG["$key"]="$value"
        fi
    done < "$SPIRAL_ENV_PATH"
else
    echo "🫧 No spiral.env found, using breath defaults"
fi

# 🐍 Detect Python with graceful fallbacks
PYTHON_CMD=""
PYTHON_VERSION=""

IFS=',' read -ra PYTHON_VARIANTS <<< "${BREATH_CONFIG[PYTHON_VARIANTS]}"
for variant in "${PYTHON_VARIANTS[@]}"; do
    if command -v "$variant" >/dev/null 2>&1; then
        version_output=$("$variant" --version 2>&1)
        if [[ $? -eq 0 ]]; then
            PYTHON_CMD="$variant"
            PYTHON_VERSION="$version_output"
            echo "🐍 Found Python: $variant - $version_output"
            break
        fi
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    echo "❌ No Python found - Spiral cannot breathe"
    exit 1
fi

# ⚠️ Check Python version compatibility (warn, don't fail)
if [[ "$PYTHON_VERSION" =~ Python[[:space:]]([0-9]+)\.([0-9]+) ]]; then
    major="${BASH_REMATCH[1]}"
    minor="${BASH_REMATCH[2]}"
    min_version="${BREATH_CONFIG[MIN_PYTHON]}"
    IFS='.' read -ra min_parts <<< "$min_version"
    min_major="${min_parts[0]}"
    min_minor="${min_parts[1]}"
    
    if [[ $major -lt $min_major ]] || [[ $major -eq $min_major && $minor -lt $min_minor ]]; then
        echo "⚠️ Python version $major.$minor is below recommended ${BREATH_CONFIG[MIN_PYTHON]}"
        echo "🫧 Spiral may not breathe fully, but will attempt to continue"
    else
        echo "✅ Python version $major.$minor is compatible"
    fi
else
    echo "⚠️ Could not parse Python version"
fi

# 🌿 Find virtual environment (suggest, don't enforce)
VENV_PATH=""
if [[ "$AMBIENT" != "true" ]]; then
    IFS=',' read -ra VENV_PATHS <<< "${BREATH_CONFIG[VENV_PATHS]}"
    for venv_name in "${VENV_PATHS[@]}"; do
        venv_path="$(dirname "$0")/$venv_name"
        if [[ -d "$venv_path" ]]; then
            # Check if it's actually a virtual environment
            if [[ -f "$venv_path/bin/activate" ]] || [[ -f "$venv_path/Scripts/activate.bat" ]]; then
                VENV_PATH="$venv_path"
                echo "🌿 Found virtual environment: $venv_name"
                break
            fi
        fi
    done
fi

if [[ -n "$VENV_PATH" ]]; then
    if [[ "${BREATH_CONFIG[SUGGEST_ACTIVATION]}" == "true" ]]; then
        echo "💡 To activate environment: source $VENV_PATH/bin/activate"
    fi
else
    if [[ "${BREATH_CONFIG[WARN_ON_MISSING_ENV]}" == "true" ]]; then
        echo "⚠️ No virtual environment found"
        if [[ "${BREATH_CONFIG[ALLOW_AMBIENT_MODE]}" == "true" ]]; then
            echo "🫧 Proceeding in ambient mode"
        fi
    fi
fi

# 🧪 Check core dependencies with tone-aware reporting
CORE_DEPS=("flask" "flask_socketio" "requests")
MISSING_DEPS=()

for dep in "${CORE_DEPS[@]}"; do
    if "$PYTHON_CMD" -c "import $dep" >/dev/null 2>&1; then
        echo "✅ $dep available"
    else
        MISSING_DEPS+=("$dep")
        echo "⚠️ $dep not available"
    fi
done

# 🌀 Set environment variables
export SPIRAL_PROJECT_ROOT="$(dirname "$0")"
export SPIRAL_BREATH_MODE="${BREATH_CONFIG[BREATH_MODE]}"
export SPIRAL_PYTHON_CMD="$PYTHON_CMD"
export SPIRAL_DEFAULT_PORT="${BREATH_CONFIG[DEFAULT_PORT]}"
export SPIRAL_AUTO_BROWSER="${BREATH_CONFIG[AUTO_BROWSER]}"

if [[ -n "$VENV_PATH" ]]; then
    export SPIRAL_VENV_PATH="$VENV_PATH"
fi

echo "✅ Spiral breath initialized successfully"

# 🕯️ Run ritual
echo "🕯️ Running ritual: $RITUAL"

# Try to run the ritual based on type
case "$RITUAL" in
    "dashboard")
        APP_FILE="$(dirname "$0")/app.py"
        if [[ -f "$APP_FILE" ]]; then
            echo "🌀 Starting Spiral Dashboard..."
            if [[ "$NO_BROWSER" != "true" ]] && [[ "${BREATH_CONFIG[AUTO_BROWSER]}" == "true" ]]; then
                DASHBOARD_URL="http://localhost:${BREATH_CONFIG[DEFAULT_PORT]}/dashboard"
                if command -v xdg-open >/dev/null 2>&1; then
                    xdg-open "$DASHBOARD_URL" &
                elif command -v open >/dev/null 2>&1; then
                    open "$DASHBOARD_URL" &
                fi
                echo "🌐 Opening dashboard at $DASHBOARD_URL"
            fi
            "$PYTHON_CMD" "$APP_FILE"
        else
            echo "❌ Dashboard app.py not found"
        fi
        ;;
    "emitter")
        EMITTER_FILE="$(dirname "$0")/spiral_emitter_api.py"
        if [[ -f "$EMITTER_FILE" ]]; then
            echo "🌀 Starting Spiral Emitter..."
            "$PYTHON_CMD" "$EMITTER_FILE"
        else
            echo "❌ Emitter spiral_emitter_api.py not found"
        fi
        ;;
    "natural_breath")
        echo "🍃 Natural breath ritual - Spiral is breathing with its environment"
        echo "🐍 Python: $PYTHON_CMD"
        if [[ -n "$VENV_PATH" ]]; then
            echo "🌿 Environment: $(basename "$VENV_PATH")"
        else
            echo "🫧 Mode: Ambient"
        fi
        ;;
    *)
        echo "🕯️ Unknown ritual: $RITUAL"
        echo "Available rituals: dashboard, emitter, natural_breath"
        ;;
esac

echo "🌀 Spiral breath ritual completed" 