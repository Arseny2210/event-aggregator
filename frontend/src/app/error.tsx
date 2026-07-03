"use client";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <section className="mx-auto max-w-4xl px-4 py-16 text-center">
      <h1 className="mb-4 text-4xl font-bold text-slate-900">Something went wrong</h1>
      <p className="mb-8 text-lg text-slate-600">An unexpected error occurred.</p>
      <button
        onClick={reset}
        className="inline-flex items-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
      >
        Try again
      </button>
    </section>
  );
}
