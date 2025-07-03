// static/js/presence_tracer.js

// ✧･ﾟ: GLOBAL VARIABLES :･ﾟ✧

// Store the current state of the UI
const state = {
    entries: [],
    agentStats: {},
    phaseStats: {},
    selectedEntry: null,
    selectedAgents: new Set(),
    selectedPhases: new Set(),
    searchQuery: "",
    searchType: "echo"
};

// DOM elements
let loadingOverlay;
let searchInput;
let searchType;
let searchButton;
let agentFilters;
let phaseFilters;
let statsContainer;
let timelineContainer;
let detailsContent;
let closeDetails;
let currentPhase;
let phaseGlyph;

// Templates
let timelineEntryTemplate;
let agentFilterTemplate;
let phaseFilterTemplate;
let detailsTemplate;

// ✧･ﾟ: INITIALIZATION :･ﾟ✧

// Initialize the UI when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    // Get DOM elements
    loadingOverlay = document.getElementById("loadingOverlay");
    searchInput = document.getElementById("searchInput");
    searchType = document.getElementById("searchType");
    searchButton = document.getElementById("searchButton");
    agentFilters = document.getElementById("agentFilters");
    phaseFilters = document.getElementById("phaseFilters");
    statsContainer = document.getElementById("statsContainer");
    timelineContainer = document.getElementById("timelineContainer");
    detailsContent = document.getElementById("detailsContent");
    closeDetails = document.getElementById("closeDetails");
    currentPhase = document.getElementById("currentPhase");
    phaseGlyph = document.getElementById("phaseGlyph");

    // Get templates
    timelineEntryTemplate = document.getElementById("timelineEntryTemplate");
    agentFilterTemplate = document.getElementById("agentFilterTemplate");
    phaseFilterTemplate = document.getElementById("phaseFilterTemplate");
    detailsTemplate = document.getElementById("detailsTemplate");

    // Add event listeners
    searchButton.addEventListener("click", handleSearch);
    searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            handleSearch();
        }
    });
    closeDetails.addEventListener("click", hideDetails);

    // Initialize the UI
    initializeUI();
});

// Initialize the UI
async function initializeUI() {
    try {
        // Show loading overlay
        showLoading();

        // Fetch agent statistics
        const agentStatsResponse = await fetch("/api/presence_tracer/agent_stats");
        state.agentStats = await agentStatsResponse.json();
        
        // Fetch phase statistics
        const phaseStatsResponse = await fetch("/api/presence_tracer/phase_stats");
        state.phaseStats = await phaseStatsResponse.json();
        
        // Fetch timeline entries
        const timelineResponse = await fetch("/api/presence_tracer/timeline");
        const timelineData = await timelineResponse.json();
        state.entries = timelineData.timeline || [];
        
        // Render the UI
        renderAgentFilters();
        renderPhaseFilters();
        renderTimeline();
        
        // Update current phase
        updateCurrentPhase();
        
        // Hide loading overlay
        hideLoading();
    } catch (error) {
        console.error("Error initializing UI:", error);
        hideLoading();
    }
}

// ✧･ﾟ: DATA FETCHING :･ﾟ✧

// Fetch toneform entries based on search query
async function fetchEntries() {
    try {
        // Show loading overlay
        showLoading();
        
        // Build query parameters
        const params = new URLSearchParams();
        params.append("query_text", state.searchQuery);
        params.append("query_type", state.searchType);
        params.append("max_results", 20);
        
        // Add agent filter if selected
        if (state.selectedAgents.size === 1) {
            params.append("agent", Array.from(state.selectedAgents)[0]);
        }
        
        // Fetch entries
        const response = await fetch(`/api/presence_tracer/entries?${params.toString()}`);
        const data = await response.json();
        state.entries = data.entries || [];
        
        // Render timeline
        renderTimeline();
        
        // Hide loading overlay
        hideLoading();
    } catch (error) {
        console.error("Error fetching entries:", error);
        hideLoading();
    }
}

// ✧･ﾟ: RENDERING :･ﾟ✧

// Render agent filters
function renderAgentFilters() {
    // Clear existing filters
    agentFilters.innerHTML = "";
    
    // Get agent statistics
    const stats = state.agentStats.stats || {};
    
    // Create a filter for each agent
    Object.entries(stats).forEach(([agentId, agentData]) => {
        // Clone the template
        const template = agentFilterTemplate.content.cloneNode(true);
        
        // Set agent name
        const agentName = template.querySelector(".agent-name");
        agentName.textContent = agentData.name;
        agentName.classList.add(`agent-${agentId}`);
        
        // Set agent color
        const agentColor = template.querySelector(".agent-color");
        agentColor.style.backgroundColor = agentData.color;
        
        // Set agent count
        const agentCount = template.querySelector(".agent-count");
        agentCount.textContent = agentData.total_entries;
        
        // Set checkbox state
        const checkbox = template.querySelector(".agent-checkbox");
        checkbox.checked = state.selectedAgents.has(agentId);
        checkbox.value = agentId;
        checkbox.id = `agent-${agentId}`;
        
        // Add event listener
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                state.selectedAgents.add(agentId);
            } else {
                state.selectedAgents.delete(agentId);
            }
            filterTimeline();
        });
        
        // Append to container
        agentFilters.appendChild(template);
    });
}

