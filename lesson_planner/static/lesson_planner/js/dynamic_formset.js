document.querySelectorAll('.dynamic-formset').forEach((container) => {
  const btn = container.querySelector('.add-row');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const totalInput = container.querySelector('input[id$="-TOTAL_FORMS"]');
    const total = parseInt(totalInput.value, 10);
    const rows = container.querySelectorAll('.form-row');
    if (!rows.length) return;
    const clone = rows[rows.length - 1].cloneNode(true);
    clone.innerHTML = clone.innerHTML.replaceAll(`-${total - 1}-`, `-${total}-`);
    clone.querySelectorAll('input, textarea, select').forEach((el) => {
      if (el.type !== 'hidden') el.value = '';
    });
    rows[rows.length - 1].after(clone);
    totalInput.value = total + 1;
  });
});
