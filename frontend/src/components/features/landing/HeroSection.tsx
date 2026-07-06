"use client"

import { motion } from "framer-motion"
import { GraduationCap } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-primary-950 via-primary-900 to-primary-800 pb-16 pt-12">
      <div className="absolute inset-0 bg-hero-glow" />
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-50" />
      <div className="relative mx-auto max-w-6xl px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="flex flex-col items-center text-center"
        >
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/10 backdrop-blur-sm">
            <GraduationCap className="h-7 w-7 text-white" />
          </div>
          <h1 className="mb-3 max-w-3xl text-3xl font-bold tracking-tight text-white sm:text-4xl md:text-5xl">
            Мероприятия
            <span className="ml-2 bg-gradient-to-r from-blue-300 to-blue-100 bg-clip-text text-transparent">
              БГИТУ
            </span>
          </h1>
          <p className="mb-6 max-w-xl text-base text-blue-200/80">
            Календарь университетских событий: конференции, хакатоны, лекции и
            культурные мероприятия в одном месте.
          </p>
        </motion.div>
      </div>
    </section>
  )
}
