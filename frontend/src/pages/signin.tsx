import { useAuth } from '../hooks/useAuth';
import AuthForm from '../components/AuthForm';
import { useRouter } from 'next/router';
import { useEffect } from 'react';

const SigninPage = () => {
  const { user, loading } = useAuth();
  const router = useRouter();

  // If user is already authenticated, redirect to todos page
  useEffect(() => {
    if (!loading && user) {
      router.push('/todos');
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (user) {
    return null; // Redirecting will happen in useEffect
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 to-indigo-500 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center">
            <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Access your task management dashboard
          </p>
        </div>
        <div className="bg-blue-900 rounded-xl shadow-xl p-8">
          <AuthForm type="login" />
        </div>
      </div>
    </div>
  );
};

export default SigninPage;