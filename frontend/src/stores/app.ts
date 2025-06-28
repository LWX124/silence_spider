import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    loading: false,
    sidebarCollapsed: false,
    theme: 'light' as 'light' | 'dark'
  }),
  
  actions: {
    setLoading(loading: boolean) {
      this.loading = loading
    },
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    
    setTheme(theme: 'light' | 'dark') {
      this.theme = theme
    }
  }
}) 