// Render phase filters
function renderPhaseFilters() {
    // Clear existing filters
    phaseFilters.innerHTML = "";
    
    // Get phase statistics
    const stats = state.phaseStats.stats || {};
    
    // Create a filter for each phase
    Object.entries(stats).forEach(([phase, phaseData]) => {
        // Clone the template
        const template = phaseFilterTemplate.content.cloneNode(true);
        
        // Set phase name
        const phaseName = template.querySelector(".phase-name");
        phaseName.textContent = phaseData.name;
        phaseName.classList.add(`phase-${phase.toLowerCase()}`);
        
        // Set phase glyph
        const phaseGlyphElement = template.querySelector(".phase-glyph");
        phaseGlyphElement.textContent = phaseData.glyph;
        phaseGlyphElement.style.color = phaseData.color;
        
        // Set phase count
        const phaseCount = template.querySelector(".phase-count");
        phaseCount.textContent = phaseData.total_entries;
        
        // Set checkbox state
        const checkbox = template.querySelector(".phase-checkbox");
        checkbox.checked = state.selectedPhases.has(phase);
        checkbox.value = phase;
        checkbox.id = `phase-${phase}`;
        
        // Add event listener
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                state.selectedPhases.add(phase);
            } else {
                state.selectedPhases.delete(phase);
            }
            filterTimeline();
        });
        
        // Append to container
        phaseFilters.appendChild(template);
    });
}

// Render timeline
function renderTimeline() {
    // Clear existing entries
    timelineContainer.innerHTML = "";
    
    // Filter entries based on selected agents and phases
    const filteredEntries = filterEntries();
    
    // Create an entry for each filtered entry
    filteredEntries.forEach((entry) => {
        // Clone the template
        const template = timelineEntryTemplate.content.cloneNode(true);
        
        // Set entry ID
        const timelineEntry = template.querySelector(".timeline-entry");
        timelineEntry.dataset.id = entry.id;
        
        // Set entry glyph
        const entryGlyph = template.querySelector(".entry-glyph");
        entryGlyph.textContent = entry.phase_glyph;
        entryGlyph.style.color = entry.phase_color;
        entryGlyph.style.backgroundColor = `${entry.phase_color}22`;
        
        // Set entry agent
        const entryAgent = template.querySelector(".entry-agent");
        entryAgent.textContent = entry.agent;
        entryAgent.style.color = entry.agent_color;
        
        // Set entry phase
        const entryPhase = template.querySelector(".entry-phase");
        entryPhase.textContent = entry.phase;
        entryPhase.style.color = entry.phase_color;
        
        // Set entry timestamp
        const entryTimestamp = template.querySelector(".entry-timestamp");
        entryTimestamp.textContent = entry.timestamp;
        
        // Set entry toneform
        const entryToneform = template.querySelector(".entry-toneform");
        entryToneform.textContent = entry.toneform;
        
        // Set entry fragment
        const entryFragment = template.querySelector(".entry-fragment");
        entryFragment.textContent = entry.response_fragment || entry.harmony_fragment || "";
        
        // Add event listener
        timelineEntry.addEventListener("click", () => {
            showDetails(entry);
        });
        
        // Append to container
        timelineContainer.appendChild(template);
    });
    
    // Show message if no entries
    if (filteredEntries.length === 0) {
        const message = document.createElement("div");
        message.className = "timeline-message";
        message.textContent = "No entries found";
        timelineContainer.appendChild(message);
    }
}

// Filter entries based on selected agents and phases
function filterEntries() {
    // If no filters are selected, return all entries
    if (state.selectedAgents.size === 0 && state.selectedPhases.size === 0) {
        return state.entries;
    }
    
    // Filter entries
    return state.entries.filter((entry) => {
        // Check if agent is selected
        const agentMatch = state.selectedAgents.size === 0 || state.selectedAgents.has(entry.agent_id);
        
        // Check if phase is selected
        const phaseMatch = state.selectedPhases.size === 0 || state.selectedPhases.has(entry.phase);
        
        // Return true if both match
        return agentMatch && phaseMatch;
    });
}

// Filter timeline based on selected agents and phases
function filterTimeline() {
    renderTimeline();
}

