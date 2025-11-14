import React from "react";
import { Button } from "./Button";
import { Input } from "./Input";
import { Alert } from "./Alert";
import { Card, CardHeader, CardTitle, CardBody } from "./Card";
import { UserRole } from "../types/dashboard";

type AuthMode = "login" | "register";

interface AuthFormProps {
  mode: AuthMode;
  email: string;
  password: string;
  registerRole: UserRole;
  authMessage: string | null;
  authError: string | null;
  onModeChange: (mode: AuthMode) => void;
  onEmailChange: (email: string) => void;
  onPasswordChange: (password: string) => void;
  onRegisterRoleChange: (role: UserRole) => void;
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
}

export const AuthForm: React.FC<AuthFormProps> = ({
  mode,
  email,
  password,
  registerRole,
  authMessage,
  authError,
  onModeChange,
  onEmailChange,
  onPasswordChange,
  onRegisterRoleChange,
  onSubmit,
}) => {
  const isLogin = mode === "login";

  return (
    <div className="container-narrow" style={{ paddingTop: "var(--space-12)" }}>
      <Card glassmorphic style={{ maxWidth: "480px", margin: "0 auto" }}>
        <CardHeader style={{ textAlign: "center", paddingBottom: "var(--space-6)", borderBottom: "none" }}>
          <CardTitle style={{ fontSize: "var(--text-3xl)", marginBottom: "var(--space-2)", color: "var(--neutral-900)" }}>
            {isLogin ? "Welcome Back" : "Create Account"}
          </CardTitle>
          <p style={{ color: "var(--neutral-700)", fontSize: "var(--text-base)", margin: 0 }}>
            {isLogin ? "Sign in to your account" : "Join our platform today"}
          </p>
        </CardHeader>
        <CardBody style={{ color: "var(--neutral-900)" }}>
          {authMessage && <Alert variant="success">{authMessage}</Alert>}
          {authError && <Alert variant="error">{authError}</Alert>}

          <form onSubmit={onSubmit} style={{ display: "grid", gap: "var(--space-4)" }}>
            {!isLogin && (
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label" style={{ color: "var(--neutral-900)" }}>I am a...</label>
                <div style={{ display: "flex", gap: "var(--space-3)" }}>
                  <button
                    type="button"
                    onClick={() => onRegisterRoleChange("seeker")}
                    className={registerRole === "seeker" ? "btn btn-primary" : "btn btn-secondary"}
                    style={{ flex: 1 }}
                  >
                    Job Seeker
                  </button>
                  <button
                    type="button"
                    onClick={() => onRegisterRoleChange("employer")}
                    className={registerRole === "employer" ? "btn btn-primary" : "btn btn-secondary"}
                    style={{ flex: 1 }}
                  >
                    Employer
                  </button>
                </div>
              </div>
            )}

            <Input
              type="email"
              label="Email Address"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => onEmailChange(e.target.value)}
              required
              autoComplete="email"
            />

            <Input
              type="password"
              label="Password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => onPasswordChange(e.target.value)}
              required
              autoComplete={isLogin ? "current-password" : "new-password"}
              helper={!isLogin ? "Minimum 8 characters recommended" : undefined}
            />

            <Button type="submit" variant="primary" size="lg" style={{ width: "100%" }}>
              {isLogin ? "Sign In" : "Create Account"}
            </Button>
          </form>

          <div style={{ marginTop: "var(--space-6)", textAlign: "center" }}>
            <p style={{ color: "var(--neutral-600)", fontSize: "var(--text-sm)" }}>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                type="button"
                onClick={() => onModeChange(isLogin ? "register" : "login")}
                style={{
                  background: "none",
                  border: "none",
                  color: "var(--primary-600)",
                  fontWeight: "var(--font-medium)",
                  cursor: "pointer",
                  textDecoration: "underline",
                  padding: 0,
                }}
              >
                {isLogin ? "Sign up" : "Sign in"}
              </button>
            </p>
          </div>
        </CardBody>
      </Card>
    </div>
  );
};
