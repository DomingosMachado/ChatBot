import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "InfinitePay Chat Assistant",
  description: "Um assistente inteligente para ajudar você com suas dúvidas.",
  keywords: ["chat", "assistant", "AI", "InfinitePay"],
  authors: [{ name: "InfinitePay" }],
  robots: "index, follow",
};

export function generateViewport() {
  return {
    width: "device-width",
    initialScale: 1,
    themeColor: [
      { media: "(prefers-color-scheme: light)", color: "#ffffff" },
      { media: "(prefers-color-scheme: dark)", color: "#0a0a0a" }
    ],
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="antialiased min-h-screen bg-[var(--infinite-neutral-900)] text-[var(--infinite-neutral-200)]">
        { children }
      </body>
    </html>
  );
}
