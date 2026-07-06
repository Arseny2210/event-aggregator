"use client"

import { FadeIn } from "@/components/motion/FadeIn"

export function CTASection() {
  return (
    <section className="bg-surface-secondary py-16">
      <div className="mx-auto max-w-6xl px-4">
        <FadeIn>
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 to-primary-800 px-8 py-14 text-center shadow-xl">
            <div className="absolute inset-0 bg-card-glow" />
            <div className="relative">
              <h2 className="mb-3 text-2xl font-bold text-white">
                Будьте в курсе событий
              </h2>
              <p className="mb-6 text-base text-blue-100/80">
                Подписывайтесь на обновления и не пропускайте важные мероприятия университета.
              </p>
            </div>
          </div>
        </FadeIn>
      </div>
    </section>
  )
}
