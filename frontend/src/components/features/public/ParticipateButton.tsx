"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
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
  const queryClient = useQueryClient()
  const { data: status, isLoading: statusLoading } = useParticipationStatus(eventId)
  const register = useRegisterParticipation()
  const cancel = useCancelParticipation()
  const [pendingState, setPendingState] = useState<boolean | null>(null)

  const isLoading = register.isPending || cancel.isPending || statusLoading
  const isRegistered = pendingState ?? status?.is_registered ?? false

  const handleClick = async () => {
    try {
      if (isRegistered) {
        setPendingState(false)
        await cancel.mutateAsync(eventId)
        toast("Запись отменена", {
          description: "Вы отменили регистрацию на мероприятие",
          dismissible: true,
          closeButton: true,
        })
      } else {
        setPendingState(true)
        await register.mutateAsync(eventId)
        toast.success("Регистрация подтверждена", {
          description: "Вы успешно записаны на мероприятие",
          dismissible: true,
          closeButton: true,
        })
      }
    } catch (error) {
      setPendingState(null)
      toast.error(error instanceof Error ? error.message : "Ошибка")
    } finally {
      await queryClient.refetchQueries({ queryKey: ["participation", eventId] })
      queryClient.invalidateQueries({ queryKey: ["public-notifications"] })
      setPendingState(null)
      queryClient.invalidateQueries({ queryKey: ["public-events"] })
      queryClient.invalidateQueries({ queryKey: ["public-event", eventId] })
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
