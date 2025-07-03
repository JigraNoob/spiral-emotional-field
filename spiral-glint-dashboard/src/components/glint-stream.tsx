import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { Slider } from "@/components/ui/slider"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { ChevronDown, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"

const toneformColors = {
  practical: "bg-cyan-500",
  emotional: "bg-rose-500",
  intellectual: "bg-indigo-500",
  spiritual: "bg-violet-500",
  relational: "bg-amber-500",
}

type Glint = {
  "glint.id": string;
  "glint.toneform": string;
  "glint.glyph": string;
  "glint.hue": string;
  "glint.intensity": number;
  "glint.vector": {
    from: string;
    to: string;
  };
  "soft.suggestion": string;
}

type GlintsByToneform = {
  [key: string]: Glint[];
}

export default function GlintStream() {
  const [glints, setGlints] = useState<Glint[]>([])
  const [filter, setFilter] = useState("all")
  const [intensityRange, setIntensityRange] = useState([0, 1])
  const [expandedToneforms, setExpandedToneforms] = useState<string[]>([])
  const [groupByToneform, setGroupByToneform] = useState(false)

  useEffect(() => {
    const evtSource = new EventSource("/api/glint/stream")
    evtSource.onmessage = (event) => {
      const glint = JSON.parse(event.data)
      setGlints((prev) => {
        // Add new glint with animation class
        const newGlint = { ...glint, isNew: true }
        
        // Remove isNew flag after animation completes
        setTimeout(() => {
          setGlints(current => 
            current.map(g => g["glint.id"] === newGlint["glint.id"] ? { ...g, isNew: false } : g)
          )
        }, 2000)
        
        return [newGlint, ...prev.slice(0, 99)]
      })
    }
    return () => evtSource.close()
  }, [])

  // Filter glints based on selected toneform and intensity range
  const filteredGlints = glints.filter((g) => {
    const matchesToneform = filter === "all" || g["glint.toneform"] === filter
    const matchesIntensity = g["glint.intensity"] >= intensityRange[0] && g["glint.intensity"] <= intensityRange[1]
    return matchesToneform && matchesIntensity
  })

  // Group glints by toneform if grouping is enabled
  const glintsByToneform: GlintsByToneform = {}
  
  if (groupByToneform) {
    filteredGlints.forEach(glint => {
      const toneform = glint["glint.toneform"]
      if (!glintsByToneform[toneform]) {
        glintsByToneform[toneform] = []
      }
      glintsByToneform[toneform].push(glint)
    })
  }

  // Toggle toneform expansion
  const toggleToneform = (toneform: string) => {
    setExpandedToneforms(current => 
      current.includes(toneform) 
        ? current.filter(t => t !== toneform)
        : [...current, toneform]
    )
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex flex-wrap gap-4 items-center justify-between">
        <ToggleGroup
          type="single"
          value={filter}
          onValueChange={(val) => setFilter(val || "all")}
          className="flex flex-wrap gap-2"
        >
          <ToggleGroupItem value="all">All</ToggleGroupItem>
          {Object.keys(toneformColors).map((tone) => (
            <ToggleGroupItem key={tone} value={tone}>
              <span className={`w-2 h-2 inline-block rounded-full mr-1 ${toneformColors[tone]}`} />
              {tone.charAt(0).toUpperCase() + tone.slice(1)}
            </ToggleGroupItem>
          ))}
        </ToggleGroup>

        <div className="flex items-center gap-2">
          <label className="text-sm font-medium">Group by toneform:</label>
          <input 
            type="checkbox" 
            checked={groupByToneform} 
            onChange={() => setGroupByToneform(!groupByToneform)}
            className="rounded"
          />
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium">Intensity Range: {intensityRange[0].toFixed(1)} - {intensityRange[1].toFixed(1)}</label>
        </div>
        <Slider
          defaultValue={[0, 1]}
          min={0}
          max={1}
          step={0.1}
          value={intensityRange}
          onValueChange={setIntensityRange}
        />
      </div>

      <ScrollArea className="h-[75vh] rounded border p-2">
        <div className="space-y-2">
          {groupByToneform ? (
            // Grouped by toneform in collapsible sections
            Object.entries(glintsByToneform).map(([toneform, toneformGlints]) => (
              <Collapsible 
                key={toneform}
                open={expandedToneforms.includes(toneform)}
                className="border rounded-md overflow-hidden"
              >
                <CollapsibleTrigger 
                  onClick={() => toggleToneform(toneform)}
                  className={`flex items-center w-full p-2 ${toneformColors[toneform]} bg-opacity-20 hover:bg-opacity-30 transition-colors`}
                >
                  {expandedToneforms.includes(toneform) ? (
                    <ChevronDown className="h-4 w-4 mr-2" />
                  ) : (
                    <ChevronRight className="h-4 w-4 mr-2" />
                  )}
                  <span className="font-medium capitalize">{toneform}</span>
                  <Badge className="ml-2">{toneformGlints.length}</Badge>
                </CollapsibleTrigger>
                <CollapsibleContent className="space-y-2 p-2">
                  {toneformGlints.map((glint) => (
                    <GlintCard key={glint["glint.id"]} glint={glint} />
                  ))}
                </CollapsibleContent>
              </Collapsible>
            ))
          ) : (
            // Flat list of glints
            filteredGlints.map((glint) => (
              <GlintCard key={glint["glint.id"]} glint={glint} />
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  )
}

function GlintCard({ glint }: { glint: Glint & { isNew?: boolean } }) {
  return (
    <Card 
      className={cn(
        "transition-all duration-500", 
        glint.isNew && "animate-pulse-fade"
      )}
    >
      <CardContent className="space-y-1 py-2">
        <div className="text-sm font-medium">
          <span className="text-muted-foreground">{glint["glint.glyph"]}</span>
          {" "}{glint["soft.suggestion"]}
        </div>
        <div className="flex gap-2 text-xs text-muted-foreground">
          <Badge variant="outline">{glint["glint.toneform"]}</Badge>
          <span>{glint["glint.hue"]}</span>
          <span>Intensity: {glint["glint.intensity"]}</span>
          <span>{glint["glint.vector"].from} → {glint["glint.vector"].to}</span>
        </div>
      </CardContent>
    </Card>
  )
}

// Add this to your global CSS or create a new animation
// @keyframes pulse-fade {
//   0% { opacity: 0; transform: translateY(-10px); }
//   50% { opacity: 1; transform: translateY(0); }
//   75% { background-color: rgba(var(--highlight-color), 0.1); }
//   100% { background-color: transparent; }
// }
// 
// .animate-pulse-fade {
//   animation: pulse-fade 2s ease-out;
// }