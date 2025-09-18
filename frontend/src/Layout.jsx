import Header from "./components/Header";

export default function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen min-w-full bg-gray-50">
      <Header />
      <main className="flex grow flex-col px-12">{children}</main>
    </div>
  );
}
