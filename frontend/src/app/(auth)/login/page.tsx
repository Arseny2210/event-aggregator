import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import { LoginForm } from "@/components/features/auth/LoginForm"
import { GraduationCap } from "lucide-react"

export default function LoginPage() {
  return (
    <Card className="text-center">
      <CardHeader>
        <div className="mb-4 flex justify-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-600 text-white">
            <GraduationCap className="h-6 w-6" />
          </div>
        </div>
        <CardTitle>Вход в систему</CardTitle>
        <CardDescription>ИС «Мероприятия» БГИТУ</CardDescription>
      </CardHeader>
      <LoginForm />
    </Card>
  )
}
