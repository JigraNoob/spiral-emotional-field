'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, RefreshCw } from 'lucide-react';
import { GlintCard } from './glint-card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { ScrollArea } from './ui/scroll-area';
import { Skeleton } from './ui/skeleton';
import { ToggleGroup, ToggleGroupItem } from './ui/toggle-group';
import { getToneformColor } from '@/lib/toneform';

type Glint = {
  id: string;
  timestamp: string;
  toneform: string;
  message: string;
  rule?: string;
  file?: string;
  line?: number;
  column?: number;
  metadata?: Record<string, unknown>;
};

type GlintListProps = {
  initialGlints?: Glint[];
  onRefresh?: () => Promise<Glint[]>;
  isLoading?: boolean;
  className?: string;
};

export function GlintList({ 
  initialGlints = [], 
  onRefresh, 
  isLoading: externalLoading,
  className = '' 
}: GlintListProps) {
  const [glints, setGlints] = useState<Glint[]>(initialGlints);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedToneforms, setSelectedToneforms] = useState<string[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  // Update glints when initialGlints changes
  useEffect(() => {
    if (initialGlints.length > 0) {
      setGlints(initialGlints);
      setIsInitialLoad(false);
    }
  }, [initialGlints]);

  // Handle refresh
  const handleRefresh = async () => {
    if (!onRefresh) return;
    
    setIsRefreshing(true);
    try {
      const freshGlints = await onRefresh();
      setGlints(freshGlints);
    } catch (error) {
      console.error('Failed to refresh glints:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  // Filter glints based on search query and selected toneforms
  const filteredGlints = glints.filter(glint => {
    const matchesSearch = 
      glint.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
      glint.rule?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      glint.file?.toLowerCase().includes(searchQuery.toLowerCase());
      
    const matchesToneform = 
      selectedToneforms.length === 0 || 
      selectedToneforms.includes(glint.toneform.toLowerCase());
      
    return matchesSearch && matchesToneform;
  });

  // Get unique toneforms from glints
  const availableToneforms = Array.from(
    new Set(glints.map(glint => glint.toneform.toLowerCase()))
  ).sort();

  const isLoading = externalLoading || isInitialLoad;
  const isRefreshingState = isRefreshing || externalLoading;

  return (
    <div className={`flex flex-col h-full ${className}`}>
      {/* Header with title and refresh button */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Glint Stream</h2>
        <Button 
          variant="outline" 
          size="sm" 
          onClick={handleRefresh}
          disabled={isRefreshingState}
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshingState ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>
      
      {/* Search and filter controls */}
      <div className="space-y-4 mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search glints..."
            className="pl-10"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-muted-foreground flex-shrink-0" />
          <span className="text-sm text-muted-foreground">Filter by toneform:</span>
          <ToggleGroup 
            type="multiple" 
            variant="outline"
            size="sm"
            value={selectedToneforms}
            onValueChange={setSelectedToneforms}
            className="flex-wrap justify-start"
          >
            {availableToneforms.map(toneform => {
              const colors = getToneformColor(toneform);
              return (
                <ToggleGroupItem 
                  key={toneform} 
                  value={toneform}
                  className={`${colors.text} ${colors.border} ${colors.bgHover} capitalize`}
                >
                  {toneform}
                </ToggleGroupItem>
              );
            })}
          </ToggleGroup>
        </div>
      </div>
      
      {/* Glint list */}
      <div className="flex-1 overflow-hidden">
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <Skeleton key={i} className="h-24 w-full rounded-lg" />
            ))}
          </div>
        ) : filteredGlints.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center p-8 text-muted-foreground">
            <Search className="h-12 w-12 mb-4 opacity-30" />
            <h3 className="text-lg font-medium mb-1">No glints found</h3>
            <p className="text-sm">
              {searchQuery || selectedToneforms.length > 0 
                ? 'Try adjusting your search or filter criteria.'
                : 'No glints available. Check back later or refresh to load new glints.'
              }
            </p>
          </div>
        ) : (
          <ScrollArea className="h-full pr-4 -mr-4">
            <div className="space-y-4 pb-4">
              {filteredGlints.map(glint => (
                <GlintCard key={glint.id} glint={glint} />
              ))}
            </div>
          </ScrollArea>
        )}
      </div>
      
      {/* Status bar */}
      <div className="mt-4 pt-2 border-t text-sm text-muted-foreground flex justify-between items-center">
        <span>
          Showing {filteredGlints.length} of {glints.length} glints
          {selectedToneforms.length > 0 && ` (filtered)`}
        </span>
        <span className="text-xs">
          Last updated: {new Date().toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
}
