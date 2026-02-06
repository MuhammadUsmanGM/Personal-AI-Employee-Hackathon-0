import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  
  // Initialize supabase with environment variables and headers
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL || '',
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
    {
      global: {
        headers: {
          Cookie: req.headers.get('cookie') ?? '',
        }
      },
      auth: {
        persistSession: false,
      },
    }
  )

  // Check session using the request cookies
  // Note: For Next.js App Router, we typically use @supabase/ssr or manual cookie handling
  // For this simple implementation, we'll check if the auth session exists
  const { data: { session } } = await supabase.auth.getSession()

  const { pathname } = req.nextUrl

  // Protect all dashboard and internal routes
  // Allow access to /auth, /api, and static assets
  const isAuthPage = pathname.startsWith('/auth')
  const isApiRoute = pathname.startsWith('/api')
  const isPublicFile = pathname.includes('.') // Simple check for assets
  const isStaticNext = pathname.startsWith('/_next')

  if (!session && !isAuthPage && !isApiRoute && !isPublicFile && !isStaticNext && pathname !== '/') {
    return NextResponse.redirect(new URL('/auth', req.url))
  }

  // If logged in and on auth page, redirect to dashboard
  if (session && isAuthPage) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }

  return res
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
