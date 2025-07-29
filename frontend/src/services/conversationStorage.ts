export class ConversationStorage {
  private static getStorageKey(agentType: string): string {
    return `thread_id_${agentType}`;
  }

  static saveThreadId(agentType: string, threadId: string): void {
    try {
      const key = this.getStorageKey(agentType);
      localStorage.setItem(key, threadId);
    } catch (error) {
      console.error('Failed to save thread ID to localStorage:', error);
    }
  }

  static loadThreadId(agentType: string): string | null {
    try {
      const key = this.getStorageKey(agentType);
      return localStorage.getItem(key);
    } catch (error) {
      console.error('Failed to load thread ID from localStorage:', error);
      return null;
    }
  }

  static clearThreadId(agentType: string): void {
    try {
      const key = this.getStorageKey(agentType);
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Failed to clear thread ID from localStorage:', error);
    }
  }

  static async clearConversation(agentType: string, threadId: string): Promise<void> {
    try {
      const response = await fetch(`http://localhost:8000/conversations/${threadId}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        // Clear the stored thread ID as well
        this.clearThreadId(agentType);
      } else {
        console.error('Failed to clear conversation on server');
      }
    } catch (error) {
      console.error('Error clearing conversation:', error);
    }
  }
}
