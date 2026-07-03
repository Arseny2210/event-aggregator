import Link from "next/link";

export default function NotFoundPage() {
  return (
    <section className="mx-auto max-w-4xl px-4 py-16 text-center">
      <h1 className="mb-4 text-6xl font-bold text-slate-900">404</h1>
      <p className="mb-8 text-lg text-slate-600">Page not found.</p>
      <Link
        href="/"
        className="inline-flex items-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
      >
        Go home
      </Link>
    </section>
  );
}
