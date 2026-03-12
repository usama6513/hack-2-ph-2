import { useState, useEffect } from 'react';
import { Todo } from '../types';
import api from '../services/api';
import TodoForm from './TodoForm';

interface TodoListProps {
  userId: number;
}

const TodoList = ({ userId }: TodoListProps) => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed' | 'pending'>('all');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data = await api.getTodos();
      setTodos(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch todos');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (description: string) => {
    try {
      const newTodo = await api.createTodo(description);
      setTodos([...todos, newTodo]);
    } catch (err: any) {
      setError(err.message || 'Failed to create todo');
    }
  };

  const handleUpdateTodo = async (id: number, description: string) => {
    try {
      const updatedTodo = await api.updateTodo(id, description);
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo));
      setEditingTodo(null);
    } catch (err: any) {
      setError(err.message || 'Failed to update todo');
    }
  };

  const handleToggleTodo = async (id: number) => {
    try {
      const updatedTodo = await api.toggleTodoStatus(id);
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo));
    } catch (err: any) {
      setError(err.message || 'Failed to toggle todo status');
    }
  };

  const handleDeleteTodo = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this todo?")) {
      try {
        await api.deleteTodo(id);
        setTodos(todos.filter(todo => todo.id !== id));
      } catch (err: any) {
        setError(err.message || 'Failed to delete todo');
      }
    }
  };

  const getTodoStatus = (todo: Todo) => {
    if (todo.completed) return 'completed';
    if (new Date(todo.created_at) > new Date(Date.now() - 24 * 60 * 60 * 1000)) {
      return 'pending';
    }
    return 'active';
  };

  const filteredTodos = todos.filter(todo => {
    if (filter === 'completed') return todo.completed;
    if (filter === 'active') return !todo.completed && getTodoStatus(todo) === 'active';
    if (filter === 'pending') return !todo.completed && getTodoStatus(todo) === 'pending';
    return true;
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">My Tasks</h1>
        <p className="text-gray-600">Manage your daily tasks efficiently</p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <TodoForm
          onSubmit={handleCreateTodo}
          placeholder="Add a new task..."
          buttonText="Add Task"
        />
      </div>

      {/* Filter buttons */}
      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            filter === 'all'
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All ({todos.length})
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            filter === 'active'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Active ({todos.filter(t => !t.completed && getTodoStatus(t) === 'active').length})
        </button>
        <button
          onClick={() => setFilter('pending')}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            filter === 'pending'
              ? 'bg-yellow-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Pending ({todos.filter(t => !t.completed && getTodoStatus(t) === 'pending').length})
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            filter === 'completed'
              ? 'bg-green-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Completed ({todos.filter(t => t.completed).length})
        </button>
      </div>

      {filteredTodos.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks found</h3>
          <p className="text-gray-500">
            {filter === 'all'
              ? "Get started by adding a new task above."
              : `No ${filter} tasks at the moment.`}
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <ul className="divide-y divide-gray-200">
            {filteredTodos.map(todo => {
              const status = getTodoStatus(todo);
              return (
                <li key={todo.id} className="p-4 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center flex-grow">
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => handleToggleTodo(todo.id)}
                        className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
                      />
                      <div className="ml-3 flex-1 min-w-0">
                        {editingTodo?.id === todo.id ? (
                          <input
                            type="text"
                            defaultValue={todo.description}
                            className="w-full px-3 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            onBlur={(e) => {
                              if (e.target.value.trim()) {
                                handleUpdateTodo(todo.id, e.target.value);
                              }
                            }}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter' && e.currentTarget.value.trim()) {
                                handleUpdateTodo(todo.id, e.currentTarget.value);
                              }
                            }}
                            autoFocus
                          />
                        ) : (
                          <div>
                            <p className={`text-sm font-medium text-gray-900 truncate ${
                              todo.completed ? 'line-through text-gray-500' : ''
                            }`}>
                              {todo.description}
                            </p>
                            <div className="flex items-center mt-1 space-x-2">
                              <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                                status === 'completed'
                                  ? 'bg-green-100 text-green-800'
                                  : status === 'pending'
                                    ? 'bg-yellow-100 text-yellow-800'
                                    : 'bg-blue-100 text-blue-800'
                              }`}>
                                {status.charAt(0).toUpperCase() + status.slice(1)}
                              </span>
                              <span className="text-xs text-gray-500">
                                {new Date(todo.created_at).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => setEditingTodo(todo)}
                        className="text-indigo-600 hover:text-indigo-900 p-1 rounded hover:bg-indigo-50 transition-colors"
                        title="Edit task"
                      >
                        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => handleDeleteTodo(todo.id)}
                        className="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50 transition-colors"
                        title="Delete task"
                      >
                        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
};

export default TodoList;