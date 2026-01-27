'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();

  // Close mobile menu on route change
  useEffect(() => {
    setIsMenuOpen(false);
  }, [pathname]);

  return (
    <header className="fixed top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6  lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg">
              <svg
                className="h-6 w-6 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2"
                />
              </svg>
            </div>
            <span className="ml-3 text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              TaskFlow
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link
              href="/login"
              className={`text-sm font-semibold transition-all
                ${
                  pathname === '/login'
                    ? 'text-indigo-600 underline underline-offset-4'
                    : 'text-gray-600 hover:text-indigo-600'
                }`}
            >
              Sign in
            </Link>

            <Link
              href="/signup"
              className="inline-flex items-center justify-center
                px-6 py-3 rounded-2xl text-sm font-semibold text-white
                bg-gradient-to-r from-indigo-600 to-purple-600
                shadow-lg transition-all
                hover:from-indigo-700 hover:to-purple-700 hover:scale-105"
            >
              Get Started
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden inline-flex items-center justify-center
              rounded-lg p-2 text-gray-600 hover:text-indigo-600
              hover:bg-gray-100 focus:outline-none focus:ring-2
              focus:ring-indigo-500"
            aria-expanded={isMenuOpen}
            aria-label="Toggle menu"
          >
            {!isMenuOpen ? (
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            ) : (
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t bg-white/95 backdrop-blur">
          <div className="flex flex-col gap-4 px-6 py-6">
            <Link
              href="/login"
              className={`text-base font-semibold transition
                ${
                  pathname === '/login'
                    ? 'text-indigo-600 underline underline-offset-4'
                    : 'text-gray-600 hover:text-indigo-600'
                }`}
            >
              Sign in
            </Link>

            <Link
              href="/signup"
              className="w-full text-center rounded-2xl px-6 py-3
                font-semibold text-white
                bg-gradient-to-r from-indigo-600 to-purple-600
                shadow-lg hover:from-indigo-700 hover:to-purple-700 transition"
            >
              Get Started
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
