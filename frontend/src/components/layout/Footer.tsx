export function Footer() {
  return (
    <footer className="border-t border-border bg-white">
      <div className="mx-auto max-w-6xl px-4 py-8 text-center text-sm text-foreground-muted">
        <p className="mb-1">
          &copy; {new Date().getFullYear()} БГИТУ — Информационная система управления мероприятиями
        </p>
        <p>Кафедра информационных технологий</p>
      </div>
    </footer>
  )
}
