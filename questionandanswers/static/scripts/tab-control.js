/*
  Tab navigation code adapted from code found on the MDN web docs
  (https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/Tab_Role)
*/
// Get all tabs and add on click listener
tabs = document.querySelectorAll('[role="tab"]');

tabs.forEach(tab => {
    tab.addEventListener("click", switchTab);
});

// function to handle switching tabs
function switchTab(e) {
  const target = e.target;
  const parent = target.parentNode;
  const grandparent = parent.parentNode;

  // Remove all current selected tabs
  parent
    .querySelectorAll('[aria-selected="true"]')
    .forEach(t => {
      t.setAttribute("aria-selected", false);
      t.classList.remove('button-selected');
    });

  // Set this tab as selected
  target.setAttribute("aria-selected", true);
  target.classList.add('button-selected');

  // Hide all tab panels
  grandparent
    .querySelectorAll('[role="tabpanel"]')
    .forEach(p => p.setAttribute("hidden", true));

  // Show the selected panel
  grandparent.parentNode
    .querySelector(`#${target.getAttribute("aria-controls")}`)
    .removeAttribute("hidden");
}