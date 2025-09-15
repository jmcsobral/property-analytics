import Link from "next/link";

export default function Layout({ children, sidebar }) {
  return (
    <div className="flex h-screen flex-col bg-gray-50">
      {/* Top Navbar */}
      <header className="flex justify-between items-center bg-white border-b shadow-sm px-6 py-3">
        <h1 className="text-xl font-bold text-blue-600">Property Analytics</h1>
        <nav className="space-x-4">
          <Link href="/">
            <span className="text-gray-700 hover:text-blue-600 cursor-pointer">
              Dashboard
            </span>
          </Link>
          <Link href="/snapshots">
            <span className="text-gray-700 hover:text-blue-600 cursor-pointer">
              Snapshots
            </span>
          </Link>
        </nav>
      </header>

      {/* Main content with sidebar + body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar (filters) */}
        {sidebar && (
          <aside className="w-72 bg-white border-r shadow-sm p-4 overflow-y-auto">
            {sidebar}
          </aside>
        )}

        {/* Main content */}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
