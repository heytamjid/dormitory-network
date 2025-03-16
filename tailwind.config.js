//tailwind is installed though postcss. 


module.exports = {
  content: [
    "./**/*",
    "!./node_modules/**/*",
    "!./env/**/*"
  ],
  theme: {
    extend: {
      colors: {
        main: 'var(--main)',
        overlay: 'var(--overlay)',
        bg: 'var(--bg)',
        bw: 'var(--bw)',
        blank: 'var(--blank)',
        text: 'var(--text)',
        mtext: 'var(--mtext)',
        border: 'var(--border)',
        ring: 'var(--ring)',
        ringOffset: 'var(--ring-offset)',
        
        secondaryBlack: '#212121', 
      },
      borderRadius: {
        base: '7px'
      },
      boxShadow: {
        shadow: 'var(--shadow)'
      },
      translate: {
        boxShadowX: '3px',
        boxShadowY: '3px',
        reverseBoxShadowX: '-3px',
        reverseBoxShadowY: '-3px',
      },
      fontWeight: {
        base: '500',
        heading: '700',
      },
    },
  },

  plugins: [
    require("tailwindcss-animate") // or any other plugins you want to use
  ],
}
