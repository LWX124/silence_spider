import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as any,
    token: null as string | null,
    isAuthenticated: false
  }),
  
  actions: {
    setUser(user: any) {
      this.user = user
      this.isAuthenticated = !!user
    },
    
    setToken(token: string) {
      this.token = token
    },
    
    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
    }
  }
}) 