import { usePageTitle } from '../hooks/usePageTitle'

export function PageShell({ title, eyebrow, children, actions }) {
  usePageTitle(title)

  return (
    <section className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          {eyebrow ? <p className="mb-2 text-sm font-black uppercase tracking-[0.16em] text-leaf">{eyebrow}</p> : null}
          <h1 className="text-3xl font-black tracking-normal text-ink sm:text-4xl">{title}</h1>
        </div>
        {actions ? <div className="flex flex-wrap gap-2">{actions}</div> : null}
      </div>
      {children}
    </section>
  )
}
