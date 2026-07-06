"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/Button"
import {
  useParticipationStatus,
  useRegisterParticipation,
  useCancelParticipation,
} from "@/lib/hooks/usePublic"
import { UserPlus, UserMinus, Loader2 } from "lucide-react"

interface ParticipateButtonProps {
  eventId: string
}

export function ParticipateButton({ eventId }: ParticipateButtonProps) {
  const { data: status, isLoading: statusLoading } = useParticipationStatus(eventId)
  const register = useRegisterParticipation()
  const cancel = useCancelParticipation()

  const isLoading = register.isPending || cancel.isPending || statusLoading
  const isRegistered = status?.is_registered ?? false

  const handleClick = async () => {
    if (isRegistered) {
      await cancel.mutateAsync(eventId)
    } else {
      await register.mutateAsync(eventId)
    }
  }

  return (
    <motion.div whileTap={{ scale: 0.97 }}>
      <Button
        variant={isRegistered ? "secondary" : "primary"}
        onClick={handleClick}
        isLoading={isLoading}
      >
        {isLoading ? (
          <Loader2 className="mr-1.5 h-4 w-4 animate-spin" />
        ) : isRegistered ? (
          <UserMinus className="mr-1.5 h-4 w-4" />
        ) : (
          <UserPlus className="mr-1.5 h-4 w-4" />
        )}
        {isRegistered ? "Отменить" : "Записаться"}
      </Button>
    </motion.div>
  )
}
