import { useState } from 'react';

interface TodoFormProps {
  onSubmit: (description: string) => void;
  placeholder?: string;
  buttonText?: string;
}

const TodoForm = ({ onSubmit, placeholder = "Add a new task...", buttonText = "Add" }: TodoFormProps) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedValue = inputValue.trim();
    if (trimmedValue) {
      onSubmit(trimmedValue);
      setInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex shadow-sm">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder={placeholder}
        className="flex-grow px-4 py-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-700"
      />
      <button
        type="submit"
        className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-r-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200 font-medium"
      >
        {buttonText}
      </button>
    </form>
  );
};

export default TodoForm;