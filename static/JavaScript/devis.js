 let compteurLigne = 0;

  function ajouterLigne() {
    compteurLigne++;
    const tbody = document.getElementById('lignesDevis');
    const ligne = document.createElement('tr');
    ligne.id = 'ligne-' + compteurLigne;

    ligne.innerHTML = `
      <td><input type="text" name="designation[]" placeholder="Ex : Développement page d'accueil" required></td>
      <td><input type="number" name="quantite[]" min="1" value="1" oninput="calculerTotal()" required></td>
      <td><input type="number" name="prixUnitaire[]" min="0" step="0.01" placeholder="0.00" oninput="calculerTotal()" required></td>
      <td><button type="button" class="btn-supprimer-ligne" onclick="supprimerLigne(${compteurLigne})">✕</button></td>
    `;

    tbody.appendChild(ligne);
  }

  function supprimerLigne(id) {
    document.getElementById('ligne-' + id).remove();
    calculerTotal();
  }

  function calculerTotal() {
    const quantites = document.querySelectorAll('input[name="quantite[]"]');
    const prix = document.querySelectorAll('input[name="prixUnitaire[]"]');
    let totalHT = 0;

    for (let i = 0; i < quantites.length; i++) {
      const q = parseFloat(quantites[i].value) || 0;
      const p = parseFloat(prix[i].value) || 0;
      totalHT += q * p;
    }

    const tauxTva = parseFloat(document.getElementById('tauxTva').value);
    let montantTva = 0;
    let labelTva = 'TVA';

    if (!isNaN(tauxTva)) {
      montantTva = totalHT * (tauxTva / 100);
      labelTva = `TVA (${tauxTva.toFixed(2)} %)`;
    } else {
      labelTva = 'TVA (non applicable)';
    }

    const totalTTC = totalHT + montantTva;

    document.getElementById('totalHT').textContent = totalHT.toLocaleString('fr-FR', {minimumFractionDigits: 2}) + ' €';
    document.getElementById('labelTva').textContent = labelTva;
    document.getElementById('montantTva').textContent = montantTva.toLocaleString('fr-FR', {minimumFractionDigits: 2}) + ' €';
    document.getElementById('totalTTC').textContent = totalTTC.toLocaleString('fr-FR', {minimumFractionDigits: 2}) + ' €';
  }

  // Une ligne visible dès le chargement de la page
  window.onload = () => ajouterLigne();