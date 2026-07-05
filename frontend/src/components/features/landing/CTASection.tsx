"use client"

import Link from "next/link"
import { FadeIn } from "@/components/motion/FadeIn"
import { Button } from "@/components/ui/Button"
import { ArrowRight } from "lucide-react"

export function CTASection() {
  return (
    <section className="bg-surface-secondary py-16">
      <div className="mx-auto max-w-6xl px-4">
        <FadeIn>
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 to-primary-800 px-8 py-14 text-center shadow-xl">
            <div className="absolute inset-0 bg-card-glow" />
            <div className="relative">
              <h2 className="mb-3 text-2xl font-bold text-white">
                Хотите управлять мероприятиями?
              </h2>
              <p className="mb-6 text-base text-blue-100/80">
                Панель управления для организаторов и администраторов университета.
              </p>
              <div className="flex flex-wrap items-center justify-center gap-3">
                <Link href="/login">
                  <Button variant="primary" size="lg" className="bg-white text-primary-700 hover:bg-blue-50">
                    Войти в систему
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Link href="/dashboard">
                  <Button variant="ghost" size="lg" className="text-white hover:bg-white/10">
                    Панель управления
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </FadeIn>
      </div>
    </section>
  )
}
