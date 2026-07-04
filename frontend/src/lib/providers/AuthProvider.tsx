"use client"

import { createContext, useCallback, useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { authApi } from "@/lib/api/auth"
import { clearTokens, getAccessToken, setTokens } from "@/lib/utils/auth"
import type { UserMeResponse } from "@/types/auth"

interface AuthState {
  user: UserMeResponse | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<string | null>
  logout: () => void
}

export const AuthContext = createContext<AuthState>({
  user: null,
  isLoading: true,
  isAuthenticated: false,
  login: async () => null,
  logout: () => {},
})

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserMeResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  const fetchUser = useCallback(async () => {
    const token = getAccessToken()
    if (!token) {
      setIsLoading(false)
      return
    }
    try {
      const me = await authApi.me()
      setUser(me)
    } catch {
      clearTokens()
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchUser()
  }, [fetchUser])

  const login = useCallback(
    async (username: string, password: string): Promise<string | null> => {
      try {
        const result = await authApi.login({ username, password })
        setTokens(result.access_token, result.refresh_token)
        await fetchUser()
        router.push("/dashboard")
        return null
      } catch (err) {
        return err instanceof Error ? err.message : "Login failed"
      }
    },
    [fetchUser, router],
  )

  const logout = useCallback(() => {
    authApi.logout().catch(() => {})
    clearTokens()
    setUser(null)
    router.push("/login")
  }, [router])

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
