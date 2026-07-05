"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Alert } from "@/components/ui/Alert"
import { useAuth } from "@/lib/hooks/useAuth"
import { loginSchema, type LoginFormData } from "@/lib/utils/validation"

export function LoginForm() {
  const { login } = useAuth()
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setError(null)
    const err = await login(data.username, data.password)
    if (err) setError(err)
  }

  return (
    <motion.form
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-4 text-left"
    >
      {error && <Alert variant="error">{error}</Alert>}

      <Input
        label="Имя пользователя"
        placeholder="Введите имя пользователя"
        {...register("username")}
        error={errors.username?.message}
      />

      <Input
        label="Пароль"
        type="password"
        placeholder="Введите пароль"
        {...register("password")}
        error={errors.password?.message}
      />

      <Button type="submit" className="w-full" isLoading={isSubmitting}>
        Войти
      </Button>
    </motion.form>
  )
}
