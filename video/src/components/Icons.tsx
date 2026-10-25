import React from "react";
export const Icon: React.FC<{
  name: string;
  size?: number;
  color?: string;
  stroke?: number;
}> = ({ name, size = 32, color = "currentColor", stroke = 1.8 }) => {
  const paths: Record<string, React.ReactNode> = {
    chevron: <path d="m15 5-7 7 7 7" />,
    right: <path d="m9 5 7 7-7 7" />,
    plus: <path d="M12 5v14M5 12h14" />,
    check: <path d="m5 12 4 4L19 6" />,
    arrow: <path d="M12 19V5m-6 6 6-6 6 6" />,
    mic: (
      <>
        <rect x="9" y="3" width="6" height="12" rx="3" />
        <path d="M6 11v1a6 6 0 0 0 12 0v-1M12 18v3m-3 0h6" />
      </>
    ),
    file: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5" />
      </>
    ),
    video: (
      <>
        <rect x="3" y="6" width="12" height="12" rx="3" />
        <path d="m15 10 6-4v12l-6-4" />
      </>
    ),
    share: (
      <>
        <path d="M8 8H5v13h14V8h-3M12 15V2m-4 4 4-4 4 4" />
      </>
    ),
    expand: (
      <>
        <path d="M8 3H3v5M16 3h5v5M3 16v5h5M21 16v5h-5" />
      </>
    ),
    clock: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 2" />
      </>
    ),
    book: (
      <>
        <path d="M3 4h8v16H3zM11 4h10v16H11M6 8h2m6 0h4M6 12h2m6 0h4" />
      </>
    ),
  };
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth={stroke}
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{ flexShrink: 0 }}
    >
      {paths[name] ?? paths.file}
    </svg>
  );
};