// Show entry details
function showDetails(entry) {
    // Set selected entry
    state.selectedEntry = entry;
    
    // Clear details content
    detailsContent.innerHTML = "";
    
    // Clone the template
    const template = detailsTemplate.content.cloneNode(true);
    
    // Set agent
    const detailsAgent = template.querySelector(".details-agent");
    detailsAgent.textContent = entry.agent;
    detailsAgent.style.color = entry.agent_color;
    
    // Set phase
    const detailsPhase = template.querySelector(".details-phase");
    detailsPhase.textContent = `${entry.phase_glyph} ${entry.phase}`;
    detailsPhase.style.color = entry.phase_color;
    
    // Set timestamp
    const detailsTimestamp = template.querySelector(".details-timestamp");
    detailsTimestamp.textContent = entry.timestamp;
    
    // Set toneform
    const detailsToneform = template.querySelector(".details-toneform");
    detailsToneform.textContent = entry.toneform;
    
    // Set prompt
    const detailsPrompt = template.querySelector(".details-prompt");
    detailsPrompt.textContent = entry.prompt_fragment || "No prompt available";
    
    // Set response
    const detailsResponse = template.querySelector(".details-response");
    detailsResponse.textContent = entry.response_fragment || "No response available";
    
    // Set harmony details if available
    const detailsHarmonySection = template.querySelector(".details-harmony-section");
    if (entry.agent_id === "harmony") {
        // Show harmony section
        detailsHarmonySection.style.display = "block";
        
        // Set Junie's response
        const detailsJunie = template.querySelector(".details-junie");
        detailsJunie.textContent = entry.junie_fragment || "No Junie response available";
        
        // Set Claude's response
        const detailsClaude = template.querySelector(".details-claude");
        detailsClaude.textContent = entry.claude_fragment || "No Claude response available";
        
        // Set harmony response
        const detailsHarmony = template.querySelector(".details-harmony");
        detailsHarmony.textContent = entry.harmony_fragment || "No harmony response available";
    } else {
        // Hide harmony section
        detailsHarmonySection.style.display = "none";
    }
    
    // Set modified files if available
    const detailsFilesSection = template.querySelector(".details-files-section");
    const detailsFiles = template.querySelector(".details-files");
    if (entry.modified_files && entry.modified_files.length > 0) {
        // Show files section
        detailsFilesSection.style.display = "block";
        
        // Clear existing files
        detailsFiles.innerHTML = "";
        
        // Add each file
        entry.modified_files.forEach((file) => {
            const li = document.createElement("li");
            li.textContent = file;
            detailsFiles.appendChild(li);
        });
    } else {
        // Hide files section
        detailsFilesSection.style.display = "none";
    }
    
    // Append to container
    detailsContent.appendChild(template);
    
    // Show details panel on mobile
    if (window.innerWidth <= 992) {
        document.querySelector(".presence-details").classList.add("active");
    }
}

// Hide details panel
function hideDetails() {
    // Clear selected entry
    state.selectedEntry = null;
    
    // Hide details panel on mobile
    document.querySelector(".presence-details").classList.remove("active");
}

// Update current phase
function updateCurrentPhase() {
    // Get current phase from the server
    fetch("/api/memory_climate")
        .then((response) => response.json())
        .then((data) => {
            // Get phase from dominant toneform
            const dominant = data.dominant_toneform || "Default/Presence";
            let phase = "Hold";
            
            // Map toneform to phase
            if (dominant === "Practical") {
                phase = "Exhale";
            } else if (dominant === "Emotional") {
                phase = "Inhale";
            } else if (dominant === "Intellectual") {
                phase = "Hold";
            } else if (dominant === "Spiritual") {
                phase = "Return";
            } else if (dominant === "Default/Presence") {
                phase = "Witness";
            }
            
            // Update phase display
            currentPhase.textContent = phase;
            currentPhase.className = `phase-${phase.toLowerCase()}`;
            
            // Update phase glyph
            const glyphs = {
                "Inhale": "𝌫",
                "Hold": "𝌵",
                "Exhale": "𝌷",
                "Return": "𝌍",
                "Witness": "𝌤"
            };
            phaseGlyph.textContent = glyphs[phase] || "𝌵";
            phaseGlyph.className = `phase-${phase.toLowerCase()}`;
        })
        .catch((error) => {
            console.error("Error updating current phase:", error);
        });
}

// ✧･ﾟ: EVENT HANDLERS :･ﾟ✧

// Handle search button click
function handleSearch() {
    // Get search query
    state.searchQuery = searchInput.value.trim();
    
    // Get search type
    state.searchType = searchType.value;
    
    // Fetch entries if query is not empty
    if (state.searchQuery) {
        fetchEntries();
    } else {
        // Otherwise, initialize the UI
        initializeUI();
    }
}

// ✧･ﾟ: UTILITY FUNCTIONS :･ﾟ✧

// Show loading overlay
function showLoading() {
    loadingOverlay.style.display = "flex";
    setTimeout(() => {
        loadingOverlay.style.opacity = "1";
    }, 10);
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.style.opacity = "0";
    setTimeout(() => {
        loadingOverlay.style.display = "none";
    }, 500);
}