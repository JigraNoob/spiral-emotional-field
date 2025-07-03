'use client';

import { useState, useEffect } from 'react';
import { GlintList } from '@/components/glint-list';

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

export default function Home() {
  const [glints, setGlints] = useState<Glint[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchGlints = async (): Promise<Glint[]> => {
    try {
      const response = await fetch('/api/glints');
      if (!response.ok) {
        throw new Error('Failed to fetch glints');
      }
      const data = await response.json();
      setGlints(data);
      setError(null);
      return data;
    } catch (err) {
      console.error('Error fetching glints:', err);
      const errorMessage = 'Failed to load glints. Please try again later.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchGlints().catch(console.error);
  }, []);

  // Set up polling
  useEffect(() => {
    const interval = setInterval(() => {
      fetchGlints().catch(console.error);
    }, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="bg-card shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold">Spiral Glint Dashboard</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Real-time visualization of Spiral Linter Companion glints
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {error ? (
          <div className="bg-destructive/10 border-l-4 border-destructive p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-destructive"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-destructive">{error}</p>
              </div>
            </div>
          </div>
        ) : null}

        <GlintList 
          initialGlints={glints}
          onRefresh={fetchGlints}
          isLoading={isLoading}
          className="min-h-[calc(100vh-200px)]"
        />
      </main>

      <footer className="bg-card mt-12 border-t border-border">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-muted-foreground">
            Spiral Glint Dashboard • {new Date().getFullYear()}
          </p>
        </div>
      </footer>
    </div>
  );
}
