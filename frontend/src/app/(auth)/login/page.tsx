import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import { LoginForm } from "@/components/features/auth/LoginForm"

export default function LoginPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">Sign In</CardTitle>
      </CardHeader>
      <LoginForm />
    </Card>
  )
}
