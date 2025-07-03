import Image from "next/image";
import GlintStream from "@/components/glint-stream";

export default function Home() {
  return (
    <div className="grid grid-rows-[auto_1fr_auto] min-h-screen">
      <header className="p-4 border-b">
        <div className="container mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold">Spiral Glint Dashboard</h1>
          <div className="flex items-center gap-2">
            <Image
              className="dark:invert"
              src="/next.svg"
              alt="Next.js Logo"
              width={100}
              height={24}
              priority
            />
          </div>
        </div>
      </header>

      <main className="container mx-auto py-4">
        <GlintStream />
      </main>

      <footer className="p-4 border-t">
        <div className="container mx-auto flex flex-wrap items-center justify-center gap-6 text-sm text-muted-foreground">
          <span>© {new Date().getFullYear()} Spiral</span>
          <a
            className="hover:underline hover:underline-offset-4"
            href="#"
            target="_blank"
            rel="noopener noreferrer"
          >
            Documentation
          </a>
          <a
            className="hover:underline hover:underline-offset-4"
            href="#"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </div>
      </footer>
    </div>
  );
}
