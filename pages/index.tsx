"use client"

import Link from 'next/link';
//import { SignInButton, SignedIn, SignedOut, UserButton } from '@clerk/nextjs';
import { SignInButton, Show, UserButton } from '@clerk/nextjs'; //cambio por actualización, ya no se usan SignedIn y SignedOut, ahora se usa Show con when="signed-in" o when="signed-out"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        {/* Navigation */}
        <nav className="flex justify-between items-center mb-12">
          <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-200">
            IdeaGen
          </h1>
          <div>
            <Show when="signed-out">
              <SignInButton mode="modal">
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
                  Iniciar Sesión
                </button>
              </SignInButton>
            </Show>
            <Show when="signed-in">
              <div className="flex items-center gap-4">
                <Link
                  href="/product"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                >
                  Ir a la App
                </Link>
                <UserButton />
              </div>
            </Show>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="text-center py-24">
          <h2 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            Genera tu siguiente
            <br />
            Gran idea de negocio
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
            Aproveche el poder de la IA para descubrir oportunidades comerciales innovadoras adaptadas a la economía de los agentes de IA.
          </p>

          <Show when="signed-out">
            <SignInButton mode="modal">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Empieza gratis
              </button>
            </SignInButton>
          </Show>
          <Show when="signed-in">
            <Link href="/product">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Generar Ideas Ahora
              </button>
            </Link>
          </Show>
        </div>
      </div>
    </main>
  );
}