// Fecha alertas automaticamente após 4 segundos
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => el.style.display = 'none', 4000);
  });
});
