import('tailwindcss').Config
module.exports = {
  important: true,
  content: ['.index.html', 'work.html', 'contact.html', 'index.js','about.html','blog.html',
                ],
  theme: {
    extend: {
      fontFamily: {
        'lexend': ['lexend'],
        'gochi': ['Gochi Hand'],
        'mrdafoe': ['"Mr Dafoe"', 'sans'],
        },
    animation: {
      'spin-slow': 'spin 12s linear infinite',
      },
   
  },
  plugins: [],
}

}