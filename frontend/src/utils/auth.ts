// 认证相关工具函数

export const getToken = (): string | null => {
  return localStorage.getItem('token')
}

export const setToken = (token: string): void => {
  localStorage.setItem('token', token)
}

export const removeToken = (): void => {
  localStorage.removeItem('token')
}

export const isAuthenticated = (): boolean => {
  return !!getToken()
} 