# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Convex + React + Vite application with authentication using Convex Auth. The app is set up with:
- Convex as the backend (database, server logic)
- React as the frontend
- Vite for development and building
- Tailwind CSS for styling (via @tailwindcss/vite)
- TypeScript for type safety
- Convex Auth for password-based authentication

## Common Development Commands

```bash
# Install dependencies
npm install

# Start development (opens frontend and runs Convex backend)
npm run dev

# Build the application
npm run build

# Run linting
npm run lint

# Preview production build
npm run preview
```

## Architecture and Key Patterns

### Backend Structure (Convex)

1. **Function Registration**: Always use the new function syntax with explicit args and returns validators:
   ```typescript
   export const myFunction = query({
     args: { param: v.string() },
     returns: v.object({ result: v.string() }),
     handler: async (ctx, args) => {
       // Implementation
     },
   });
   ```

2. **Authentication**: The app uses Convex Auth with password provider. Access authenticated user with:
   ```typescript
   import { getAuthUserId } from "@convex-dev/auth/server";
   const userId = await getAuthUserId(ctx);
   ```

3. **Schema**: Defined in `convex/schema.ts`. Currently includes:
   - Auth tables (from `authTables`)
   - `numbers` table with `value: v.number()`

4. **File Organization**:
   - `convex/auth.ts` - Authentication setup
   - `convex/auth.config.ts` - Auth configuration
   - `convex/http.ts` - HTTP endpoints
   - `convex/myFunctions.ts` - Main application functions
   - `convex/schema.ts` - Database schema

### Frontend Structure

1. **Main App Component** (`src/App.tsx`):
   - Uses `Authenticated` and `Unauthenticated` components for auth state
   - Implements sign in/sign up form with email/password
   - Shows authenticated content with user email display

2. **Convex Integration**:
   - Uses `useQuery` for data fetching
   - Uses `useMutation` for data modifications
   - Uses `useAuthActions` for authentication operations

3. **Styling**: Tailwind CSS classes are used directly in components

## Important Convex Guidelines (from .cursor/rules/convex_rules.mdc)

1. **Always use validators**: Every function must have explicit `args` and `returns` validators
2. **Use proper function types**: `query`, `mutation`, `action` for public; `internalQuery`, `internalMutation`, `internalAction` for private
3. **Function references**: Use `api.filename.functionName` for public, `internal.filename.functionName` for internal
4. **No `.delete()` in queries**: Use `.collect()` then iterate with `ctx.db.delete()`
5. **Indexes over filters**: Define indexes in schema and use `withIndex` instead of `filter`
6. **Type safety**: Use `Id<'tableName'>` for document IDs, not generic strings

## Testing

Currently, no test framework is configured. To add tests, consider:
- Setting up Vitest for unit tests (aligns with Vite)
- Using React Testing Library for component tests
- Adding test scripts to package.json

## Environment Variables

- `VITE_CONVEX_URL` - Required for connecting to Convex backend
- `CONVEX_SITE_URL` - Used in auth configuration

## Key TypeScript Configurations

- Strict mode is enabled
- Project references: `tsconfig.app.json` (app code) and `tsconfig.node.json` (build scripts)
- Convex directory has its own `tsconfig.json`

## ESLint Configuration

- TypeScript-aware linting with type checking
- React hooks rules enabled
- Allows unused vars with `_` prefix
- Allows explicit `any` types (can be made stricter later)