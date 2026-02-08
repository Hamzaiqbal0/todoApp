'use client'

import { useState, useEffect } from 'react'
import { Plus, Check, Trash2, Edit3 } from 'lucide-react'

// Define types
type Todo = {
  id: string
  title: string
  description?: string
  completed: boolean
  priority: 'low' | 'medium' | 'high' | 'urgent'
  due_date?: string
  category?: string
  tags?: string[]
  created_at: string
  updated_at: string
}

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [newTodo, setNewTodo] = useState('')
  const [loading, setLoading] = useState(true)

  // Load todos from API
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await fetch('/api/todos')
        const data = await response.json()
        if (data.success) {
          setTodos(data.data.todos || [])
        }
      } catch (error) {
        console.error('Error fetching todos:', error)
      } finally {
        setLoading(false)
      }
    }

    // For now, we'll simulate data since the backend isn't running yet
    setTodos([
      {
        id: '1',
        title: 'Learn Next.js',
        description: 'Complete the official Next.js tutorial',
        completed: false,
        priority: 'high',
        due_date: '2023-12-31',
        category: 'work',
        tags: ['important'],
        created_at: '2023-12-01T10:00:00Z',
        updated_at: '2023-12-01T10:00:00Z'
      },
      {
        id: '2',
        title: 'Build Todo App',
        description: 'Create a full-stack todo application',
        completed: true,
        priority: 'medium',
        due_date: '2023-12-15',
        category: 'personal',
        tags: ['project'],
        created_at: '2023-12-01T09:00:00Z',
        updated_at: '2023-12-02T15:30:00Z'
      }
    ])
    setLoading(false)
  }, [])

  const addTodo = async () => {
    if (!newTodo.trim()) return

    // Simulate API call
    const newTodoItem: Todo = {
      id: Date.now().toString(),
      title: newTodo,
      completed: false,
      priority: 'medium',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }

    setTodos([newTodoItem, ...todos])
    setNewTodo('')
  }

  const toggleTodo = async (id: string) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ))
  }

  const deleteTodo = async (id: string) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-500'
      case 'urgent': return 'text-red-700'
      case 'medium': return 'text-yellow-500'
      case 'low': return 'text-green-500'
      default: return 'text-gray-500'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Todo Application</h1>
          <p className="text-gray-600">Manage your tasks efficiently</p>
        </header>

        <main>
          {/* Add Todo Form */}
          <div className="bg-white rounded-xl shadow-md p-6 mb-8">
            <div className="flex gap-3">
              <input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="What needs to be done?"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                onKeyDown={(e) => e.key === 'Enter' && addTodo()}
              />
              <button
                onClick={addTodo}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition duration-200"
              >
                <Plus size={20} />
                <span>Add</span>
              </button>
            </div>
          </div>

          {/* Todo List */}
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="border-b border-gray-200 p-4 bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800">Your Tasks</h2>
            </div>

            {loading ? (
              <div className="p-8 text-center">
                <p>Loading todos...</p>
              </div>
            ) : todos.length === 0 ? (
              <div className="p-8 text-center">
                <p className="text-gray-500">No tasks yet. Add your first task!</p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {todos.map((todo) => (
                  <li key={todo.id} className="p-4 hover:bg-gray-50 transition duration-150">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <button
                          onClick={() => toggleTodo(todo.id)}
                          className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                            todo.completed
                              ? 'bg-green-500 border-green-500 text-white'
                              : 'border-gray-300 hover:border-green-400'
                          }`}
                        >
                          {todo.completed && <Check size={16} />}
                        </button>
                        
                        <div>
                          <h3
                            className={`font-medium ${
                              todo.completed ? 'line-through text-gray-500' : 'text-gray-800'
                            }`}
                          >
                            {todo.title}
                          </h3>
                          {todo.description && (
                            <p className="text-sm text-gray-600 mt-1">{todo.description}</p>
                          )}
                          
                          <div className="flex gap-3 mt-2">
                            {todo.priority && (
                              <span className={`text-xs px-2 py-1 rounded-full ${getPriorityColor(todo.priority)} bg-opacity-20`}>
                                {todo.priority}
                              </span>
                            )}
                            
                            {todo.category && (
                              <span className="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-800">
                                {todo.category}
                              </span>
                            )}
                            
                            {todo.tags && todo.tags.length > 0 && (
                              <div className="flex gap-1">
                                {todo.tags.map((tag, index) => (
                                  <span key={index} className="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-800">
                                    {tag}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex gap-2">
                        <button className="p-2 text-gray-500 hover:text-blue-500 hover:bg-blue-50 rounded-full">
                          <Edit3 size={18} />
                        </button>
                        <button
                          onClick={() => deleteTodo(todo.id)}
                          className="p-2 text-gray-500 hover:text-red-500 hover:bg-red-50 rounded-full"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </div>
                    
                    {todo.due_date && (
                      <div className="mt-2 text-sm text-gray-500 flex items-center gap-1">
                        Due: {new Date(todo.due_date).toLocaleDateString()}
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </main>

        <footer className="mt-12 text-center text-gray-600 text-sm">
          <p>© {new Date().getFullYear()} Todo Application. All rights reserved.</p>
        </footer>
      </div>
    </div>
  )
}