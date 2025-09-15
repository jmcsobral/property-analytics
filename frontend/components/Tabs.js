import Link from "next/link";
import { useRouter } from "next/router";

const tabs = [
  { name: "All Data", href: "/" },
  { name: "New", href: "/new" },
  { name: "Sold", href: "/sold" },
  { name: "Price Drops", href: "/price-drops" },
  { name: "Reviewed", href: "/reviewed" },
];

export default function Tabs() {
  const router = useRouter();
  return (
    <nav className="flex space-x-6">
      {tabs.map((tab) => (
        <Link
          key={tab.name}
          href={tab.href}
          className={`pb-2 border-b-2 ${
            router.pathname === tab.href
              ? "border-blue-600 text-blue-600 font-semibold"
              : "border-transparent text-gray-500 hover:text-gray-700"
          }`}
        >
          {tab.name}
        </Link>
      ))}
    </nav>
  );
}
