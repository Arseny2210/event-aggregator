"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/Button"
import { useParticipationStatus, useRegisterParticipation } from "@/lib/hooks/usePublic"
import { UserPlus, Check, Loader2 } from "lucide-react"

interface ParticipateButtonProps {
  eventId: string
}

export function ParticipateButton({ eventId }: ParticipateButtonProps) {
  const { data: status, isLoading: statusLoading } = useParticipationStatus(eventId)
  const register = useRegisterParticipation()

  const isLoading = register.isPending || statusLoading
  const isRegistered = status?.is_registered ?? false

  const handleClick = async () => {
    if (isRegistered) return
    await register.mutateAsync(eventId)
  }

  return (
    <motion.div whileTap={isRegistered ? undefined : { scale: 0.97 }}>
      <Button
        variant={isRegistered ? "success" : "primary"}
        onClick={handleClick}
        isLoading={isLoading}
        disabled={isRegistered}
      >
        {isLoading ? (
          <Loader2 className="mr-1.5 h-4 w-4 animate-spin" />
        ) : isRegistered ? (
          <Check className="mr-1.5 h-4 w-4" />
        ) : (
          <UserPlus className="mr-1.5 h-4 w-4" />
        )}
        {isRegistered ? "Вы записаны" : "Записаться"}
      </Button>
    </motion.div>
  )
}
