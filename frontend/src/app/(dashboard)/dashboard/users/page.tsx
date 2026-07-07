"use client"

import { useState } from "react"
import { Crown, ShieldCheck, ShieldOff, User, Plus, X } from "lucide-react"
import { PageTransition } from "@/components/motion/PageTransition"
import { motion, AnimatePresence } from "framer-motion"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Select } from "@/components/ui/Select"
import { Badge } from "@/components/ui/Badge"
import { Spinner } from "@/components/ui/Spinner"
import { Alert } from "@/components/ui/Alert"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { usersApi, type UserInfo } from "@/lib/api/users"
import { useAuth } from "@/lib/hooks/useAuth"

const ROLE_OPTIONS = [
  { value: "editor", label: "Редактор" },
  { value: "administrator", label: "Администратор" },
]

export default function UsersPage() {
  const { user: currentUser } = useAuth()
  const queryClient = useQueryClient()
  const isAdmin = currentUser?.role?.name === "administrator"

  const { data, isLoading, error } = useQuery({
    queryKey: ["users"],
    queryFn: () => usersApi.list({ limit: 100 }),
    enabled: isAdmin,
  })

  const changeRoleMut = useMutation({
    mutationFn: (params: { userId: string; roleName: string }) =>
      usersApi.changeRole(params.userId, params.roleName),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  })

  const [showCreate, setShowCreate] = useState(false)
  const [createForm, setCreateForm] = useState({
    username: "",
    email: "",
    password: "",
    role_name: "editor",
  })
  const [createError, setCreateError] = useState("")

  const createMut = useMutation({
    mutationFn: (data: typeof createForm) => usersApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
      setShowCreate(false)
      setCreateForm({ username: "", email: "", password: "", role_name: "editor" })
      setCreateError("")
    },
    onError: (err: Error) => setCreateError(err.message),
  })

  if (!isAdmin) {
    return (
      <PageTransition>
        <Alert variant="error">Доступ запрещён. Только для администратора.</Alert>
      </PageTransition>
    )
  }

  if (isLoading) {
    return (
      <PageTransition>
        <div className="flex justify-center py-12">
          <Spinner className="h-8 w-8" />
        </div>
      </PageTransition>
    )
  }

  if (error) {
    return (
      <PageTransition>
        <Alert variant="error">Ошибка загрузки пользователей</Alert>
      </PageTransition>
    )
  }

  const users = data?.items ?? []

  return (
    <PageTransition>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Пользователи</h1>
          <Button onClick={() => setShowCreate(true)}>
            <Plus className="mr-1.5 h-4 w-4" />
            Создать пользователя
          </Button>
        </div>

        <AnimatePresence>
          {showCreate && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="overflow-hidden"
            >
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Новый пользователь</CardTitle>
                    <Button variant="ghost" size="sm" onClick={() => setShowCreate(false)}>
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>
                <form
                  onSubmit={(e) => {
                    e.preventDefault()
                    setCreateError("")
                    createMut.mutate(createForm)
                  }}
                  className="space-y-4 p-6 pt-0"
                >
                  {createError && (
                    <Alert variant="error">{createError}</Alert>
                  )}
                  <Input
                    label="Имя пользователя"
                    placeholder="petrov"
                    value={createForm.username}
                    onChange={(e) =>
                      setCreateForm({ ...createForm, username: e.target.value })
                    }
                    required
                  />
                  <Input
                    label="Email"
                    type="email"
                    placeholder="petrov@bgitu.ru"
                    value={createForm.email}
                    onChange={(e) =>
                      setCreateForm({ ...createForm, email: e.target.value })
                    }
                    required
                  />
                  <Input
                    label="Пароль"
                    type="password"
                    placeholder="Минимум 8 символов"
                    value={createForm.password}
                    onChange={(e) =>
                      setCreateForm({ ...createForm, password: e.target.value })
                    }
                    required
                  />
                  <Select
                    label="Роль"
                    options={ROLE_OPTIONS}
                    value={createForm.role_name}
                    onChange={(e) =>
                      setCreateForm({ ...createForm, role_name: e.target.value })
                    }
                  />
                  <div className="flex gap-2">
                    <Button type="submit" isLoading={createMut.isPending}>
                      Создать
                    </Button>
                    <Button type="button" variant="secondary" onClick={() => setShowCreate(false)}>
                      Отмена
                    </Button>
                  </div>
                </form>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        <Card>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border text-left text-xs font-semibold uppercase tracking-wider text-foreground-muted">
                  <th className="p-4">Пользователь</th>
                  <th className="p-4">Email</th>
                  <th className="p-4">Роль</th>
                  <th className="p-4">Действия</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr
                    key={u.id}
                    className="border-b border-border/50 transition-colors hover:bg-surface-secondary/50"
                  >
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-surface-tertiary">
                          <User className="h-4 w-4 text-foreground-muted" />
                        </div>
                        <div>
                          <p className="font-medium text-foreground">{u.username}</p>
                          {u.id === currentUser?.id && (
                            <span className="text-xs text-foreground-muted">это вы</span>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="p-4 text-sm text-foreground-secondary">{u.email}</td>
                    <td className="p-4">
                      <Badge
                        className={
                          u.role.name === "administrator"
                            ? "bg-purple-100 text-purple-700"
                            : "bg-blue-100 text-blue-700"
                        }
                      >
                        {u.role.name === "administrator" ? (
                          <Crown className="mr-1 h-3 w-3" />
                        ) : (
                          <ShieldCheck className="mr-1 h-3 w-3" />
                        )}
                        {u.role.name === "administrator" ? "Администратор" : "Редактор"}
                      </Badge>
                    </td>
                    <td className="p-4">
                      {u.id !== currentUser?.id && (
                        <Button
                          size="sm"
                          variant={u.role.name === "administrator" ? "secondary" : "primary"}
                          onClick={() => {
                            const newRole =
                              u.role.name === "administrator" ? "editor" : "administrator"
                            changeRoleMut.mutate({ userId: u.id, roleName: newRole })
                          }}
                          isLoading={changeRoleMut.isPending}
                        >
                          {u.role.name === "administrator" ? (
                            <>
                              <ShieldOff className="mr-1 h-3.5 w-3.5" />
                              Сделать редактором
                            </>
                          ) : (
                            <>
                              <Crown className="mr-1 h-3.5 w-3.5" />
                              Сделать админом
                            </>
                          )}
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {users.length === 0 && (
            <div className="p-8 text-center text-foreground-muted">
              Нет пользователей
            </div>
          )}
        </Card>
      </div>
    </PageTransition>
  )
}
