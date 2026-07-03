export function Footer() {
  return (
    <footer className="border-t border-slate-200">
      <div className="mx-auto max-w-6xl px-4 py-6 text-center text-sm text-slate-500">
        &copy; {new Date().getFullYear()} Event Aggregator
      </div>
    </footer>
  );
}
