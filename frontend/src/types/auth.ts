export interface LoginRequest {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserMeResponse {
  id: string
  username: string
  email: string
  role: {
    id: number
    name: string
  }
  permissions: string[]
}
