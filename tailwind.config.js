/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // 中国风 Chinoiserie — 全部走 CSS 变量，避免 Tailwind 缓存旧色值
        // #C9563A #EAD6B8 #777A86 #292C30 #684131
        primary: 'rgb(var(--color-primary) / <alpha-value>)',
        primaryLight: 'rgb(var(--color-primary-light) / <alpha-value>)',
        primaryDark: 'rgb(var(--color-primary-dark) / <alpha-value>)',
        accentCream: 'rgb(var(--color-cream) / <alpha-value>)',
        accentGray: 'rgb(var(--color-gray) / <alpha-value>)',
        accentBrown: 'rgb(var(--color-brown) / <alpha-value>)',
        accentOrange: 'rgb(var(--color-primary) / <alpha-value>)',
        accentPurple: 'rgb(var(--color-purple) / <alpha-value>)',
        accentYellow: 'rgb(var(--color-yellow) / <alpha-value>)',
        accentPink: 'rgb(var(--color-pink) / <alpha-value>)',
        background: 'rgb(var(--color-bg) / <alpha-value>)',
        text: 'rgb(var(--color-text) / <alpha-value>)',
        textSecondary: 'rgb(var(--color-text-secondary) / <alpha-value>)',
        textTertiary: 'rgb(var(--color-text-tertiary) / <alpha-value>)',
        textFaint: 'rgb(var(--color-text-faint) / <alpha-value>)',
        border: 'rgb(var(--color-border) / <alpha-value>)',
        success: 'rgb(var(--color-success) / <alpha-value>)',
        successText: 'rgb(var(--color-success-text) / <alpha-value>)',
        danger: 'rgb(var(--color-danger) / <alpha-value>)',
        dangerText: 'rgb(var(--color-danger-text) / <alpha-value>)',
        warning: 'rgb(var(--color-warning) / <alpha-value>)',
        warningText: 'rgb(var(--color-warning-text) / <alpha-value>)',
      },
      fontFamily: {
        sans: ['PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', 'sans-serif'],
      },
      fontSize: {
        'title-lg': ['26px', '1.4'],
        'title-md': ['20px', '1.4'],
        'body': ['16px', '1.7'],
        'body-sm': ['14px', '1.6'],
        'caption': ['12px', '1.5'],
      },
      borderRadius: {
        card: '12px',
        button: '8px',
      },
      boxShadow: {
        // 名称避免与 colors.card 冲突：用 elevation 前缀
        'elevation': 'var(--shadow-card)',
        'elevation-hover': 'var(--shadow-card-hover)',
        'elevation-nav': 'var(--shadow-nav)',
      },
      letterSpacing: {
        body: '0.5px',
      },
      backdropBlur: {
        glass: '12px',
      },
    },
  },
}
