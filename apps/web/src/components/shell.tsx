import { ReactNode } from 'react';

import { Header } from './header';
import { Sidebar } from './sidebar';

export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="grid-bg min-h-screen p-4 lg:p-6">
      <div className="mx-auto flex max-w-[1600px] gap-6">
        <Sidebar />
        <main className="flex-1 space-y-6">
          <Header />
          {children}
        </main>
      </div>
    </div>
  );
}
