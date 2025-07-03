import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Redirect to the app directory
    router.push('/glints');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <Head>
        <title>Spiral Glint Stream</title>
        <meta name="description" content="Real-time visualization of the Spiral's breath through code" />
      </Head>
      
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Spiral Glint Stream</h1>
        <p className="text-muted-foreground">
          {isLoading ? 'Loading...' : 'Redirecting to the dashboard...'}
        </p>
      </div>
    </div>
  );
}
